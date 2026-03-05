#!/usr/bin/env bash
# fix_project_fields.sh
# Idempotent: finds or creates the LOGOS V1 Development Dashboard project,
# then ensures PHASE, CATEGORY, STATUS, PRIORITY single-select fields exist.
#
# Usage:
#   export GH_TOKEN=ghp_<your-token-with-project-scope>
#   bash fix_project_fields.sh
set -euo pipefail

PROJECT_TITLE="LOGOS V1 Development Dashboard"
OUT_FILE="_Governance/GitHub/Projects/LOGOS_V1_Project_Metadata.json"

echo "== LOGOS Project Field Creation (Idempotent) =="

if ! command -v jq >/dev/null 2>&1; then
  echo "Installing jq..."
  sudo apt-get update -y >/dev/null && sudo apt-get install -y jq >/dev/null
fi

# Resolve owner
REPO_FULL="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
OWNER="${REPO_FULL%/*}"
REPO="${REPO_FULL#*/}"

OWNER_ID="$(gh api graphql -f query='
query($owner:String!,$repo:String!){repository(owner:$owner,name:$repo){owner{id __typename}}}
' -F owner="$OWNER" -F repo="$REPO" --jq '.data.repository.owner.id')"

OWNER_TYPENAME="$(gh api graphql -f query='
query($owner:String!,$repo:String!){repository(owner:$owner,name:$repo){owner{__typename}}}
' -F owner="$OWNER" -F repo="$REPO" --jq '.data.repository.owner.__typename')"

echo "Owner: $OWNER ($OWNER_TYPENAME, $OWNER_ID)"

# Find or create project
PROJECT_ID="$(
  gh api graphql -f query='
query($ownerId:ID!) {
  node(id:$ownerId) {
    ... on Organization { projectsV2(first:50) { nodes { id title } } }
    ... on User         { projectsV2(first:50) { nodes { id title } } }
  }
}' -F ownerId="$OWNER_ID" | jq -r --arg t "$PROJECT_TITLE" '
  .data.node.projectsV2.nodes | map(select(.title==$t)) | .[0].id // empty
')"

if [ -z "${PROJECT_ID:-}" ]; then
  echo "Project not found. Creating: $PROJECT_TITLE"
  PROJECT_ID="$(
    jq -n \
      --arg query 'mutation($ownerId:ID!,$title:String!){createProjectV2(input:{ownerId:$ownerId,title:$title}){projectV2{id title}}}' \
      --arg ownerId "$OWNER_ID" \
      --arg title  "$PROJECT_TITLE" \
      '{"query":$query,"variables":{"ownerId":$ownerId,"title":$title}}' \
    | gh api graphql --input - --jq '.data.createProjectV2.projectV2.id'
  )"
  echo "Created project: $PROJECT_ID"
else
  echo "Project exists: $PROJECT_ID"
fi

# ── helpers ──────────────────────────────────────────────────────────────────
get_field_json() {
  gh api graphql -f query='
query($projectId:ID!) {
  node(id:$projectId) {
    ... on ProjectV2 {
      fields(first:100) {
        nodes {
          __typename
          ... on ProjectV2FieldCommon { id name dataType }
          ... on ProjectV2SingleSelectField {
            id name dataType
            options { id name }
          }
        }
      }
    }
  }
}' -F projectId="$PROJECT_ID"
}

MUTATION='mutation($projectId:ID!,$name:String!,$opts:[ProjectV2SingleSelectFieldOptionInput!]!){createProjectV2Field(input:{projectId:$projectId,dataType:SINGLE_SELECT,name:$name,singleSelectOptions:$opts}){projectV2Field{...on ProjectV2SingleSelectField{id name options{id name}}}}}'

ensure_field() {
  local FIELD_NAME="$1"
  local OPTIONS_JSON="$2"

  local FIELD_ID
  FIELD_ID="$(get_field_json | jq -r --arg n "$FIELD_NAME" '
    .data.node.fields.nodes | map(select(.name == $n)) | .[0].id // empty
  ')"

  if [ -n "$FIELD_ID" ]; then
    echo "  [exists] $FIELD_NAME → $FIELD_ID"
    echo "$FIELD_ID"
    return 0
  fi

  FIELD_ID="$(
    jq -n \
      --arg query   "$MUTATION" \
      --arg pid     "$PROJECT_ID" \
      --arg name    "$FIELD_NAME" \
      --argjson opts "$OPTIONS_JSON" \
      '{"query":$query,"variables":{"projectId":$pid,"name":$name,"opts":$opts}}' \
    | gh api graphql --input - --jq '.data.createProjectV2Field.projectV2Field.id'
  )"
  echo "  [created] $FIELD_NAME → $FIELD_ID"
  echo "$FIELD_ID"
}

# ── create fields ─────────────────────────────────────────────────────────────
# GitHub requires color and description on each option.
# Valid colors: GRAY BLUE GREEN YELLOW ORANGE RED PINK PURPLE
echo "Ensuring fields..."
PHASE_FIELD_ID="$(    ensure_field "PHASE"    '[{"name":"P1","color":"BLUE","description":"Phase 1"},{"name":"P2","color":"GREEN","description":"Phase 2"},{"name":"P3","color":"YELLOW","description":"Phase 3"},{"name":"P4","color":"ORANGE","description":"Phase 4"},{"name":"P5","color":"PURPLE","description":"Phase 5"}]')"
CATEGORY_FIELD_ID="$( ensure_field "CATEGORY" '[{"name":"Phase Deliverable","color":"BLUE","description":""},{"name":"Verification","color":"GREEN","description":""},{"name":"Infrastructure","color":"GRAY","description":""}]')"
STATUS_FIELD_ID="$(   ensure_field "STATUS"   '[{"name":"Backlog","color":"GRAY","description":""},{"name":"Ready","color":"BLUE","description":""},{"name":"In Progress","color":"YELLOW","description":""},{"name":"Verify","color":"ORANGE","description":""},{"name":"Complete","color":"GREEN","description":""}]')"
PRIORITY_FIELD_ID="$( ensure_field "PRIORITY" '[{"name":"High","color":"RED","description":""},{"name":"Medium","color":"YELLOW","description":""},{"name":"Low","color":"GRAY","description":""}]')"

# ── snapshot & write metadata ─────────────────────────────────────────────────
FIELDS_SNAPSHOT="$(get_field_json)"
owner             "$OWNER" \
  --arg repo              "$REPO" \
  --arg 
jq -n \
  --arg project_id        "$PROJECT_ID" \
  --arg phase_field_id    "$PHASE_FIELD_ID" \
  --arg category_field_id "$CATEGORY_FIELD_ID" \
  --arg status_field_id   "$STATUS_FIELD_ID" \
  --arg priority_field_id "$PRIORITY_FIELD_ID" \
  --argjson fields_snap$owner, name: $repo
'{
  schema_version: "1.0",
  generated_utc: (now | todateiso8601),
  repository: { owner: "Project-Logos-2026", name: "Logos" },
  project: { title: "LOGOS V1 Development Dashboard", id: $project_id },
  fields: {
    PHASE:    { id: $phase_field_id },
    CATEGORY: { id: $category_field_id },
    STATUS:   { id: $status_field_id },
    PRIORITY: { id: $priority_field_id }
  },
  fields_snapshot_graphql: $fields_snapshot
}' > "$OUT_FILE"

echo "Wrote: $OUT_FILE"

# ── commit ────────────────────────────────────────────────────────────────────
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
echo "Project ID: $PROJECT_ID"
echo "Fields:"
echo "  PHASE:    $PHASE_FIELD_ID"
echo "  CATEGORY: $CATEGORY_FIELD_ID"
echo "  STATUS:   $STATUS_FIELD_ID"
echo "  PRIORITY: $PRIORITY_FIELD_ID"
echo "Metadata: $OUT_FILE"
