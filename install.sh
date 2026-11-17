#!/usr/bin/env bash
# ReCord installer for Linux, macOS and Windows (Git Bash / WSL).
#
#   curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash -s -- --no-plugin
#   curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash -s -- --uninstall
set -euo pipefail

RAW="${RECORD_RAW:-https://raw.githubusercontent.com/leriart/ReCord/main}"
THEME="ReCord.theme.css"
LEGACY="Retroless.theme.css"

# Set when the script runs from a checkout, so local files are used instead of downloads.
HERE=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

action="install"
plugin=1
enable=1

usage() {
    cat <<'TXT'
ReCord installer

  (no option)     install or update the theme, the startup splash and the plugin
  --no-plugin     theme and splash only; keep the stock Vencord build
  --no-enable     copy the theme but do not switch it on
  --uninstall     remove the theme, the splash and the plugin build
  --help          show this help

The plugin (in-app settings and sounds) is installed for Vesktop. A ready-made
build is downloaded when available; otherwise it is built here, which needs
git and Node.js.

Clients: Vencord, Vesktop, Equicord, Equibop, BetterDiscord (native and Flatpak).
TXT
}

for arg in "$@"; do
    case "$arg" in
        --plugin) plugin=1 ;;
        --no-plugin) plugin=0 ;;
        --no-enable) enable=0 ;;
        --uninstall) action="uninstall" ;;
        --help | -h) usage; exit 0 ;;
        *) echo "Unknown option: $arg" >&2; usage >&2; exit 2 ;;
    esac
done

say() { printf '  %s\n' "$*"; }
title() { printf '\n== %s\n' "$*"; }

fetch() {
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$1" -o "$2"
    elif command -v wget >/dev/null 2>&1; then
        wget -qO "$2" "$1"
    else
        echo "curl or wget is required" >&2
        exit 1
    fi
}

case "$(uname -s)" in
    Darwin) roots=("$HOME/Library/Application Support") ;;
    MINGW* | MSYS* | CYGWIN*) roots=("${APPDATA:-$HOME/AppData/Roaming}") ;;
    *)
        roots=(
            "${XDG_CONFIG_HOME:-$HOME/.config}"
            "$HOME/.var/app/dev.vencord.Vesktop/config"
            "$HOME/.var/app/com.discordapp.Discord/config"
            "$HOME/.var/app/com.discordapp.DiscordCanary/config"
            "$HOME/.var/app/io.github.equicord.equibop/config"
        )
        ;;
esac

clients=()
for root in "${roots[@]}"; do
    for name in Vencord vesktop Equicord equibop BetterDiscord; do
        [ -d "$root/$name" ] && clients+=("$root/$name")
    done
done

json_tool="${RECORD_JSON_TOOL:-}"
if [ -z "$json_tool" ]; then
    if command -v python3 >/dev/null 2>&1; then json_tool="python3"
    elif command -v node >/dev/null 2>&1; then json_tool="node"
    fi
fi

# edit_settings <file> <add|remove>: switches the theme on or off in a Vencord-style settings.json
edit_settings() {
    local file="$1" mode="$2"
    [ -f "$file" ] || return 1
    case "$json_tool" in
        python3)
            python3 - "$file" "$mode" "$THEME" "$LEGACY" <<'PY'
import json, sys
path, mode, theme, legacy = sys.argv[1:5]
with open(path, encoding="utf-8") as handle:
    data = json.load(handle)
enabled = [name for name in data.get("enabledThemes", []) if name not in (theme, legacy)]
if mode == "add":
    enabled.append(theme)
data["enabledThemes"] = enabled
data["themeLinks"] = [link for link in data.get("themeLinks", []) if "leriart/Retroless" not in link and "leriart/ReCord" not in link]
with open(path, "w", encoding="utf-8") as handle:
    json.dump(data, handle, indent=4)
PY
            ;;
        node)
            node -e '
                const fs = require("fs");
                const [path, mode, theme, legacy] = process.argv.slice(1);
                const data = JSON.parse(fs.readFileSync(path, "utf8"));
                const enabled = (data.enabledThemes ?? []).filter(name => name !== theme && name !== legacy);
                if (mode === "add") enabled.push(theme);
                data.enabledThemes = enabled;
                data.themeLinks = (data.themeLinks ?? []).filter(link => !link.includes("leriart/Retroless") && !link.includes("leriart/ReCord"));
                fs.writeFileSync(path, JSON.stringify(data, null, 4));
            ' "$file" "$mode" "$THEME" "$LEGACY"
            ;;
        *) return 1 ;;
    esac
}

# json_set <file> <dotted.key> [json-value]: sets a key, or removes it when no value is given.
# Works with python3 or node, whichever the machine has.
json_set() {
    local file="$1" key="$2" value="${3-}" remove=0
    [ $# -lt 3 ] && remove=1
    case "$json_tool" in
        python3)
            python3 - "$file" "$key" "$value" "$remove" <<'PY'
import json, os, sys
path, key, value, remove = sys.argv[1:5]
data = {}
if os.path.exists(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
node = data
parts = key.split(".")
for part in parts[:-1]:
    node = node.setdefault(part, {})
if remove == "1":
    node.pop(parts[-1], None)
else:
    node[parts[-1]] = json.loads(value)
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as handle:
    json.dump(data, handle, indent=4)
PY
            ;;
        node)
            node -e '
                const fs = require("fs"), path = require("path");
                const [file, key, value, remove] = process.argv.slice(1);
                const data = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf8")) : {};
                const parts = key.split(".");
                let node = data;
                for (const part of parts.slice(0, -1)) node = node[part] ??= {};
                if (remove === "1") delete node[parts.at(-1)]; else node[parts.at(-1)] = JSON.parse(value);
                fs.mkdirSync(path.dirname(file), { recursive: true });
                fs.writeFileSync(file, JSON.stringify(data, null, 4));
            ' "$file" "$key" "$value" "$remove"
            ;;
        *) return 1 ;;
    esac
}

vesktop_dirs() {
    for client in ${clients[@]+"${clients[@]}"}; do
        case "$client" in */vesktop) printf '%s\n' "$client" ;; esac
    done
}

install_theme() {
    title "Theme"
    if [ ${#clients[@]} -eq 0 ]; then
        say "No Vencord, Vesktop, Equicord, Equibop or BetterDiscord folder found."
        say "Start your client once, or add this link in Themes > Online Themes:"
        say "$RAW/$THEME"
        return
    fi

    local tmp
    tmp="$(mktemp)"
    if [ -n "$HERE" ] && [ -f "$HERE/$THEME" ]; then
        cp "$HERE/$THEME" "$tmp"
    else
        fetch "$RAW/$THEME" "$tmp"
    fi
    grep -q "@name ReCord" "$tmp" || { echo "Downloaded file is not the ReCord theme" >&2; rm -f "$tmp"; exit 1; }

    for client in "${clients[@]}"; do
        mkdir -p "$client/themes"
        cp "$tmp" "$client/themes/$THEME"
        rm -f "$client/themes/$LEGACY"
        if [ "$enable" -eq 1 ] && edit_settings "$client/settings/settings.json" add; then
            say "installed and enabled: $client"
        else
            say "installed: $client (enable ReCord in Settings > Themes)"
        fi
    done
    rm -f "$tmp"
}

uninstall_theme() {
    title "Theme"
    for client in ${clients[@]+"${clients[@]}"}; do
        if [ -f "$client/themes/$THEME" ] || [ -f "$client/themes/$LEGACY" ]; then
            rm -f "$client/themes/$THEME" "$client/themes/$LEGACY"
            edit_settings "$client/settings/settings.json" remove || true
            say "removed: $client"
        fi
    done
}

PLUGIN_FILES="vencordDesktopMain.js vencordDesktopPreload.js vencordDesktopRenderer.js vencordDesktopRenderer.css"
PLUGIN_RELEASE="${RECORD_PLUGIN_URL:-https://github.com/leriart/ReCord/releases/download/plugin}"

# Fills $1 with a Vencord build that includes the plugin. A ready-made build is
# tried first, so the machine does not need git or Node.js.
fetch_plugin_build() {
    local out="$1" file
    mkdir -p "$out"
    for file in $PLUGIN_FILES; do
        fetch "$PLUGIN_RELEASE/$file" "$out/$file" 2>/dev/null || return 1
        [ -s "$out/$file" ] || return 1
    done
}

build_plugin() {
    local out="$1" tool file
    for tool in git node npm; do
        command -v "$tool" >/dev/null 2>&1 || return 1
    done

    local work="${XDG_DATA_HOME:-$HOME/.local/share}/record/Vencord"
    if [ -d "$work/.git" ]; then
        git -C "$work" pull --ff-only --quiet || true
    else
        mkdir -p "$(dirname "$work")"
        git clone --quiet --depth 1 https://github.com/Vendicated/Vencord.git "$work" || return 1
    fi

    local dest="$work/src/userplugins/record"
    rm -rf "$work/src/userplugins/retroless" "$work/src/userplugins/retrolessSounds" "$dest"
    mkdir -p "$dest"
    for file in index.tsx native.ts; do
        if [ -n "$HERE" ] && [ -f "$HERE/plugin/record/$file" ]; then
            cp "$HERE/plugin/record/$file" "$dest/$file"
        else
            fetch "$RAW/plugin/record/$file" "$dest/$file" || return 1
        fi
    done

    local pnpm="pnpm"
    command -v pnpm >/dev/null 2>&1 || pnpm="npx --yes pnpm@10"
    say "building Vencord with the ReCord plugin (this takes a minute)"
    local log
    log="$(mktemp)"
    if ! (cd "$work" && $pnpm install --frozen-lockfile && $pnpm build) >"$log" 2>&1; then
        tail -n 30 "$log" >&2
        rm -f "$log"
        return 1
    fi
    rm -f "$log"

    mkdir -p "$out"
    for file in $PLUGIN_FILES; do
        cp "$work/dist/$file" "$out/$file"
    done
}

install_plugin() {
    title "Plugin"
    local targets
    targets="$(vesktop_dirs)"
    if [ -z "$targets" ]; then
        say "Vesktop not found, so the plugin was skipped. The theme works without it."
        say "For a Vencord built from source: copy plugin/record into src/userplugins,"
        say "then run pnpm build && pnpm inject."
        return
    fi
    if [ -z "$json_tool" ]; then
        say "python3 or node is needed to point Vesktop at the plugin build; skipped."
        return
    fi

    local stage
    stage="$(mktemp -d)"
    # A checkout builds its own sources so local changes are what gets installed.
    if [ -n "$HERE" ] && [ -f "$HERE/plugin/record/index.tsx" ] && build_plugin "$stage"; then
        say "built from this checkout"
    elif fetch_plugin_build "$stage"; then
        say "downloaded the ready-made build"
    elif build_plugin "$stage"; then
        say "built on this machine"
    else
        say "No ready-made build could be downloaded and it could not be built here"
        say "(building needs git and Node.js). The theme is still installed."
        rm -rf "$stage"
        return
    fi

    local client file
    while IFS= read -r client; do
        local target="$client/record-vencord"
        mkdir -p "$target"
        for file in $PLUGIN_FILES; do
            cp "$stage/$file" "$target/$file"
        done
        echo "{}" > "$target/package.json"
        rm -rf "$client/retroless-vencord"
        json_set "$client/state.json" vencordDir "\"$target\""
        json_set "$client/settings/settings.json" plugins.ReCord.enabled true
        say "installed and enabled: $target"
    done <<<"$targets"
    rm -rf "$stage"
}

uninstall_plugin() {
    title "Plugin"
    local client
    while IFS= read -r client; do
        [ -n "$client" ] || continue
        if [ -d "$client/record-vencord" ] || [ -d "$client/retroless-vencord" ]; then
            rm -rf "$client/record-vencord" "$client/retroless-vencord"
            json_set "$client/state.json" vencordDir || true
            json_set "$client/settings/settings.json" plugins.ReCord || true
            say "removed: $client (stock Vencord will load again)"
        fi
    done <<<"$(vesktop_dirs)"
    rm -rf "${XDG_DATA_HOME:-$HOME/.local/share}/record" "${XDG_DATA_HOME:-$HOME/.local/share}/retroless"
}

# Vesktop shows its own splash window before Discord loads, so the theme cannot
# reach it; it reads the image from userAssets and the colors from settings.json.
install_splash() {
    title "Startup splash"
    local targets client tmp
    targets="$(vesktop_dirs)"
    if [ -z "$targets" ]; then
        say "Vesktop not found; only Vesktop has a replaceable splash."
        return
    fi

    tmp="$(mktemp)"
    if [ -n "$HERE" ] && [ -f "$HERE/assets/brand/splash.gif" ]; then
        cp "$HERE/assets/brand/splash.gif" "$tmp"
    elif ! fetch "$RAW/assets/brand/splash.gif" "$tmp"; then
        say "could not download the splash image; skipped."
        rm -f "$tmp"
        return
    fi

    while IFS= read -r client; do
        mkdir -p "$client/userAssets"
        cp "$tmp" "$client/userAssets/splash"
        if json_set "$client/settings.json" splashTheming true \
            && json_set "$client/settings.json" splashPixelated true \
            && json_set "$client/settings.json" splashColor '"rgb(240, 222, 198)"' \
            && json_set "$client/settings.json" splashBackground '"rgb(5, 6, 5)"'; then
            say "installed: $client"
        else
            say "image copied: $client (pick it in Vesktop Settings > Customize App Assets)"
        fi
    done <<<"$targets"
    rm -f "$tmp"
}

uninstall_splash() {
    local client key
    while IFS= read -r client; do
        [ -n "$client" ] || continue
        [ -f "$client/userAssets/splash" ] || continue
        rm -f "$client/userAssets/splash"
        for key in splashTheming splashPixelated splashColor splashBackground; do
            json_set "$client/settings.json" "$key" || true
        done
    done <<<"$(vesktop_dirs)"
}

echo "ReCord $action"
if [ "$action" = "uninstall" ]; then
    uninstall_theme
    uninstall_splash
    uninstall_plugin
else
    install_theme
    install_splash
    if [ "$plugin" -eq 1 ]; then install_plugin; fi
fi

echo
echo "Done. Fully close Discord (also from the tray) and open it again."
