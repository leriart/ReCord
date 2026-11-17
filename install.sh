#!/usr/bin/env bash
# ReCord installer for Linux, macOS and Windows (Git Bash / WSL).
#
#   curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash -s -- --plugin
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
plugin=0
enable=1

usage() {
    cat <<'TXT'
ReCord installer

  (no option)     install or update the theme in every client found
  --plugin        also build and install the ReCord plugin for Vesktop
                  (in-app settings and sounds; needs git and Node.js)
  --no-enable     copy the theme but do not switch it on
  --uninstall     remove the theme and the plugin build
  --help          show this help

Clients: Vencord, Vesktop, Equicord, Equibop, BetterDiscord (native and Flatpak).
TXT
}

for arg in "$@"; do
    case "$arg" in
        --plugin) plugin=1 ;;
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

json_tool=""
if command -v python3 >/dev/null 2>&1; then json_tool="python3"
elif command -v node >/dev/null 2>&1; then json_tool="node"
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

# set_state <file> <key> [value]: sets or removes a key in Vesktop state.json
set_state() {
    node -e '
        const fs = require("fs");
        const [file, key, value] = process.argv.slice(1);
        const state = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf8")) : {};
        if (value) state[key] = value; else delete state[key];
        fs.writeFileSync(file, JSON.stringify(state, null, 4));
    ' "$@"
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

install_plugin() {
    title "Plugin"
    for tool in git node npm; do
        command -v "$tool" >/dev/null 2>&1 || { say "$tool is required for --plugin; skipped."; return; }
    done

    local targets
    targets="$(vesktop_dirs)"
    if [ -z "$targets" ]; then
        say "Vesktop not found. For other Vencord installs copy plugin/record"
        say "into src/userplugins of your Vencord checkout and run pnpm build && pnpm inject."
        return
    fi

    local work="${XDG_DATA_HOME:-$HOME/.local/share}/record/Vencord"
    if [ -d "$work/.git" ]; then
        git -C "$work" pull --ff-only --quiet
    else
        mkdir -p "$(dirname "$work")"
        git clone --quiet --depth 1 https://github.com/Vendicated/Vencord.git "$work"
    fi

    local dest="$work/src/userplugins/record"
    rm -rf "$work/src/userplugins/retroless" "$work/src/userplugins/retrolessSounds" "$dest"
    mkdir -p "$dest"
    for file in index.tsx native.ts; do
        if [ -n "$HERE" ] && [ -f "$HERE/plugin/record/$file" ]; then
            cp "$HERE/plugin/record/$file" "$dest/$file"
        else
            fetch "$RAW/plugin/record/$file" "$dest/$file"
        fi
    done

    local pnpm="pnpm"
    command -v pnpm >/dev/null 2>&1 || pnpm="npx --yes pnpm@10"
    say "building Vencord with the ReCord plugin (this takes a minute)"
    local log
    log="$(mktemp)"
    if ! (cd "$work" && $pnpm install --frozen-lockfile && $pnpm build) >"$log" 2>&1; then
        tail -n 30 "$log" >&2
        echo "Plugin build failed. The theme is still installed." >&2
        rm -f "$log"
        return
    fi
    rm -f "$log"

    while IFS= read -r client; do
        local target="$client/record-vencord"
        mkdir -p "$target"
        for file in vencordDesktopMain.js vencordDesktopPreload.js vencordDesktopRenderer.js vencordDesktopRenderer.css; do
            cp "$work/dist/$file" "$target/$file"
        done
        echo "{}" > "$target/package.json"
        rm -rf "$client/retroless-vencord"
        set_state "$client/state.json" vencordDir "$target"
        say "installed: $target"
    done <<<"$targets"
    say "Enable ReCord in Settings > Plugins after restarting."
}

uninstall_plugin() {
    title "Plugin"
    while IFS= read -r client; do
        [ -n "$client" ] || continue
        if [ -d "$client/record-vencord" ] || [ -d "$client/retroless-vencord" ]; then
            rm -rf "$client/record-vencord" "$client/retroless-vencord"
            command -v node >/dev/null 2>&1 && set_state "$client/state.json" vencordDir
            say "removed: $client (stock Vencord will load again)"
        fi
    done <<<"$(vesktop_dirs)"
    rm -rf "${XDG_DATA_HOME:-$HOME/.local/share}/record" "${XDG_DATA_HOME:-$HOME/.local/share}/retroless"
}

echo "ReCord $action"
if [ "$action" = "uninstall" ]; then
    uninstall_theme
    uninstall_plugin
else
    install_theme
    [ "$plugin" -eq 1 ] && install_plugin
fi

echo
echo "Done. Fully close Discord (also from the tray) and open it again."
