#!/usr/bin/env bash
# Builds Vencord with the Retroless userplugin and points Vesktop at it.
# Run again to update. Use --uninstall to go back to the stock Vencord build.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
work="${XDG_DATA_HOME:-$HOME/.local/share}/retroless/Vencord"

if [ -d "$HOME/.var/app/dev.vencord.Vesktop/config/vesktop" ]; then
    config="$HOME/.var/app/dev.vencord.Vesktop/config/vesktop"
elif [ -d "${XDG_CONFIG_HOME:-$HOME/.config}/vesktop" ]; then
    config="${XDG_CONFIG_HOME:-$HOME/.config}/vesktop"
else
    echo "Vesktop config folder not found. Start Vesktop once and run this again." >&2
    exit 1
fi

target="$config/retroless-vencord"
state="$config/state.json"

set_dir() {
    node -e '
        const fs = require("fs");
        const [file, dir] = process.argv.slice(1);
        const state = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf8")) : {};
        if (dir) state.vencordDir = dir; else delete state.vencordDir;
        fs.writeFileSync(file, JSON.stringify(state, null, 4));
    ' "$state" "${1:-}"
}

if [ "${1:-}" = "--uninstall" ]; then
    set_dir
    rm -rf "$target"
    echo "Removed. Restart Vesktop to load the stock Vencord build."
    exit 0
fi

for tool in git node npm; do
    command -v "$tool" >/dev/null || { echo "$tool is required" >&2; exit 1; }
done

if [ -d "$work/.git" ]; then
    git -C "$work" pull --ff-only
else
    mkdir -p "$(dirname "$work")"
    git clone --depth 1 https://github.com/Vendicated/Vencord.git "$work"
fi

rm -rf "$work/src/userplugins/retrolessSounds" "$work/src/userplugins/retroless"
mkdir -p "$work/src/userplugins"
cp -r "$repo/plugin/retroless" "$work/src/userplugins/retroless"

pnpm="pnpm"
command -v pnpm >/dev/null || pnpm="npx --yes pnpm@10"

(cd "$work" && $pnpm install --frozen-lockfile && $pnpm build)

mkdir -p "$target"
for file in vencordDesktopMain.js vencordDesktopPreload.js vencordDesktopRenderer.js vencordDesktopRenderer.css; do
    cp "$work/dist/$file" "$target/$file"
done
echo "{}" > "$target/package.json"
set_dir "$target"

echo
echo "Installed to $target"
echo "Restart Vesktop, then enable Retroless in Settings > Plugins."
