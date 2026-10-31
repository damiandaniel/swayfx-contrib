set -euo pipefail

mode="$1"
shift
root="$PWD"
work=$(mktemp -d)

git clone --quiet "$SWAYFX_URL" "$work/src"
cd "$work/src"
git config user.name ci
git config user.email ci@localhost

if [ "$mode" = "tag" ]; then
  ref=$(git tag --sort=-v:refname | head -n1)
else
  ref=$(git rev-parse HEAD)
fi

if [ "$#" -gt 0 ]; then
  names=("$@")
else
  names=()
  for d in "$root"/patches/*/; do
    [ -d "$d" ] && names+=("$(basename "$d")")
  done
fi

: > "$root/failed-$mode.txt"
for name in "${names[@]}"; do
  dir="$root/patches/$name"
  [ -d "$dir" ] || continue
  git checkout --quiet --detach "$ref"
  git reset --quiet --hard
  if ! git am --quiet --3way "$dir"/*.patch; then
    git am --abort || true
    echo "$name" >> "$root/failed-$mode.txt"
  fi
done

echo "ref=$ref"
cat "$root/failed-$mode.txt"
[ ! -s "$root/failed-$mode.txt" ]
