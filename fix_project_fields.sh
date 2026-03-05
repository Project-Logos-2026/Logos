#!/usr/bin/env bash
# fix_project_fields.sh
# Idempotent: creates PHASE, CATEGORY, STATUS, PRIORITY single-select fields
# on the existing LOGOS V1 Development Dashboard project.
#
# Usage:
#   export GH_TOKEN=ghp_<your-token-with-project-scope>
#   bash fix_project_fields.sh
set -euo pipefail

PROJECT_ID="PVT_kwHOD3Zliw84BQ2pl"
OUT_FILE="_Governance/GitHub/Projects/LOGOS_V1_Project_Metadata.json"

echo "== LOGOS Project Field Creation (Idempotent) =="
echo "Project ID: $PROJECT_ID"

if ! command -v jq >/dev/null 2>&1; then
  echo "Installing jq..."
  sudo apt-get update -y >/dev/null && sudo apt-get install -y jq >/dev/null
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
echo "Ensuring fields..."
PHASE_FIELD_ID="$(    ensure_field "PHASE"    '[{"name":"P1"},{"name":"P2"},{"name":"P3"},{"name":"P4"},{"name":"P5"}]')"
CATEGORY_FIELD_ID="$( ensure_field "CATEGORY" '[{"name":"Phase Deliverable"},{"name":"Verification"},{"name":"Infrastructure"}]')"
STATUS_FIELD_ID="$(   ensure_field "STATUS"   '[{"name":"Backlog"},{"name":"Ready"},{"name":"In Progress"},{"name":"Verify"},{"name":"Complete"}]')"
PRIORITY_FIELD_ID="$( ensure_field "PRIORITY" '[{"name":"High"},{"name":"Medium"},{"name":"Low"}]')"

# ── snapshot & write metadata ─────────────────────────────────────────────────
FIELDS_SNAPSHOT="$(get_field_json)"

jq -n \
  --arg project_id        "$PROJECT_ID" \
  --arg phase_field_id    "$PHASE_FIELD_ID" \
  --arg category_field_id "$CATEGORY_FIELD_ID" \
  --arg status_field_id   "$STATUS_FIELD_ID" \
  --arg priority_field_id "$PRIORITY_FIELD_ID" \
  --argjson fields_snapshot "$FIELDS_SNAPSHOT" \
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
