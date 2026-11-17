#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCOPE = (
    '[class*="toolbar_"]', '[class*="panels_"]', '[class*="channelTextArea_"]',
    '[class*="buttonsInner_"]', '[class*="headerActions_"]', '[class*="upperContainer_"]',
)
BUTTON = ':is(button, [role="button"], [role="switch"])'

BUTTONS = [
    ("thread", ["Hilos", "Threads", "Crear hilo", "Create Thread"]),
    ("bell", ["Ajustes de notificaciones", "Notification Settings"]),
    ("pin", ["Mensajes fijados", "Pinned Messages", "Fijar mensaje", "Pin Message"]),
    ("members", ["lista de miembros", "Member List"]),
    ("inbox", ["Bandeja de entrada", "Inbox"]),
    ("help", ["Ayuda", "Help"]),
    ("phone", ["Iniciar llamada de voz", "Start Voice Call"]),
    ("camera", ["Iniciar videollamada", "Start Video Call", "Encender cámara", "Turn On Camera", "Apagar cámara", "Turn Off Camera"]),
    ("user", ["perfil de usuario", "User Profile"]),
    ("plus", ["Añadir amigos a MD", "Add Friends to DM", "Crear MD", "Create DM", "Subir un archivo", "Upload a file"]),
    ("mic", ["Silenciar", "Mute"]),
    ("mic-off", ["Activar micrófono", "Unmute"]),
    ("headphones", ["Ensordecer", "Deafen"]),
    ("headphones-off", ["Activar audio", "Undeafen"]),
    ("settings", ["Ajustes de usuario", "User Settings"]),
    ("phone-off", ["Desconectar", "Disconnect"]),
    ("screen", ["Compartir pantalla", "Share Your Screen"]),
    ("gift", ["Enviar un regalo", "Send a gift"]),
    ("gif", ["selector de GIF", "GIF picker"]),
    ("sticker", ["selector de sticker", "sticker picker"]),
    ("emoji", ["Agregar emoji", "Seleccionar emoji", "Select emoji"]),
    ("spark", ["Apps"]),
    ("send", ["Enviar mensaje", "Send Message"]),
    ("react", ["Añadir reacción", "Add Reaction"]),
    ("reply", ["Responder", "Reply"]),
    ("edit", ["Editar", "Edit"]),
    ("arrow-right", ["Reenviar", "Forward"]),
    ("more", ["Más", "More"]),
    ("trash", ["Eliminar", "Delete"]),
    ("copy", ["Copiar", "Copy"]),
    ("close", ["Cerrar", "Close"]),
    ("plus", ["Más opciones de mensajes", "More message options"]),
]

# Discord draws each icon as an SVG whose first path is stable across languages,
# so the start of that path identifies the icon wherever it appears.
SIGNATURES = [
    ("volume", ["M12 3a1 1 0 0 0-1-1h-.06a1 1 0 0 0"]),
    ("chevron-down", ["M5.3 9.3a1 1 0 0 1 1.4 0l5.3 5.29"]),
    ("chevron-right", ["M9.3 5.3a1 1 0 0 0 0 1.4l5.29 5.3-", "M8.3 3.3a1 1 0 0 0 0 1.4l7.29 7.3-"]),
    ("hash", ["M10.99 3.16A1 1 0 1 0 9 2.84L8.15"]),
    ("hash-lock", ["M16 4h.5v-.5a2.5 2.5 0 0 1 5 0V4h."]),
    ("folder", ["M2 5a3 3 0 0 1 3-3h3.93a2 2 0 0 1"]),
    ("chat", ["M12 22a10 10 0 1 0-8.45-4.64c.13.1", "M19.33 13.01c.28-.03.58.02.84.15l3"]),
    ("more-vertical", ["M10 4a2 2 0 1 0 4 0 2 2 0 0 0-4 0Z"]),
    ("more", ["M4 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"]),
    ("plus", ["M13 5a1 1 0 1 0-2 0v6H5a1 1 0 1 0", "M13 3a1 1 0 1 0-2 0v8H3a1 1 0 1 0"]),
    ("gamepad", ["M20.97 4.06c0 .18.08.35.24.43.55.2", "M15.02 13.43c-.25.1-.5.2-.75.35a3."]),
    ("members", ["M14.5 8a3 3 0 1 0-2.7-4.3c-.2.4.06"]),
    ("settings", ["M10.56 1.1c-.46.05-.7.53-.64.98.18"]),
    ("music", ["M8.65 1.51A2 2 0 0 0 6 3.41v9.88A3"]),
    ("reply", ["M2.3 7.3a1 1 0 0 0 0 1.4l5 5a1 1 0"]),
    ("forward", ["M21.7 7.3a1 1 0 0 1 0 1.4l-5 5a1 1"]),
    ("search", ["M15.62 17.03a9 9 0 1 1 1.41-1.41l4"]),
    ("check", ["M19.06 6.94a1.5 1.5 0 0 1 0 2.12l-"]),
    ("friends", ["M13 10a4 4 0 1 0 0-8 4 4 0 0 0 0 8"]),
    ("user", ["M12 10a4 4 0 1 0 0-8 4 4 0 0 0 0 8"]),
    ("arrow-left", ["M3.3 11.3a1 1 0 0 0 0 1.4l5 5a1 1"]),
    ("arrow-right", ["M20.7 12.7a1 1 0 0 0 0-1.4l-5-5a1"]),
    ("inbox", ["M5 2a3 3 0 0 0-3 3v14a3 3 0 0 0 3"]),
    ("screen", ["M5 2a3 3 0 0 0-3 3v8a3 3 0 0 0 3 3", "M4 4a3 3 0 0 0-3 3v10a3 3 0 0 0 3"]),
    ("compass", ["M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4"]),
    ("pin", ["M19.38 11.38a3 3 0 0 0 4.24 0l.03-"]),
    ("boost", ["M11.02 1.36c.56-.48 1.4-.48 1.96 0"]),
    ("thread", ["M12 2.81a1 1 0 0 1 0-1.41l.36-.36a"]),
    ("id", ["M15.3 14.48c-.46.45-1.08.67-1.86.6"]),
    ("calendar", ["M7 1a1 1 0 0 1 1 1v.75c0 .14.11.25"]),
    ("browse", ["M18.5 23c.88 0 1.7-.25 2.4-.69l1.4"]),
    ("book", ["M15 2a3 3 0 0 1 3 3v12H5.5a1.5 1.5"]),
    ("user-plus", ["M19 14a1 1 0 0 1 1 1v3h3a1 1 0 0 1", "M19 14a1 1 0 0 1 1 1v3h3a1 1 0 1 1"]),
    ("forum", ["M18.91 12.98a5.45 5.45 0 0 1 2.18"]),
    ("bell-off", ["M1.3 21.3a1 1 0 1 0 1.4 1.4l20-20a"]),
    ("bell", ["M9.7 2.89c.18-.07.32-.24.37-.43a2"]),
    ("close", ["M17.3 18.7a1 1 0 0 0 1.4-1.4L13.42", "M19.3 20.7a1 1 0 0 0 1.4-1.4L13.42"]),
    ("download", ["M12 2a1 1 0 0 1 1 1v10.59l3.3-3.3a", "M12 2C12.2652 2 12.5196 2.10536 12"]),
    ("trophy", ["M8 20a1 1 0 0 0-1 1v.5c0 .28.22.5."]),
    ("flame", ["M3 14a9 9 0 1 0 18 0c0-2.63-.61-5."]),
    ("spark", ["M16.23 12c0 1.29-.95 2.25-2.22 2.2", "M22.95 11.05a1 1 0 0 1 1 1 11.5 11"]),
    ("link", ["M16.32 14.72a1 1 0 0 1 0-1.41l2.51"]),
    ("shop", ["M2.63 4.19A3 3 0 0 1 5.53 2H7a1 1"]),
    ("missions", ["M7.5 21.7a8.95 8.95 0 0 1 9 0 1 1"]),
    ("external", ["M8 5a1 1 0 0 0 0 2h7.59L5.29 17.3a"]),
    ("star", ["M10.81 2.86c.38-1.15 2-1.15 2.38 0"]),
    ("edit", ["m13.96 5.46 4.58 4.58a1 1 0 0 0 1."]),
    ("shield", ["M20.3 5.41h-.39c-.84 0-1.52-.65-1."]),
    ("plug", ["M18.559 12.8227C17.7884 13.4957 16"]),
    ("brush", ["M15.35 7.24C15.9 6.67 16 5.8 16 5a", "M19 16h-5a2 2 0 0 0-2 2v2c0 1.66-1"]),
    ("cloud", ["M16.8333 19H5.16667C3.16667 19 1.5"]),
    ("sync", ["M21 2.01232C21.2652 2.01232 21.519"]),
    ("wrench", ["M7.79997 15.7699C8.49996 16.1999 8"]),
    ("gift", ["M4 6a4 4 0 0 1 4-4h.09c1.8 0 3.39"]),
    ("card", ["M0 6c0-1.1 1.07-2 2.4-2h19.2c1.32"]),
    ("mic", ["M12 2a4 4 0 0 0-4 4v4a4 4 0 0 0 8"]),
    ("globe", ["M11 2a1 1 0 1 0-2 0v1H3a1 1 0 0 0"]),
    ("code", ["M9.6 7.8 4 12l5.6 4.2a1 1 0 0 1 .4"]),
    ("logout", ["M9 12a1 1 0 0 1 1 1v2a1 1 0 1 1-2"]),
    ("react", ["M12 1a11 11 0 0 1 9.16 17.08 2 2 0"]),
    ("copy", ["M3 16a1 1 0 0 1-1-1v-5a8 8 0 0 1 8"]),
    ("bookmark", ["M17 4H7a1 1 0 0 0-1 1v13.74l3.99-3"]),
    ("apps", ["M2.06 7.61c-.25.95.31 1.92 1.26 2.", "M15 2a1 1 0 0 1 1-1h6a1 1 0 0 1 1"]),
    ("unread", ["M12.93 21.96c.25-.03.43-.23.47-.47"]),
    ("trash", ["M14.25 1c.41 0 .75.34.75.75V3h5.25", "M12.79 20.97a1 1 0 0 1 .17 1.99 11", "M10.67 1.33a9.33 9.33 0 0 1 8.05 1"]),
    ("flag", ["M3 1a1 1 0 0 1 1 1v.82l8.67-1.45A2"]),
]

STATUS = [
    ("status-online", "online"),
    ("status-idle", "idle"),
    ("status-dnd", "dnd"),
    ("status-offline", "offline"),
    ("status-streaming", "streaming"),
    ("status-mobile", "online-mobile"),
]

CHANNELS = [
    ("volume", ["voz", "voice", "escenario", "stage"]),
    ("announcement", ["anuncio", "announcement"]),
    ("forum", ["foro", "forum"]),
]

LINKS = [
    ("friends", 'a[href="/channels/@me"]'),
    ("spark", 'a[href="/store"]'),
    ("shop", 'a[href="/shop"]'),
    ("missions", 'a[href^="/quest"]'),
]

def url(name):
    assert (ROOT / "assets" / "icons" / f"{name}.svg").exists(), name
    return f'url("../assets/icons/{name}.svg")'

def labels(items):
    return ", ".join(f'[aria-label*="{label}" i]' for label in items)

scope = "#app-mount :is(\n    " + ",\n    ".join(SCOPE) + "\n)"
out = [
    "/* pixel icon set. Generated by scripts/generate-icon-css.py */",
    "",
    f"{scope} {BUTTON}[aria-label]::before {{",
    '    content: "";',
    "    display: var(--rl-icon-display, none);",
    "    flex: 0 0 auto;",
    "    width: var(--rl-icon-size, 16px);",
    "    height: var(--rl-icon-size, 16px);",
    "    background: currentColor;",
    "    -webkit-mask: var(--rl-icon) center / contain no-repeat;",
    "    mask: var(--rl-icon) center / contain no-repeat;",
    "}",
    "",
    "@container style(--rl-icon-display: inline-block) {",
    '    #app-mount :is(svg, [class*="lottieIcon_"], [class*="spriteContainer_"]) {',
    "        display: none !important;",
    "    }",
    "}",
    "",
]
for name, items in BUTTONS:
    out += [
        f"{scope} {BUTTON}:is({labels(items)}) {{",
        f"    --rl-icon: {url(name)};",
        "    --rl-icon-display: inline-block;",
        "}",
        "",
    ]

chan = '#app-mount a[data-list-item-id^="channels___"]'
out += [
    f'{chan} [class*="iconContainer_"] > svg {{',
    "    display: none !important;",
    "}",
    "",
    f'{chan} [class*="iconContainer_"]::before {{',
    '    content: "";',
    "    display: block;",
    "    width: 16px;",
    "    height: 16px;",
    "    background: currentColor;",
    f"    -webkit-mask: var(--rl-channel-icon, {url('hash')}) center / contain no-repeat;",
    f"    mask: var(--rl-channel-icon, {url('hash')}) center / contain no-repeat;",
    "}",
    "",
]
for name, items in CHANNELS:
    out += [f"{chan}:is({labels(items)}) {{", f"    --rl-channel-icon: {url(name)};", "}", ""]

nav = '#app-mount [class*="privateChannels_"]'
out += [
    f'{nav} svg[class*="linkButtonIcon_"] {{',
    "    display: none !important;",
    "}",
    "",
    f'{nav} [class*="avatar_"]:has(> svg[class*="linkButtonIcon_"])::before {{',
    '    content: "";',
    "    display: block;",
    "    width: 16px;",
    "    height: 16px;",
    "    margin: auto;",
    "    background: currentColor;",
    f"    -webkit-mask: var(--rl-link-icon, {url('diamond')}) center / contain no-repeat;",
    f"    mask: var(--rl-link-icon, {url('diamond')}) center / contain no-repeat;",
    "}",
    "",
]
for name, sel in LINKS:
    out += [f"{nav} {sel} {{", f"    --rl-link-icon: {url(name)};", "}", ""]

def signature(paths):
    return ",\n".join(f'svg:has(> path[d^="{path}"])' for path in paths)

every = [path for _, paths in SIGNATURES for path in paths]
out += [
    f"#app-mount :is(\n{signature(every)}\n) {{",
    "    background: currentColor !important;",
    "    -webkit-mask: var(--rl-glyph) center / contain no-repeat !important;",
    "    mask: var(--rl-glyph) center / contain no-repeat !important;",
    "}",
    "",
    f"#app-mount :is(\n{signature(every)}\n) > * {{",
    "    visibility: hidden;",
    "}",
    "",
]
for name, paths in SIGNATURES:
    out += [f"#app-mount :is(\n{signature(paths)}\n) {{", f"    --rl-glyph: {url(name)};", "}", ""]

for name, state in STATUS:
    out += [
        f'#app-mount svg[class*="mask_"] rect[mask="url(#svg-mask-status-{state})"] {{',
        f"    -webkit-mask: {url(name)} center / contain no-repeat !important;",
        f"    mask: {url(name)} center / contain no-repeat !important;",
        "}",
        "",
    ]

out += [
    '#app-mount [class*="rtcConnectionStatus"] [class*="ping_"] svg > * {',
    "    visibility: hidden;",
    "}",
    "",
    '#app-mount [class*="rtcConnectionStatus"] [class*="ping_"] svg {',
    "    background: currentColor;",
    f"    -webkit-mask: {url('signal-3')} center / contain no-repeat;",
    f"    mask: {url('signal-3')} center / contain no-repeat;",
    "}",
    "",
]

head, body = out[:2], out[2:]
while body and not body[-1]:
    body.pop()
wrapped = ["@container not style(--rl-icons: off) {"] + [("    " + line if line else line) for line in body] + ["}"]
(ROOT / "src" / "14-icons.css").write_text("\n".join(head + wrapped) + "\n")
print("wrote src/14-icons.css")
