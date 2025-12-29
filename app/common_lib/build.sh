#!/bin/bash

set -Eeuo pipefail

die(){ echo "❌ $*" >&2; exit 1; }

# load .env
[[ -f .env ]] || die ".env not found"
set -a
source .env
set +a

: "${PKG_VERSION:?}"
: "${NEXUS_REPO_URL:?}"
: "${NEXUS_USERNAME:?}"
: "${NEXUS_PASSWORD:?}"

echo "▶ Publish common-lib"
echo "  - version : $PKG_VERSION"
echo "  - nexus   : $NEXUS_REPO_URL"

[[ -f pyproject.toml ]] || die "pyproject.toml not found"

# version line replace (single-line form required)
sed -i.bak -E "s/^version *= *\"[^\"]+\"/version = \"${PKG_VERSION}\"/" pyproject.toml
rm -f pyproject.toml.bak
grep -q "version = \"${PKG_VERSION}\"" pyproject.toml || die "version update failed"

rm -rf dist build *.egg-info
python -m pip install -U pip build twine
python -m build

python -m twine upload \
  --repository-url "$NEXUS_REPO_URL" \
  -u "$NEXUS_USERNAME" \
  -p "$NEXUS_PASSWORD" \
  dist/*

echo "✅ Publish done"
