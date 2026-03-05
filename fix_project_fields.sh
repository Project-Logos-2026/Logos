#!/usr/bin/env bash
# fix_project_fields.sh — idempotent, handles pre-existing fields
set -euo pipefail

PROJECT_TITLE="LOGOS V1 Development Dashboard"
OUT_FILE="_Governance/GitHub/Projects/LOGOS_V1_Project_Metadata.json"

echo "== LOGOS Project Field Setup (Idempotent) =="

command -v jq >/dev/null 2>&1 || { sudo apt-get update -y >/dev/null && sudo apt-get install -y jq >/dev/null; }

# ── resolve repo + owner ───────────────────────────────────────────────────────
REPO_FULL="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
OWNER="${REPO_FULL%/*}"
REPO="${REPO_FULL#*/}"

OWNER_ID="$(gh api graphql -f query='
query($o:String!,$r:String!){repository(owner:$o,name:$r){owner{id}}}
' -F o="$OWNER" -F r="$REPO" --jq '.data.repository.owner.id')"

echo "Repo: $OWNER/$REPO  Owner ID: $OWNER_ID"

# ── find or create project ─────────────────────────────────────────────────────
PROJECT_ID="$(
  gh api graphql -f query='
query($id:ID!){node(id:$id){... on User{projectsV2(first:50){nodes{id title}}}... on Organization{projectsV2(first:50){nodes{id title}}}}}
' -F id="$OWNER_ID" | jq -r --arg t "$PROJECT_TITLE" '
  .data.node.projectsV2.nodes | map(select(.title==$t)) | .[0].id // empty
')"

if [ -z "${PROJECT_ID:-}" ]; then
  PROJECT_ID="$(
    jq -n \
      --arg q 'mutation($o:ID!,$t:String!){createProjectV2(input:{ownerId:$o,title:$t}){projectV2{id}}}' \
      --arg o "$OWNER_ID" --arg t "$PROJECT_TITLE" \
      '{"query":$q,"variables":{"o":$o,"t":$t}}' \
    | gh api graphql --input - --jq '.data.createProjectV2.projectV2.id'
  )"
  echo "Created project: $PROJECT_ID"
else
  echo "Project exists: $PROJECT_ID"
fi

# ── fetch all current fields ───────────────────────────────────────────────────
fetch_fields() {
  gh api graphql -f query='
query($p:ID!){node(id:$p){... on ProjectV2{fields(first:100){nodes{
  __typename
  ... on ProjectV2FieldCommon{id name}
  ... on ProjectV2SingleSelectField{id name options{id name}}
}}}}}' -F p="$PROJECT_ID"
}

# look up field ID by exact name (case-sensitive, as stored on GitHub)
field_id_by_name() {
  local fname="$1"
  fetch_fields | jq -r --arg n "$fname" \
    '.data.node.fields.nodes | map(select(.name == $n)) | .[0].id // empty'
}

# look up field ID case-insensitively (for STATUS vs Status collision)
field_id_icase() {
  local fname="${1,,}"   # lowercase
  fetch_fields | jq -r --arg n "$fname" \
    '.data.node.fields.nodes | map(select(.name | ascii_downcase == $n)) | .[0].id // empty'
}

MUTATION='mutation($p:ID!,$n:String!,$o:[ProjectV2SingleSelectFieldOptionInput!]!){createProjectV2Field(input:{projectId:$p,dataType:SINGLE_SELECT,name:$n,singleSelectOptions:$o}){projectV2Field{... on ProjectV2SingleSelectField{id name}}}}'

ensure_field() {
  local FNAME="$1"
  local OPTS="$2"

  # exact-name lookup first
  local FID
  FID="$(field_id_by_name "$FNAME")"

  if [ -n "$FID" ]; then
    echo "  [exists] $FNAME → $FID"
    printf '%s' "$FID"
    return 0
  fi

  # try to create
  local CREATE_OUT
  CREATE_OUT="$(
    jq -n \
      --arg q  "$MUTATION" \
      --arg p  "$PROJECT_ID" \
      --arg n  "$FNAME" \
      --argjson o "$OPTS" \
      '{"query":$q,"variables":{"p":$p,"n":$n,"o":$o}}' \
    | gh api graphql --input - 2>&1
  )" || true

  FID="$(printf '%s' "$CREATE_OUT" | jq -r '.data.createProjectV2Field.projectV2Field.id // empty' 2>/dev/null || true)"

  if [ -n "$FID" ]; then
    echo "  [created] $FNAME → $FID"
    printf '%s' "$FID"
    return 0
  fi

  # creation failed (likely name collision) — fall back to case-insensitive lookup
  FID="$(field_id_icase "$FNAME")"
  if [ -n "$FID" ]; then
    echo "  [reused existing] $FNAME (case collision) → $FID"
    printf '%s' "$FID"
    return 0
  fi

  echo "  [ERROR] Could not find or create field: $FNAME" >&2
  printf ''
}

# ── ensure all four fields ─────────────────────────────────────────────────────
echo "Ensuring fields..."
PHASE_ID="$(    ensure_field "PHASE"    '[{"name":"P1","color":"BLUE","description":"Phase 1"},{"name":"P2","color":"GREEN","description":"Phase 2"},{"name":"P3","color":"YELLOW","description":"Phase 3"},{"name":"P4","color":"ORANGE","description":"Phase 4"},{"name":"P5","color":"PURPLE","description":"Phase 5"}]')"
CATEGORY_ID="$( ensure_field "CATEGORY" '[{"name":"Phase Deliverable","color":"BLUE","description":""},{"name":"Verification","color":"GREEN","description":""},{"name":"Infrastructure","color":"GRAY","description":""}]')"
STATUS_ID="$(   ensure_field "STATUS"   '[{"name":"Backlog","color":"GRAY","description":""},{"name":"Ready","color":"BLUE","description":""},{"name":"In Progress","color":"YELLOW","description":""},{"name":"Verify","color":"ORANGE","description":""},{"name":"Complete","color":"GREEN","description":""}]')"
PRIORITY_ID="$( ensure_field "PRIORITY" '[{"name":"High","color":"RED","description":""},{"name":"Medium","color":"YELLOW","description":""},{"name":"Low","color":"GRAY","description":""}]')"

# ── snapshot + write metadata ──────────────────────────────────────────────────
SNAPSHOT="$(fetch_fields)"

mkdir -p "$(dirname "$OUT_FILE")"

jq -n \
  --arg owner      "$OWNER" \
  --arg repo       "$REPO" \
  --arg proj_title "$PROJECT_TITLE" \
  --arg proj_id    "$PROJECT_ID" \
  --arg phase      "$PHASE_ID" \
  --arg category   "$CATEGORY_ID" \
  --arg status     "$STATUS_ID" \
  --arg priority   "$PRIORITY_ID" \
  --argjson snap   "$SNAPSHOT" \
'{
  schema_version: "1.0",
  generated_utc: (now | todateiso8601),
  repository: { owner: $owner, name: $repo },
  project: { title: $proj_title, id: $proj_id },
  fields: {
    PHASE:    { id: $phase },
    CATEGORY: { id: $category },
    STATUS:   { id: $status },
    PRIORITY: { id: $priority }
  },
  fields_snapshot_graphql: $snap
}' > "$OUT_FILE"

echo "Wrote: $OUT_FILE"

# ── commit ─────────────────────────────────────────────────────────────────────
git add "$OUT_FILE"
if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "Update LOGOS V1 project metadata: field IDs resolved"
  git push
  echo "Committed and pushed."
fi

echo ""
echo "== SUCCESS =="
echo "Project:  $PROJECT_TITLE ($PROJECT_ID)"
echo "  PHASE:    $PHASE_ID"
echo "  CATEGORY: $CATEGORY_ID"
echo "  STATUS:   $STATUS_ID"
echo "  PRIORITY: $PRIORITY_ID"
echo "Metadata: $OUT_FILE"
