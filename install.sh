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
CACHEBUST="$(date +%s)"

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
  --doctor        report what is installed and how Discord is rendering; changes nothing
  --help          show this help

The plugin (in-app settings and sounds) is installed for Vesktop. A ready-made
build is downloaded when available; otherwise it is built here, which needs
git and Node.js.

Clients: Vencord, Vesktop, Equicord, Equibop, BetterDiscord, Dorion, Legcord,
GoofCord and Replugged (native and Flatpak).
TXT
}

for arg in "$@"; do
    case "$arg" in
        --plugin) plugin=1 ;;
        --no-plugin) plugin=0 ;;
        --doctor) action="doctor" ;;
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
        curl -fsSL --retry 2 --retry-delay 1 "$1" -o "$2"
    elif command -v wget >/dev/null 2>&1; then
        wget -q --tries=2 -O "$2" "$1"
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
            "$HOME/.var/app/app.legcord.Legcord/config"
            "$HOME/.var/app/io.github.milkshiift.GoofCord/config"
        )
        ;;
esac

# Clients that take a .theme.css in a themes folder and a Vencord-style settings file.
clients=()
# Clients with their own theme format: "kind:folder".
others=()
for root in "${roots[@]}"; do
    for name in Vencord vesktop Equicord equibop BetterDiscord; do
        [ -d "$root/$name" ] && clients+=("$root/$name")
    done
    for name in dorion legcord replugged goofcord; do
        [ -d "$root/$name" ] && others+=("$name:$root/$name")
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
    if [ ${#clients[@]} -eq 0 ] && [ ${#others[@]} -eq 0 ]; then
        say "No supported client folder found (Vencord, Vesktop, Equicord, Equibop,"
        say "BetterDiscord, Dorion, Legcord, GoofCord, Replugged)."
        say "Start your client once, or add this link in Themes > Online Themes:"
        say "$RAW/$THEME"
        return
    fi

    local tmp
    tmp="$(mktemp)"
    if [ -n "$HERE" ] && [ -f "$HERE/$THEME" ]; then
        cp "$HERE/$THEME" "$tmp"
    else
        fetch "$RAW/$THEME?$CACHEBUST" "$tmp"
    fi
    grep -q "@name ReCord" "$tmp" || { echo "Downloaded file is not the ReCord theme" >&2; rm -f "$tmp"; exit 1; }

    for client in ${clients[@]+"${clients[@]}"}; do
        mkdir -p "$client/themes"
        cp "$tmp" "$client/themes/$THEME"
        rm -f "$client/themes/$LEGACY"
        if [ "$enable" -eq 1 ] && edit_settings "$client/settings/settings.json" add; then
            say "installed and enabled: $client"
        else
            say "installed: $client (enable ReCord in Settings > Themes)"
        fi
    done
    local entry
    for entry in ${others[@]+"${others[@]}"}; do
        install_other "${entry%%:*}" "${entry#*:}" "$tmp"
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
    local entry
    for entry in ${others[@]+"${others[@]}"}; do
        uninstall_other "${entry%%:*}" "${entry#*:}"
    done
}

# json_list <file> <key> <add|remove> <value>: keeps a string in, or out of, a JSON array.
json_list() {
    local file="$1" key="$2" mode="$3" value="$4"
    case "$json_tool" in
        python3)
            python3 - "$file" "$key" "$mode" "$value" <<'PY'
import json, os, sys
path, key, mode, value = sys.argv[1:5]
data = {}
if os.path.exists(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
items = [item for item in (data.get(key) or []) if item != value]
if mode == "add":
    items.append(value)
data[key] = items
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as handle:
    json.dump(data, handle, indent=4)
PY
            ;;
        node)
            node -e '
                const fs = require("fs"), path = require("path");
                const [file, key, mode, value] = process.argv.slice(1);
                const data = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf8")) : {};
                const items = (data[key] ?? []).filter(item => item !== value);
                if (mode === "add") items.push(value);
                data[key] = items;
                fs.mkdirSync(path.dirname(file), { recursive: true });
                fs.writeFileSync(file, JSON.stringify(data, null, 4));
            ' "$file" "$key" "$mode" "$value"
            ;;
        *) return 1 ;;
    esac
}

# Each of these clients stores themes its own way; the paths and formats come
# from their source code.
install_other() {
    local kind="$1" dir="$2" css="$3" target
    case "$kind" in
        dorion)
            # Windows keeps Dorion themes under the home folder, not AppData.
            target="$dir/themes"
            case "$(uname -s)" in MINGW* | MSYS* | CYGWIN*) target="${USERPROFILE:-$HOME}/dorion/themes" ;; esac
            mkdir -p "$target"
            rm -f "$target/$LEGACY"
            cp "$css" "$target/$THEME"
            if [ "$enable" -eq 1 ] && json_list "$dir/config.json" themes add "$THEME"; then
                say "installed and enabled: $dir (Dorion)"
            else
                say "installed: $dir (Dorion; enable ReCord in its theme settings)"
            fi
            ;;
        legcord)
            target="$dir/themes/ReCord"
            rm -rf "$target"
            mkdir -p "$target"
            cp "$css" "$target/src.css"
            cat > "$target/manifest.json" <<JSON
{
    "id": "ReCord",
    "name": "ReCord",
    "author": "leriart",
    "description": "A REPLACED-inspired terminal for Discord.",
    "version": "$(sed -n 's/^ \* @version //p' "$css" | head -n 1)",
    "source": "https://github.com/leriart/ReCord",
    "theme": "src.css",
    "enabled": $([ "$enable" -eq 1 ] && echo true || echo false)
}
JSON
            say "installed: $dir (Legcord)"
            ;;
        replugged)
            target="$dir/themes/dev.leriart.record"
            rm -rf "$target"
            mkdir -p "$target"
            cp "$css" "$target/$THEME"
            cat > "$target/manifest.json" <<JSON
{
    "id": "dev.leriart.record",
    "name": "ReCord",
    "description": "A REPLACED-inspired terminal for Discord.",
    "author": { "name": "leriart", "github": "leriart" },
    "version": "$(sed -n 's/^ \* @version //p' "$css" | head -n 1)",
    "license": "Apache-2.0",
    "type": "replugged-theme",
    "main": "$THEME",
    "source": "https://github.com/leriart/ReCord"
}
JSON
            say "installed: $dir (Replugged; enable ReCord in Settings > Themes)"
            ;;
        goofcord)
            # GoofCord loads every .css in this folder.
            target="$dir/GoofCord/assets"
            mkdir -p "$target"
            rm -f "$target/$LEGACY"
            cp "$css" "$target/$THEME"
            say "installed: $dir (GoofCord)"
            ;;
    esac
}

uninstall_other() {
    local kind="$1" dir="$2"
    case "$kind" in
        dorion)
            local target="$dir/themes"
            case "$(uname -s)" in MINGW* | MSYS* | CYGWIN*) target="${USERPROFILE:-$HOME}/dorion/themes" ;; esac
            [ -f "$target/$THEME" ] || return 0
            rm -f "$target/$THEME"
            json_list "$dir/config.json" themes remove "$THEME" || true
            ;;
        legcord) [ -d "$dir/themes/ReCord" ] || return 0; rm -rf "$dir/themes/ReCord" ;;
        replugged) [ -d "$dir/themes/dev.leriart.record" ] || return 0; rm -rf "$dir/themes/dev.leriart.record" ;;
        goofcord) [ -f "$dir/GoofCord/assets/$THEME" ] || return 0; rm -f "$dir/GoofCord/assets/$THEME" ;;
    esac
    say "removed: $dir"
}

PLUGIN_FILES="vencordDesktopMain.js vencordDesktopPreload.js vencordDesktopRenderer.js vencordDesktopRenderer.css"
PLUGIN_RELEASE="${RECORD_PLUGIN_URL:-https://github.com/leriart/ReCord/releases/download/plugin}"

# Fills $1 with a Vencord build that includes the plugin. A ready-made build is
# tried first, so the machine does not need git or Node.js.
fetch_plugin_build() {
    local out="$1" file
    mkdir -p "$out"
    for file in $PLUGIN_FILES; do
        fetch "$PLUGIN_RELEASE/$file?$CACHEBUST" "$out/$file" 2>/dev/null || return 1
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
            fetch "$RAW/plugin/record/$file?$CACHEBUST" "$dest/$file" || return 1
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

    local file
    for file in $PLUGIN_FILES; do
        if [ ! -s "$stage/$file" ] || [ "$(wc -c < "$stage/$file")" -lt 1024 ]; then
            say "The plugin build is incomplete: $file"
            rm -rf "$stage"
            return
        fi
    done

    local client
    while IFS= read -r client; do
        local target="$client/record-vencord"
        local next="$client/record-vencord.new"
        rm -rf "$next"
        mkdir -p "$next"
        for file in $PLUGIN_FILES; do
            cp "$stage/$file" "$next/$file"
        done
        echo "{}" > "$next/package.json"
        rm -rf "$target"
        mv "$next" "$target"
        rm -rf "$client/retroless-vencord"
        json_set "$client/state.json" vencordDir "\"$target\""
        json_set "$client/settings/settings.json" plugins.ReCord.enabled true
        say "installed cleanly and enabled: $target"
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
    elif ! fetch "$RAW/assets/brand/splash.gif?$CACHEBUST" "$tmp"; then
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

# read_flag <file> <key>: prints true, false or unset for a top-level JSON boolean.
read_flag() {
    [ -f "$1" ] || { echo "default"; return; }
    case "$json_tool" in
        python3) python3 -c 'import json,sys; v=json.load(open(sys.argv[1])).get(sys.argv[2]); print("default" if v is None else str(v).lower())' "$1" "$2" 2>/dev/null || echo "default" ;;
        node) node -e 'const v=JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"))[process.argv[2]]; console.log(v===undefined?"default":String(v))' "$1" "$2" 2>/dev/null || echo "default" ;;
        *) echo "default" ;;
    esac
}

# Reports only. Graphics settings are left alone on purpose: the right ones
# depend on the driver, and a wrong flag can leave the window black.
doctor() {
    title "Clients"
    local client entry found=0
    for client in ${clients[@]+"${clients[@]}"}; do
        found=1
        if [ -f "$client/themes/$THEME" ]; then
            say "$client: theme installed ($(sed -n 's/^ \* @version //p' "$client/themes/$THEME" | head -n 1))"
        else
            say "$client: theme not installed"
        fi
    done
    for entry in ${others[@]+"${others[@]}"}; do
        found=1
        say "${entry#*:} (${entry%%:*})"
    done
    [ "$found" -eq 1 ] || say "none found"

    title "Rendering"
    local gpu=""
    if command -v lspci >/dev/null 2>&1; then
        gpu="$(lspci 2>/dev/null | grep -Ei 'vga|3d|display' | sed 's/^[^:]*:[^:]*: //' | head -n 3)"
    elif [ "$(uname -s)" = "Darwin" ]; then
        gpu="$(system_profiler SPDisplaysDataType 2>/dev/null | sed -n 's/^ *Chipset Model: //p' | head -n 3)"
    fi
    if [ -n "$gpu" ]; then
        printf '%s\n' "$gpu" | while IFS= read -r line; do say "GPU: $line"; done
    else
        say "GPU: could not be detected"
    fi

    local targets acceleration video
    targets="$(vesktop_dirs)"
    if [ -z "$targets" ]; then
        say "Vesktop not found. In Discord: Settings > Advanced > Hardware Acceleration."
    else
        while IFS= read -r client; do
            acceleration="$(read_flag "$client/settings.json" hardwareAcceleration)"
            video="$(read_flag "$client/settings.json" hardwareVideoAcceleration)"
            say "$client"
            say "  hardware acceleration: $acceleration   video decoding: $video"
            if [ "$acceleration" = "false" ]; then
                say "  Discord is drawing on the CPU. Turn on Hardware Acceleration in Vesktop Settings,"
                say "  or switch on Low power in the ReCord plugin."
            fi
        done <<<"$targets"
    fi

    title "If Discord feels heavy"
    say "1. Keep hardware acceleration on. It matters more than any theme option."
    say "2. In the ReCord plugin turn on Low power: no scan beam, grain, flicker or constant animations."
    say "3. Discord > Settings > Accessibility: turn off autoplay for GIFs and animated emoji and stickers."
    say "4. Discord > Settings > Chat: turn off link previews you do not need."
    say "To see what the browser engine is actually using, open chrome://gpu from a Chromium window."
}

echo "ReCord $action"
if [ "$action" = "doctor" ]; then
    doctor
    exit 0
fi

if [ "$action" = "uninstall" ]; then
    uninstall_theme
    uninstall_splash
    uninstall_plugin
else
    running="$(ps -A -o comm= 2>/dev/null | grep -Eiw 'vesktop|discord|discordcanary|discordptb|equibop|dorion|legcord|goofcord' | sort -u | tr '\n' ' ' || true)"
    if [ -n "$running" ]; then
        echo "Discord is running: $running" >&2
        echo "Close it completely (also from the tray) and run this again." >&2
        echo "Nothing has been changed: a running client keeps the old plugin in memory" >&2
        echo "and rewrites its settings on exit." >&2
        exit 1
    fi
    install_theme
    install_splash
    if [ "$plugin" -eq 1 ]; then install_plugin; fi
fi

echo
echo "Done. Fully close Discord (also from the tray) and open it again."
