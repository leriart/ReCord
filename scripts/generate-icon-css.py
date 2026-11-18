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
    ("chevron-down", ["M3.3 8.3a1 1 0 0 1 1.4 0l7.3 7.29"]),
    ("chevron-up", ["M5.3 14.7a1 1 0 0 0 1.4 0L12 9.42l"]),
    ("settings", ["M22 5a1 1 0 0 1-1 1h-8.2a2.5 2.5 0"]),
    ("play", ["M9.25 3.35C7.87 2.45 6 3.38 6 4.96"]),
    ("check", ["M21.7 5.3a1 1 0 0 1 0 1.4l-12 12a1"]),
    ("attach", ["M13.82 21.7c.17.05.14.3-.04.3H6a4"]),
    ("poll", ["M2 5c0-1.1.9-2 2-2h16a2 2 0 1 1 0"]),
    ("info", ["M2 19V5a3 3 0 0 1 3-3h14a3 3 0 0 1"]),
    ("eye", ["M15.56 11.77c.2-.1.44.02.44.23a4 4"]),
    ("shield", ["M17.05 8.76a4.7 4.7 0 0 1-1.29-.88"]),
    ("lock", ["M6 9h1V6a5 5 0 0 1 10 0v3h1a3 3 0"]),
    ("emoji", ["M8.49999 3.7998L4.85999 7.4398V12."]),
    ("check", ["M16.7 8.7a1 1 0 0 0-1.4-1.4l-3.26"]),
    ("phone", ["M2 7.4A5.4 5.4 0 0 1 7.4 2c.36 0 ."]),
    ("user", ["M23 12.38c-.02.38-.45.58-.78.4a6.9"]),
    ("external", ["M14 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1"]),
    ("image", ["M2 5a3 3 0 0 1 3-3h14a3 3 0 0 1 3"]),
    ("sticker", ["M6 2h12a4 4 0 0 1 4 4v7.5a.5.5 0 0"]),
    ("home", ["m2.4 8.4 8.38-6.46a2 2 0 0 1 2.44"]),
    ("sync", ["M21 2a1 1 0 0 1 1 1v6a1 1 0 0 1-1"]),
    ("brush", ["m15.93 3.04-1.82 1.83-.58-.58a2.74"]),
    ("logout", ["M18.46 20.9a12.65 12.65 0 0 1-1.46"]),
]


# Discord ships its icon set as named components in the web bundle. These are the
# first-path signatures of the current client (web build 8414378, 2026-11-17),
# mapped to the pixel set above. They are checked after the legacy signatures so a
# path that changed shape still lands on the right pixel glyph. Paths shared by
# several icons (lock, warning, spoiler) resolve to the same pixel glyph on purpose.
CURRENT_SIGNATURES = [
    ('announcement', ["M19.56 2a3 3 0 0 0-2.46 1.28 3.85 3.85 0 0"]),
    ('apps', ["M2.06 7.61c-.25.95.31 1.92 1.26 2.18l4.3 1", "M15 11a2 2 0 0 1-2-2V4c0-1.1.9-2 2-2h5a2 2"]),
    ('arrow-down', ["M12.7 20.7a1 1 0 0 1-1.4 0l-5-5a1 1 0 1 1 "]),
    ('arrow-left', ["M3.3 11.3a1 1 0 0 0 0 1.4l5 5a1 1 0 0 0 1."]),
    ('arrow-right', ["M20.7 12.7a1 1 0 0 0 0-1.4l-8-8a1 1 0 1 0-", "M20.7 12.7a1 1 0 0 0 0-1.4l-5-5a1 1 0 1 0-"]),
    ('at', ["M16.44 6.96c.29 0 .51.25.47.54l-.82 6.34c-"]),
    ('attach', ["M10.57 4.01a6.97 6.97 0 0 1 9.86 0l.54.55a"]),
    ('bell', ["M9.7 2.89c.18-.07.32-.24.37-.43a2 2 0 0 1 "]),
    ('bell-off', ["M1.3 21.3a1 1 0 1 0 1.4 1.4l20-20a1 1 0 0 0-1.4-1.4l-20 20ZM3.13 1"]),
    ('bold', ["M5.42 22a.9.9 0 0 1-.91-.9V2.9c0-.5.4-.9.9"]),
    ('book', ["M15 2a3 3 0 0 1 3 3v12H5.5a1.5 1.5 0 0 0 0"]),
    ('bookmark', ["M4 5a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v16a1 1"]),
    ('boost', ["M11.02 1.36c.56-.48 1.4-.48 1.96 0l6.48 5.", "M10.95 1.4a1.59 1.59 0 0 1 2.1 0l4.9 4A3.3"]),
    ('bot', ["M19.73 4.87a18.2 18.2 0 0 0-4.6-1.44c-.21.", "M7.89 13.46a1 1 0 0 1-1.78-.9L7 13l-.9-.45"]),
    ('browse', ["M18.5 23c.88 0 1.7-.25 2.4-.69l1.4 1.4a1 1"]),
    ('brush', ["M21.7 2.3a1 1 0 0 1 0 1.4l-4.92 4.93c-.12.", "M19 16h-5a2 2 0 0 0-2 2v2c0 1.66-1.37 3.04"]),
    ('bug', ["M9.54 3.28a3 3 0 0 0-.37.74c-.19.52.28.98."]),
    ('calendar', ["M7 1a1 1 0 0 1 1 1v.75c0 .14.11.25.25.25h7"]),
    ('camera', ["M15 13a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"]),
    ('chat', ["M12.2 22c.5-.01.66-.84.37-1.24A3 3 0 0 1 1", "M12.66 21.98c.4-.03.56-.51.28-.8l-.06-.06a", "M12 22a10 10 0 1 0-8.45-4.64c.13.19.11.44-", "M19 14a1 1 0 0 1 1 1v3h3a1 1 0 1 1 0 2h-3v", "M22 12a10 10 0 0 1-10 10H2.2a1 1 0 0 1-.75", "M3.11 8H6v10.82c0 .86.37 1.68 1 2.27.46.43"]),
    ('check', ["M22.06 4.94a1.5 1.5 0 0 1 0 2.12l-12 12a1.", "M21.7 5.3a1 1 0 0 1 0 1.4l-12 12a1 1 0 0 1", "M19.06 6.94a1.5 1.5 0 0 1 0 2.12l-8 8a1.5 ", "M18.7 7.3a1 1 0 0 1 0 1.4l-8 8a1 1 0 0 1-1", "M12 23a11 11 0 1 0 0-22 11 11 0 0 0 0 22Zm5.7"]),
    ('chevron-down', ["M3.3 8.3a1 1 0 0 1 1.4 0l7.3 7.29 7.3-7.3a", "M5.3 9.3a1 1 0 0 1 1.4 0l5.3 5.29 5.3-5.3a"]),
    ('chevron-left', ["M14.7 5.3a1 1 0 0 1 0 1.4L9.42 12l5.3 5.3a"]),
    ('chevron-right', ["M9.3 5.3a1 1 0 0 0 0 1.4l5.29 5.3-5.3 5.3a"]),
    ('chevron-up', ["M3.3 15.7a1 1 0 0 0 1.4 0L12 8.42l7.3 7.3a", "M5.3 14.7a1 1 0 0 0 1.4 0L12 9.42l5.3 5.3a"]),
    ('clips', ["M15.74 5.74a.5.5 0 0 0 .54.7l5.01-.88a.5.5"]),
    ('clock', ["M12 23a11 11 0 1 0 0-22 11 11 0 0 0 0 22Zm1-18", "M9.1 8.85A.5.5 0 0 1 9.45 8h5.1a.5.5 0 0 1", "M12 22a9 9 0 0 0 7.03-14.62l.68-.67a1 1 0 "]),
    ('close', ["M12 23a11 11 0 1 0 0-22 11 11 0 0 0 0 22Zm4.7", "M8 6a2 2 0 0 1-2 2H3a1 1 0 0 0 0 2h3a4 4 0", "M15 4v3.59l5.3-5.3a1 1 0 1 1 1.4 1.42L16.4", "M19.3 20.7a1 1 0 0 0 1.4-1.4L13.42 12l7.3-", "M13.86 10.47 21.15 2h-1.73l-6.33 7.35L8.04", "M17.3 18.7a1 1 0 0 0 1.4-1.4L13.42 12l5.3-"]),
    ('cloud', ["M14 4a5 5 0 0 1 5 5v.2A5.5 5.5 0 0 1 17.5 "]),
    ('code', ["M9.6 7.8 4 12l5.6 4.2a1 1 0 0 1 .4.8v1.98c", "M9.5 11.87a1 1 0 0 1 1.55-.83l3.2 2.13a1 1"]),
    ('compass', ["M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z", "M11 3a1 1 0 1 1 2 0v2h5.75c.16 0 .3.07.4.2"]),
    ('copy', ["M3 16a1 1 0 0 1-1-1v-5a8 8 0 0 1 8-8h5a1 1"]),
    ('crop', ["M7 2a1 1 0 0 0-2 0v3H2a1 1 0 1 0 0 2h3v8a4"]),
    ('crown', ["M5 18a1 1 0 0 0-1 1 3 3 0 0 0 3 3h10a3 3 0"]),
    ('deny', ["M21.76.83a5.02 5.02 0 0 1 .78 7.7 5 5 0 0 "]),
    ('dice', ["M8.18 14.82c.5-.11 1.07.45 1.29 1.27.21.81"]),
    ('download', ["M12 2a1 1 0 0 1 1 1v10.59l3.3-3.3a1 1 0 1 "]),
    ('drag', ["M6 4a2 2 0 1 0 4 0 2 2 0 0 0-4 0Zm0 8a2 2 "]),
    ('edit', ["m13.96 5.46 4.58 4.58a1 1 0 0 0 1.42 0l1.3"]),
    ('emoji', ["M12 23a11 11 0 1 0 0-22 11 11 0 0 0 0 22ZM6.5", "M12 1a11 11 0 1 0 0 22 11 11 0 0 0 0-22Zm5"]),
    ('envelope', ["M1.16 5.02c-.1.28.04.58.29.74l10.27 6.85a."]),
    ('external', ["M4 6c0-1.1.9-2 2-2h3a1 1 0 0 0 0-2H6a4 4 0", "M7 4a1 1 0 0 0 0 2h9.59L4.29 18.3a1 1 0 1 ", "M8 5a1 1 0 0 0 0 2h7.59L5.29 17.3a1 1 0 1 ", "M14 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v6a1 1 ", "M15 2a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v6a1 1 "]),
    ('eye', ["M15.56 11.77c.2-.1.44.02.44.23a4 4 0 1 1-4", "M22.52 13.17c-.2.41-.87.35-1.15 0a3.02 3.0"]),
    ('eye-off', ["M1.3 21.3a1 1 0 1 0 1.4 1.4l20-20a1 1 0 0 0-1.4-1.4l-20 20ZM3.16 1"]),
    ('file', ["M21.27 12.38c.35.11.73-.13.73-.5V10.5a.5.5", "M5 2a3 3 0 0 0-3 3v14a3 3 0 0 0 3 3h14a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3H5Zm1 4a", "M10.07 9.4a.6.6 0 0 0-1.14 0l-.1.25a2 2 0 "]),
    ('flag', ["M5.1 1a2.1 2.1 0 0 1 1.8 3.14h14.05c.84 0 ", "M3 1a1 1 0 0 1 1 1v.82l8.67-1.45A2 2 0 0 1"]),
    ('flame', ["M3 14a9 9 0 1 0 18 0c0-2.63-.61-5.22-1.79-"]),
    ('folder', ["M2 5a3 3 0 0 1 3-3h3.93a2 2 0 0 1 1.66.9L1"]),
    ('food', ["M7 1a1 1 0 0 0-1 1v.2c0 .79-.4 1.53-1.05 1"]),
    ('forum', ["M18.91 12.98a5.45 5.45 0 0 1 2.18 6.2c-.1."]),
    ('forward', ["M21.7 7.3a1 1 0 0 1 0 1.4l-5 5a1 1 0 0 1-1"]),
    ('friends', ["M13 10a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z"]),
    ('gamepad', ["M22 4v1.51a6 6 0 0 1-1.76 4.25l-4.1 4.1a.5", "M15.5 18.08a.74.74 0 0 1 1.04 1.04l-.57.58", "M20.97 4.06c0 .18.08.35.24.43.55.28.9.82 1", "M23.79 16.92c-.47.59-1.62 1.01-1.62 1.01L1", "M6.23 2 2 17.77 17.77 22 22 6.23 6.23 2Zm7", "M4.5 3.92A11.03 11.03 0 0 1 11.99 1v.02a11", "M24 5.7c0-1.54-.2-2.66-.34-3.23C23.35 1.17", "M5 2a3 3 0 0 0-3 3v14a3 3 0 0 0 3 3h14a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3H5Zm6.8", "M10.9 22.95c-1.7-.16-3.4-.77-4.88-1.73-1.2"]),
    ('gif', ["M5 2a3 3 0 0 0-3 3v14a3 3 0 0 0 3 3h14a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3H5Zm2.1"]),
    ('gift', ["M4 6a4 4 0 0 1 4-4h.09c1.8 0 3.39 1.18 3.9"]),
    ('globe', ["M23 12a11 11 0 1 1-22 0 11 11 0 0 1 22 0Zm-4.1"]),
    ('hash', ["M10.99 3.16A1 1 0 1 0 9 2.84L8.15 8H4a1 1 ", "M9.02 2.84a1 1 0 0 1 1.97.33L10.2 8h2.1a.7"]),
    ('hash-lock', ["M16 4h.5v-.5a2.5 2.5 0 0 1 5 0V4h.5a1 1 0 ", "M16.48 13.71a1.1 1.1 0 0 1 2.04 0l.46 1.24"]),
    ('headphones', ["M12 3a9 9 0 0 0-8.95 10h1.87a5 5 0 0 1 4.1"]),
    ('headphones-off', ["M22.7 2.7a1 1 0 0 0-1.4-1.4l-20 20a1 1 0 1 0 1.4 1.4l20-20ZM17.0"]),
    ('heart', ["M12.47 21.73a.92.92 0 0 1-.94 0C9.43 20.48", "M12 8.07 10.6 6.7A5 5 0 0 0 6.75 5 3.75 3."]),
    ('help', ["M12 23a11 11 0 1 0 0-22 11 11 0 0 0 0 22Zm-.2"]),
    ('home', ["m2.4 8.4 8.38-6.46a2 2 0 0 1 2.44 0l8.39 6"]),
    ('id', ["M15.3 14.48c-.46.45-1.08.67-1.86.67h-1.39V"]),
    ('image', ["M2 5a3 3 0 0 1 3-3h14a3 3 0 0 1 3 3v14a3 3", "M2 5a3 3 0 0 1 3-3h14a3 3 0 0 1 3 3v8.03c0", "M2 5a3 3 0 0 1 3-3h14a3 3 0 0 1 3 3v8.67c0", "M5 2a3 3 0 0 0-3 3v14a3 3 0 0 0 3 3h6.49c.", "M4 8v7.5a.5.5 0 0 1-.5.5H3a1 1 0 0 1-1-1V8"]),
    ('inbox', ["M5 2a3 3 0 0 0-3 3v14a3 3 0 0 0 3 3h14a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3H5ZM4 "]),
    ('info', ["M23 12a11 11 0 1 1-22 0 11 11 0 0 1 22 0Zm-9.5"]),
    ('italic', ["M8.87 2.31A.5.5 0 0 1 9.34 2h10.92c.36 0 ."]),
    ('leaf', ["M9.8 14.6c-.45.31-.9.6-1.37.89l-.02.01-1.1"]),
    ('link', ["M16.32 14.72a1 1 0 0 1 0-1.41l2.51-2.51a3."]),
    ('lock', ["M6 9h1V6a5 5 0 0 1 10 0v3h1a3 3 0 0 1 3 3v"]),
    ('logout', ["M9 12a1 1 0 0 1 1 1v2a1 1 0 1 1-2 0v-2a1 1", "M9 10a1 1 0 0 1 1 1v2a1 1 0 0 1-2 0v-2a1 1"]),
    ('members', ["M3.18 3.12c.49.24.73.79.66 1.32-.27 2 .1 4", "M1.59 3.78c.22-.66.98-.97 1.6-.66.48.24.73", "M14.5 8a3 3 0 1 0-2.7-4.3c-.2.4.06.86.44 1"]),
    ('mic', ["M12 2a4 4 0 0 0-4 4v4a4 4 0 0 0 8 0V6a4 4 "]),
    ('mic-off', ["m2.7 22.7 20-20a1 1 0 0 0-1.4-1.4l-20 20a1"]),
    ('minus', ["M22 12a1 1 0 0 1-1 1H3a1 1 0 1 1 0-2h18a1 "]),
    ('missions', ["M11.76 20.14c.12-.12.3-.15.46-.1.3.1.6.14.", "M7.5 21.7a8.95 8.95 0 0 1 9 0 1 1 0 0 0 1-"]),
    ('more', ["M4 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm10-2a2 "]),
    ('more-vertical', ["M10 4a2 2 0 1 0 4 0 2 2 0 0 0-4 0Zm2 10a2 "]),
    ('music', ["M8.65 1.51A2 2 0 0 0 6 3.41v9.88A3.98 3.98"]),
    ('pause', ["M6 4a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h3a1 1 "]),
    ('phone', ["M5 4a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v16a3 3 ", "M2 7.4A5.4 5.4 0 0 1 7.4 2c.36 0 .7.22.83."]),
    ('pin', ["M19.38 11.38a3 3 0 0 0 4.24 0l.03-.03a.5.5"]),
    ('play', ["M12 23a11 11 0 1 0 0-22 11 11 0 0 0 0 22ZM9 8", "M9.25 3.35C7.87 2.45 6 3.38 6 4.96v14.08c0"]),
    ('plug', ["M15 4a1 1 0 0 0-.95 1.32l.9 2.68h-4.6l-.92", "M11.62 2.08a1 1 0 0 1 1.09.21l5 5a1 1 0 0 ", "M13 7.83a3 3 0 1 0-2 0V11H8a4 4 0 0 0-4 4v"]),
    ('plus', ["M12 23a11 11 0 1 0 0-22 11 11 0 0 0 0 22Zm0-1", "M13 5a1 1 0 1 0-2 0v6H5a1 1 0 1 0 0 2h6v6a", "M13 6a1 1 0 1 0-2 0v5H6a1 1 0 1 0 0 2h5v5a"]),
    ('poll', ["M2 19V5a3 3 0 0 1 3-3h14a3 3 0 0 1 3 3v14a"]),
    ('quote', ["M2.35 19.44A4.75 4.75 0 0 0 6.07 21c1.43 0"]),
    ('react', ["M14.61 2.26c.25-.34.16-.92-.25-1A11 11 0 0"]),
    ('reply', ["M2.3 7.3a1 1 0 0 0 0 1.4l5 5a1 1 0 0 0 1.4"]),
    ('save', ["M16.7 8.68a.93.93 0 0 1 1.07-.63c.51.1.84."]),
    ('screen', ["M12 3a9 9 0 0 0-7.47 14.03c.28.41.28.97-.0", "M2 5a3 3 0 0 1 3-3h14a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3V5Zm16 ", "M5 2a3 3 0 0 0-3 3v8a3 3 0 0 0 3 3h14a3 3 ", "M4 3a3 3 0 0 0-3 3v9a3 3 0 0 0 3 3h16a3 3 ", "M4 4a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h11a3 3", "M4 4a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h8.5a.5"]),
    ('screen-off', ["M15.46 15.46a5 5 0 0 1 7.07 0 5 5 0 0 1-7.", "M2 5a3 3 0 0 1 3-3h14a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3V5Zm6.3", "M22.7 2.7a1 1 0 0 0-1.4-1.4l-20 20a1 1 0 1 0 1.4 1.4l20-20ZM9.2"]),
    ('search', ["M15.62 17.03a9 9 0 1 1 1.41-1.41l4.68 4.67"]),
    ('send', ["M6.6 10.02 14 11.4a.6.6 0 0 1 0 1.18L6.6 1"]),
    ('server', ["M10.55 4.4c.13-.24.1-.54-.12-.71L8.6 2.24a"]),
    ('settings', ["M10.56 1.1c-.46.05-.7.53-.64.98.18 1.16-.1"]),
    ('shield', ["M5.26 12.45c.1.03.18.08.25.14l.52.44 5.26 ", "M17.05 8.76a4.7 4.7 0 0 1-1.29-.88c-.36-.3", "M20.3 5.41h-.39c-.84 0-1.52-.65-1.52-1.46v", "M2 20.59V19.4a1 1 0 0 1 .3-.7l2.4-2.42a1 1"]),
    ('shop', ["M6.69 2A3 3 0 0 0 3.7 4.67l-.33 3A3 3 0 0 ", "M10.41 3.59 11.6 2.4a2 2 0 0 1 2.82 0l1.3 ", "M2.63 4.19A3 3 0 0 1 5.53 2H7a1 1 0 0 1 1 "]),
    ('signal-0', ["M2 3a1 1 0 0 1 1-1c6.92 0 12.97 3.7 16.3 9"]),
    ('signal-1', ["M2 13a1 1 0 0 1 1-1 9 9 0 0 1 9 9 1 1 0 1 "]),
    ('signal-2', ["M3 7a1 1 0 0 0 0 2 12 12 0 0 1 12 12 1 1 0"]),
    ('signal-3', ["M2 3a1 1 0 0 1 1-1 19 19 0 0 1 19 19 1 1 0", "M17.38 21c.61 0 1.23-.18 1.7-.58a11 11 0 1"]),
    ('slash', ["M23 12a11 11 0 1 1-22 0 11 11 0 0 1 22 0Zm-2 0", "M5 2a3 3 0 0 0-3 3v14a3 3 0 0 0 3 3h14a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3H5Zm12.7", "M19.12 2a.5.5 0 0 1 .43.76L8.22 21.64a.75."]),
    ('soundboard', ["M14.24 1.03a1 1 0 0 1 .73 1.21l-1 4a1 1 0 "]),
    ('spark', ["M11.45 6.05c.3-.1.6.09.72.38l.04.09c.26.59", "M5.86 13.27a.89.89 0 0 1 1.28 0l.75.77a.9.9 0 0 0 .54.26l1.06.12c.5.06.85.52.8 1.02l-.13 1.08c-.02.2.03.42.14.6l.56.92c.27.43.14 1-.28 1.26l-.9.58a.92.92 0 0 0-.37.48l-.36 1.02a.9.9 0 0 1-1.15.57l-1-.36a.89.89 0 0 0-.6 0l-1 .36a.9.9 0 0 1-1.15-.57l-.36-1.02a.92.92 0 0 0-.37-.48l-.9-.58a.93.93 0 0 1-.28-1.26l.56-.93c.11-.17.16-.38.14-.59l-.12-1.08c-.06-.5.3-.96.8-1.02l1.05-.12a.9.9 0 0 0 .54-.26l.75-.77ZM16.48 13.71a1.1 1.1 0 0 1 2.04 0l.46 1.24c.19.5.57.88 1.07 1.07l1.24.46c.95.35.95 1.7 0 2.04l-", "M24 12c0 1.2-1.95 2.1-2.25 3.15-.3 1.05.6 ", "M7.65 21.75a1 1 0 0 0 1.64.96l11.24-9.96a1", "M15.7 12a5.6 5.6 0 0 1 5.67 5.5c0 .57-.09 ", "M12.37 9.04c.25-.26.73-.2 1.06.13L15 10.7c", "M16.23 12c0 1.29-.95 2.25-2.22 2.25A2.18 2", "M11.75 7.57a5.12 5.12 0 0 1-3.86 3.87.42.4", "M18.14 2.8a1.21 1.21 0 0 0-2.28 0l-.5 1.37"]),
    ('stage', ["M19.61 18.25a1.08 1.08 0 0 1-.07-1.33 9 9 ", "M21.92 14.08c.32.27.86.15.93-.26A11 11 0 1"]),
    ('star', ["M11.26 2.86c.38-1.15 2-1.15 2.38 0l1.89 5.", "M10.16 4.06a2.13 2.13 0 0 1 3.68 0l8 13.77", "M10.81 2.86c.38-1.15 2-1.15 2.38 0l1.89 5.", "M2.07 10.94a1.25 1.25 0 0 1 .73-2.25h6.12l", "M17.93 1.51a.74.74 0 0 0-1.41 0l-1.13 3.47"]),
    ('sticker', ["M6 2h12a4 4 0 0 1 4 4v7.5a.5.5 0 0 1-.5.5H"]),
    ('strike', ["M12.1 22.5c-1.8 0-3.3-.37-4.53-1.11A7.95 7"]),
    ('sync', ["M21 2a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1h-6a1 1", "M4 12a8 8 0 0 1 14.93-4H15a1 1 0 1 0 0 2h6"]),
    ('tag', ["M12.24 2a3 3 0 0 0-2.12.88l-8.25 8.25a3 3 "]),
    ('thread', ["M12 2.81a1 1 0 0 1 0-1.41l.36-.36a1 1 0 0 ", "M19 15a2.5 2.5 0 0 1 2.5 2.5v.5h.5a1 1 0 0", "m12.58 18.26-9.55-6.72a1 1 0 0 0-1.3.13l-."]),
    ('trash', ["M14.25 1c.41 0 .75.34.75.75V3h5.25c.41 0 ."]),
    ('trophy', ["M13.76 4.97a1 1 0 0 1-.73-1.21l.5-2a1 1 0 ", "M10.89 11.79A3 3 0 1 0 13.1 6.2a3 3 0 0 0-", "M8 20a1 1 0 0 0-1 1v.5c0 .28.22.5.5.5h9a.5"]),
    ('underline', ["M7.03 16.6c1.18 1.17 2.84 1.76 4.97 1.76s3"]),
    ('upload', ["M13 16V5.41l3.3 3.3a1 1 0 1 0 1.4-1.42l-5-"]),
    ('user', ["M18.46 20.9a12.65 12.65 0 0 1-1.46.9 10.95", "M12 10a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM11.53 "]),
    ('user-plus', ["M11.33 13.68c.41.27.93.27 1.34 0 1.73-1.1 "]),
    ('volume', ["M12 3a1 1 0 0 0-1-1h-.06a1 1 0 0 0-.74.32L5.92 7H3a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h2.92l4.28 4.68a1 1 0 0 0 .74.32H11a1 1 0 0 0 1-1V3ZM15.", "M11 2a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1h-.06a"]),
    ('volume-mute', ["M22.7 2.7a1 1 0 0 0-1.4-1.4l-20 20a1 1 0 1 0 1.4 1.4l20-20ZM15.2", "M12 3a1 1 0 0 0-1-1h-.06a1 1 0 0 0-.74.32L5.92 7H3a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h2.92l4.28 4.68a1 1 0 0 0 .74.32H11a1 1 0 0 0 1-1V3ZM22."]),
    ('warning', ["M18.09 1.63c.4-.7 1.43-.7 1.82 0l3.96 6.9c", "M5.86 13.27a.89.89 0 0 1 1.28 0l.75.77a.9.9 0 0 0 .54.26l1.06.12c.5.06.85.52.8 1.02l-.13 1.08c-.02.2.03.42.14.6l.56.92c.27.43.14 1-.28 1.26l-.9.58a.92.92 0 0 0-.37.48l-.36 1.02a.9.9 0 0 1-1.15.57l-1-.36a.89.89 0 0 0-.6 0l-1 .36a.9.9 0 0 1-1.15-.57l-.36-1.02a.92.92 0 0 0-.37-.48l-.9-.58a.93.93 0 0 1-.28-1.26l.56-.93c.11-.17.16-.38.14-.59l-.12-1.08c-.06-.5.3-.96.8-1.02l1.05-.12a.9.9 0 0 0 .54-.26l.75-.77ZM16.48 13.71a1.1 1.1 0 0 1 2.04 0l.46 1.24c.19.5.57.88 1.07 1.07l1.24.46c.95.35.95 1.7 0 2.05l-", "M12 23a11 11 0 1 0 0-22 11 11 0 0 0 0 22Zm1.44", "M21.65 13.63c.1.17.35.1.35-.1V10.5a.5.5 0 ", "m13.47 1 .07.04c.45.06.9.1 1.35.18.95.17 1", "M10 3.1a2.37 2.37 0 0 1 4 0l8.71 14.75c.84"]),
    ('waveform', ["M7 2a1 1 0 0 0-1 1v18a1 1 0 1 0 2 0V3a1 1 "]),
    ('waveform-off', ["M22.7 2.7a1 1 0 0 0-1.4-1.4l-20 20a1 1 0 1 0 1.4 1.4l20-20ZM6.8"]),
    ('wrench', ["M1.23 21.13a1 1 0 0 1 0-1.41l7.48-7.47c.2-", "M7.8 15.77c.7.43 1.2 1.14 1.2 1.96V21a1 1 "]),
]

def merge_signatures(*tables):
    """Keep table order, letting later tables own a path they share."""
    owner = {}
    for table in tables:
        for name, paths in table:
            for path in paths:
                owner[path] = name
    merged = []
    for table in tables:
        groups = {}
        order = []
        for name, paths in table:
            if name not in groups:
                groups[name] = []
                order.append(name)
            for path in paths:
                if owner[path] == name and path not in groups[name]:
                    groups[name].append(path)
        merged += [(name, groups[name]) for name in order if groups[name]]
    return merged


SIGNATURES = merge_signatures(SIGNATURES, CURRENT_SIGNATURES)

# Discord paints each status as a rect with a per-avatar mask, so the fill color
# is the stable way to tell them apart.
STATUS = [
    ("status-online", "var(--rl-green)", ["#45a366", "#43a25a", "#23a55a"]),
    ("status-idle", "var(--rl-amber)", ["#ffc04e", "#ca9654", "#f0b232"]),
    ("status-dnd", "var(--rl-red)", ["#da3e44", "#d83a42", "#f23f43"]),
    ("status-offline", "var(--rl-offline)", ["#84858d", "#83838b", "#80848e"]),
    ("status-streaming", "var(--rl-purple)", ["#9147ff", "#593695"]),
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

# Voice panel controls are Lottie animations, not SVG paths: camera, screen share,
# activities and soundboard in the action row, plus noise cancellation and
# disconnect in the status row. Mask the animation layer and let the pixel icon
# sit on top. The selectors follow the stable class prefixes and child order.
RTC_ACTION = '#app-mount [class*="container_"]:has(> [class*="connection_"] [class*="voiceButtonsContainer_"]) > [class*="actionButtons_"]'
RTC_VOICE = '#app-mount [class*="voiceButtonsContainer_"]'
RTC_ITEMS = [f'{RTC_ACTION} > *', f'{RTC_VOICE} > *']
out += [
    ",\n".join(f"{selector}::before" for selector in RTC_ITEMS) + " {",
    '    content: "";',
    "    display: var(--rl-rtc-display, none);",
    "    position: absolute;",
    "    z-index: 1;",
    "    left: 50%;",
    "    top: 50%;",
    "    width: 20px;",
    "    height: 20px;",
    "    transform: translate(-50%, -50%);",
    "    background: currentColor;",
    "    -webkit-mask: var(--rl-rtc-icon) center / contain no-repeat;",
    "    mask: var(--rl-rtc-icon) center / contain no-repeat;",
    "    pointer-events: none;",
    "}",
    "",
    ",\n".join(RTC_ITEMS) + " {",
    "    position: relative;",
    "}",
    "",
    "@container style(--rl-rtc-display: block) {",
    "    " + ",\n".join(
        f'{selector} :is(svg, canvas, video, [class*="lottie"], [class*="sprite"], [class*="buttonContents_"])'
        for selector in RTC_ITEMS
    ) + " {",
    "        display: none !important;",
    "    }",
    "}",
    "",
]
CAMERA_ON_LABELS = ["Turn Off Camera", "Apagar cámara", "Desactivar cámara", "Turn Camera Off"]
CAMERA_ON_SELECTOR = ", ".join(f'[aria-label*="{label}" i]' for label in CAMERA_ON_LABELS)
RTC_ICONS = [
    (f'{RTC_VOICE} > :nth-child(1):not(:nth-last-child(1))', "waveform"),
    (f'{RTC_VOICE} > :nth-last-child(1)', "phone-off"),
    (f'{RTC_ACTION} > :nth-child(1)', "camera-off"),
    (f'{RTC_ACTION} > :nth-child(1):is({CAMERA_ON_SELECTOR})', "camera"),
    (f'{RTC_ACTION} > :nth-child(1):has({CAMERA_ON_SELECTOR})', "camera"),
    (f'{RTC_ACTION} > :nth-child(2)', "screen-share"),
    (f'{RTC_ACTION} > :nth-child(3)', "apps"),
    (f'{RTC_ACTION} > :nth-child(4)', "soundboard"),
    (
        f'{RTC_ACTION} > :nth-last-child(1):has('
        '[aria-label*="Soundboard" i], [aria-label*="Mesa de sonido" i], '
        '[aria-label*="Panel de sonido" i], [aria-label*="Efectos de sonido" i])',
        "soundboard",
    ),
]
for selector, name in RTC_ICONS:
    out += [
        f"{selector} {{",
        f"    --rl-rtc-icon: {url(name)};",
        "    --rl-rtc-display: block;",
        "}",
        "",
    ]

import re

def pixel_path(name, scale=1.5):
    svg = (ROOT / "assets" / "icons" / f"{name}.svg").read_text()
    rows = {}
    for x, y in re.findall(r'<rect x="(\d+)" y="(\d+)" width="1" height="1"/>', svg):
        rows.setdefault(int(y), set()).add(int(x))
    assert rows, name
    number = lambda value: f"{value * scale:g}"
    d = ""
    for y in sorted(rows):
        columns = sorted(rows[y])
        index = 0
        while index < len(columns):
            start = columns[index]
            while index + 1 < len(columns) and columns[index + 1] == columns[index] + 1:
                index += 1
            width = columns[index] - start + 1
            d += f"M{number(start)} {number(y)}h{number(width)}v{number(1)}h-{number(width)}z"
            index += 1
    return d

# The CSS d property swaps the vector itself: no masks, no extra layers, and the
# icon keeps whatever fill Discord gives it. Matching on the path tag keeps the
# selectors in the fast tag bucket.
ICON = '#app-mount svg[viewBox="0 0 24 24"] > path'
every = [path for _, paths in SIGNATURES for path in paths]
out += [
    ",\n".join(f'{ICON}[d^="{path}"] ~ *' for path in every) + " {",
    "    display: none;",
    "}",
    "",
]
for name, paths in SIGNATURES:
    out += [
        ",\n".join(f'{ICON}[d^="{path}"]' for path in paths) + " {",
        f'    d: path("{pixel_path(name)}");',
        "    shape-rendering: crispEdges;",
        "}",
        "",
    ]

# A handful of Discord icons are a single basic shape instead of a path. The only
# one that is not already square is the common rarity badge; crop its circle into
# a square so it matches the rest of the set. The circle stays transparent in the
# compound Circle* icons, so they are unaffected.
out += [
    '#app-mount svg[viewBox="0 0 24 24"] > circle[cx="12"][cy="12"][r="10"]:only-child {',
    "    clip-path: polygon(25% 25%, 75% 25%, 75% 75%, 25% 75%);",
    "}",
    "",
]

for name, color, fills in STATUS:
    selector = ",\n".join(f'#app-mount svg[class*="mask_"] rect[fill="{fill}" i]' for fill in fills)
    out += [
        f"{selector} {{",
        f"    fill: {color};",
        f"    -webkit-mask: {url(name)} center / contain no-repeat !important;",
        f"    mask: {url(name)} center / contain no-repeat !important;",
        "}",
        "",
    ]

out += [
    '#app-mount svg[class*="mask_"] rect[mask="url(#svg-mask-status-online-mobile)"] {',
    f"    -webkit-mask: {url('status-mobile')} center / contain no-repeat !important;",
    f"    mask: {url('status-mobile')} center / contain no-repeat !important;",
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
