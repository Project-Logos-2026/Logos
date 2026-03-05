#!/usr/bin/env bash
set -euo pipefail

echo "== LOGOS GitHub Projects v2 Setup (Idempotent) =="

# ─────────────────────────────────────────────────────────────
# 0) Preconditions
# ─────────────────────────────────────────────────────────────
if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI not found in this environment."
  exit 1
fi

echo "Checking GitHub auth..."
gh auth status >/dev/null 2>&1 || {
  echo "ERROR: gh is not authenticated. Run: gh auth login"
  exit 1
}

# Projects v2 mutations require a PAT with 'project' scope.
# The default Codespaces GITHUB_TOKEN (GitHub App token with no OAuth scopes)
# cannot create or modify Projects v2.
# Resolution: Create a classic PAT at https://github.com/settings/tokens
# with scopes: repo, project — then export it:
#   export GH_TOKEN=ghp_<your-token>
# and re-run this script.
SCOPES="$(gh api user --include 2>/dev/null | grep -i '^x-oauth-scopes:' | cut -d: -f2- | tr -d ' \r')"
if [ -z "$SCOPES" ]; then
  echo ""
  echo "ERROR: The current GitHub token has no OAuth scopes (it is a GitHub App/GITHUB_TOKEN)."
  echo "       GitHub Projects v2 mutations require a PAT with 'project' scope."
  echo ""
  echo "  To fix:"
  echo "    1. Create a classic PAT at: https://github.com/settings/tokens"
  echo "       Required scopes: repo, project"
  echo "    2. In this terminal, run:  export GH_TOKEN=ghp_<your-token>"
  echo "    3. Re-run this script."
  echo ""
  exit 1
fi
if [[ "$SCOPES" != *"project"* ]]; then
  echo ""
  echo "ERROR: Current token scopes ($SCOPES) do not include 'project'."
  echo "       GitHub Projects v2 mutations require the 'project' scope."
  echo "       Please supply a PAT that includes 'project': export GH_TOKEN=ghp_..."
  echo ""
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Installing jq..."
  sudo apt-get update -y >/dev/null
  sudo apt-get install -y jq >/dev/null
fi

# ─────────────────────────────────────────────────────────────
# 1) Resolve repo owner/name + ownerId (user or org)
# ─────────────────────────────────────────────────────────────
REPO_FULL="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
OWNER="${REPO_FULL%/*}"
REPO="${REPO_FULL#*/}"

echo "Repo detected: ${OWNER}/${REPO}"

OWNER_ID="$(gh api graphql -f query='
query($owner:String!, $repo:String!) {
  repository(owner:$owner, name:$repo) {
    owner { id login __typename }
  }
}' -F owner="$OWNER" -F repo="$REPO" --jq '.data.repository.owner.id')"

OWNER_TYPENAME="$(gh api graphql -f query='
query($owner:String!, $repo:String!) {
  repository(owner:$owner, name:$repo) {
    owner { id login __typename }
  }
}' -F owner="$OWNER" -F repo="$REPO" --jq '.data.repository.owner.__typename')"

echo "Owner type: ${OWNER_TYPENAME}"
echo "Owner id:   ${OWNER_ID}"

# ─────────────────────────────────────────────────────────────
# 2) Find or create the Project v2 board
# ─────────────────────────────────────────────────────────────
PROJECT_TITLE="LOGOS V1 Development Dashboard"

PROJECT_ID="$(
  gh api graphql -f query='
query($ownerId:ID!) {
  node(id:$ownerId) {
    ... on Organization {
      projectsV2(first:50) { nodes { id title } }
    }
    ... on User {
      projectsV2(first:50) { nodes { id title } }
    }
  }
}' -F ownerId="$OWNER_ID" | jq -r --arg t "$PROJECT_TITLE" '
  (
    .data.node.projectsV2.nodes
    | map(select(.title == $t))
    | .[0].id
  ) // empty
')"

if [ -z "${PROJECT_ID:-}" ]; then
  echo "Project not found. Creating: ${PROJECT_TITLE}"
  PROJECT_ID="$(
    gh api graphql -f query='
mutation($ownerId:ID!, $title:String!) {
  createProjectV2(input:{ownerId:$ownerId, title:$title}) {
    projectV2 { id title }
  }
}' -F ownerId="$OWNER_ID" -F title="$PROJECT_TITLE" --jq '.data.createProjectV2.projectV2.id'
  )"
  echo "Created project id: ${PROJECT_ID}"
else
  echo "Project exists. Using id: ${PROJECT_ID}"
fi

# ─────────────────────────────────────────────────────────────
# 3) Helpers: ensure single-select field exists (name + options)
# ─────────────────────────────────────────────────────────────
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
            id
            name
            dataType
            options { id name }
          }
        }
      }
    }
  }
}' -F projectId="$PROJECT_ID"
}

ensure_single_select_field() {
  local FIELD_NAME="$1"
  local OPTIONS_JSON="$2"

  local FIELD_ID
  FIELD_ID="$(get_field_json | jq -r --arg n "$FIELD_NAME" '
    .data.node.fields.nodes
    | map(select(.name == $n))
    | .[0].id // empty
  ')"

  if [ -n "$FIELD_ID" ]; then
    echo "Field exists: $FIELD_NAME (id: $FIELD_ID)" >&2
    echo "$FIELD_ID"
    return 0
  fi

  echo "Creating field: $FIELD_NAME" >&2
  FIELD_ID="$(
    gh api graphql -f query='
mutation($projectId:ID!, $name:String!, $opts:[ProjectV2SingleSelectFieldOptionInput!]!) {
  createProjectV2Field(input:{
    projectId:$projectId,
    dataType:SINGLE_SELECT,
    name:$name,
    singleSelectOptions:$opts
  }) {
    projectV2Field {
      ... on ProjectV2SingleSelectField {
        id
        name
        options { id name }
      }
    }
  }
}' -F projectId="$PROJECT_ID" -F name="$FIELD_NAME" -f opts="$OPTIONS_JSON" --jq '.data.createProjectV2Field.projectV2Field.id'
  )"

  echo "Created field: $FIELD_NAME (id: $FIELD_ID)" >&2
  echo "$FIELD_ID"
}

# ─────────────────────────────────────────────────────────────
# 4) Ensure required fields and options
# ─────────────────────────────────────────────────────────────
PHASE_OPTS='[{"name":"P1"},{"name":"P2"},{"name":"P3"},{"name":"P4"},{"name":"P5"}]'
CATEGORY_OPTS='[{"name":"Phase Deliverable"},{"name":"Verification"},{"name":"Infrastructure"}]'
STATUS_OPTS='[{"name":"Backlog"},{"name":"Ready"},{"name":"In Progress"},{"name":"Verify"},{"name":"Complete"}]'
PRIORITY_OPTS='[{"name":"High"},{"name":"Medium"},{"name":"Low"}]'

PHASE_FIELD_ID="$(ensure_single_select_field "PHASE" "$PHASE_OPTS")"
CATEGORY_FIELD_ID="$(ensure_single_select_field "CATEGORY" "$CATEGORY_OPTS")"
STATUS_FIELD_ID="$(ensure_single_select_field "STATUS" "$STATUS_OPTS")"
PRIORITY_FIELD_ID="$(ensure_single_select_field "PRIORITY" "$PRIORITY_OPTS")"

# Pull back the full resolved field+option IDs for metadata
FIELDS_SNAPSHOT="$(get_field_json)"

# ─────────────────────────────────────────────────────────────
# 5) Write canonical metadata artifact for downstream prompts
# ─────────────────────────────────────────────────────────────
OUT_DIR="_Governance/GitHub/Projects"
OUT_FILE="${OUT_DIR}/LOGOS_V1_Project_Metadata.json"

mkdir -p "$OUT_DIR"

jq -n \
  --arg owner "$OWNER" \
  --arg repo "$REPO" \
  --arg project_title "$PROJECT_TITLE" \
  --arg project_id "$PROJECT_ID" \
  --arg phase_field_id "$PHASE_FIELD_ID" \
  --arg category_field_id "$CATEGORY_FIELD_ID" \
  --arg status_field_id "$STATUS_FIELD_ID" \
  --arg priority_field_id "$PRIORITY_FIELD_ID" \
  --argjson fields_snapshot "$FIELDS_SNAPSHOT" \
'{
  schema_version: "1.0",
  generated_utc: (now | todateiso8601),
  repository: { owner: $owner, name: $repo },
  project: { title: $project_title, id: $project_id },
  fields: {
    PHASE: { id: $phase_field_id },
    CATEGORY: { id: $category_field_id },
    STATUS: { id: $status_field_id },
    PRIORITY: { id: $priority_field_id }
  },
  fields_snapshot_graphql: $fields_snapshot
}' > "$OUT_FILE"

echo "Wrote metadata: $OUT_FILE"

# ─────────────────────────────────────────────────────────────
# 6) Commit metadata artifact
# ─────────────────────────────────────────────────────────────
git status --porcelain
git add "$OUT_FILE"

if git diff --cached --quiet; then
  echo "No changes to commit (metadata already up to date)."
else
  git commit -m "Add LOGOS V1 GitHub Project v2 metadata (ids + fields)"
  git push
  echo "Committed and pushed: $OUT_FILE"
fi

# ─────────────────────────────────────────────────────────────
# 7) Report success summary
# ─────────────────────────────────────────────────────────────
echo ""
echo "== SUCCESS =="
echo "Project Title: $PROJECT_TITLE"
echo "Project ID:    $PROJECT_ID"
echo "Fields:"
echo "  PHASE:    $PHASE_FIELD_ID"
echo "  CATEGORY: $CATEGORY_FIELD_ID"
echo "  STATUS:   $STATUS_FIELD_ID"
echo "  PRIORITY: $PRIORITY_FIELD_ID"
echo "Metadata:   $OUT_FILE"
echo ""
echo "Next: run Prompt 2 (GitHub Actions Setup) to create/merge workflows before branch protection."
