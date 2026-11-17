# ReCord

Un terminal para Discord inspirado en REPLACED. Un solo color de señal, tipografía pixel, paneles rectos, scanlines y grano, en modo terminal oscuro o papel claro.

![ReCord](docs/banner.png)

## Instalación

**Linux, macOS, Git Bash, WSL**

```bash
curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash
```

**Windows PowerShell**

```powershell
irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1 | iex
```

El instalador busca Vencord, Vesktop, Equicord, Equibop y BetterDiscord (nativos y Flatpak), copia `ReCord.theme.css` a cada carpeta de temas y lo activa. Cierra Discord por completo y vuelve a abrirlo. El mismo comando sirve para actualizar.

| Opción | Efecto |
| --- | --- |
| `--plugin` | Compila también el plugin ReCord para Vesktop: ajustes dentro de Discord y sonidos. Necesita `git` y Node.js. |
| `--no-enable` | Copia el tema sin activarlo. |
| `--uninstall` | Quita el tema y la compilación del plugin. |

Las opciones van después de `bash -s --`:

```bash
curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash -s -- --plugin
curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash -s -- --uninstall
```

En PowerShell, para desinstalar:

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -Uninstall
```

### Sin el instalador

- **Tema online**: pega `https://raw.githubusercontent.com/leriart/ReCord/main/ReCord.theme.css` en `Vencord` -> `Themes` -> `Online Themes`.
- **Archivo**: descarga [`ReCord.theme.css`](https://raw.githubusercontent.com/leriart/ReCord/main/ReCord.theme.css) y suéltalo en `Themes` -> `Local Themes` -> `Open Themes Folder`.

El archivo es autocontenido: fuentes, iconos y texturas van embebidos, así que funciona sin conexión.

Usa ReCord como único tema activo. Otros temas completos sobrescriben las mismas variables de Discord y se mezclan.

## Configuración

| Opción | Valores |
| --- | --- |
| Modo de color | Seguir la apariencia de Discord, terminal oscuro, papel claro |
| Acento | Cualquier color; todos los tonos de acento salen de él |
| Colores libres | Tu propio color de fondo y de texto; paneles, bordes y texto secundario los siguen |
| Imagen de fondo | Tu propia imagen, con oscurecido y opacidad de paneles |
| Animaciones | Completas, sutiles (solo menús y diálogos), desactivadas |
| Tipografía | Pixel Operator, Pixel Operator Mono, monoespaciada del sistema, la de Discord |
| Capa CRT | Scanlines, grano, viñeta, parpadeo, haz de barrido, marco de esquinas |
| Iconos pixel | Activados, o los iconos nativos de Discord |
| Avatares | Filtro cálido y scanlines, sí o no |

Tres formas de cambiarlas:

1. **Dentro de Discord**, con el plugin: `Ajustes` -> `Plugins` -> `ReCord`. Los cambios se aplican al momento.
2. **En la [página](https://leriart.github.io/ReCord/)** (en inglés y español): la tarjeta `CONFIGURE` descarga el tema con tu configuración incluida, o copia un bloque para QuickCSS.
3. **A mano** en `Vencord` -> `Themes` -> `QuickCSS`:

```css
html:root:root {
    --rl-accent: #3ddc97;
    --rl-motion: subtle;              /* full | subtle | off */
    --rl-icons: on;                   /* on | off */
    --rl-scanline-opacity: 0.25;
    --rl-grain-opacity: 0.18;
    --rl-vignette-opacity: 0.55;
    --rl-flicker-duration: 0s;        /* 6s para activarlo */
    --rl-frame-opacity: 0.6;
    --rl-beam-opacity: 0.5;           /* 0 oculta el haz de barrido */
    --rl-background-image: url("https://i.imgur.com/imagen.png");
    --rl-background-dim: 70%;
    --rl-surface: 70%;                /* opacidad de paneles */
}
```

El modo claro sigue la `Apariencia` -> `Claro` de Discord. Una URL de fondo en QuickCSS tiene que estar en un host que Vencord permita (GitHub, Imgur, CDN de Discord, Catbox); el plugin y el configurador aceptan un archivo de tu equipo. La paleta completa está en `src/00-tokens.css`.

## Plugin

`plugin/record` es un userplugin de Vencord que se instala con `--plugin`. Los temas son solo CSS, así que el plugin aporta lo que el CSS no puede:

- **Panel de ajustes** con todas las opciones de arriba.
- **Sonidos de Discord sustituidos**: mensajes, menciones, silenciar, ensordecer, entrar, salir, llamadas, directos, cámara, pulsar para hablar, actividades.
- **Sonidos de interfaz**: cursor, seleccionar, volver, navegar, interruptores, abrir y cerrar menús, teclear, enviar, arranque.
- **Control de sonidos**: una lista con cada sonido, su interruptor y un botón para oírlo; un volumen para los sonidos de interfaz y otro para los sonidos de Discord sustituidos.
- **Tus propios sonidos**: cualquier audio en la carpeta `record-sounds` (hay un botón en los ajustes) sustituye al sonido incluido del mismo nombre, sea un nombre del pack (`mention`, `hover`...) o un evento de Discord (`message1`, `user_join`...). WAV, OGG, MP3, FLAC y M4A.

El instalador compila Vencord con el plugin y apunta Vesktop a esa compilación, así que ahí Vencord deja de actualizarse solo; vuelve a ejecutar el instalador para actualizar. En cualquier otro Vencord compilado desde el código, copia `plugin/record` en `src/userplugins/` y ejecuta `pnpm build && pnpm inject`.

El pack de `sounds/` es audio original sintetizado (CC0). No se incluye ni distribuye audio del juego. Se puede escuchar en `docs/sounds.html`.

## Qué cambia

- **Selecciones**: el canal, DM, elemento de menú y entrada de ajustes activos son bloques sólidos del color de acento con texto oscuro.
- **Movimiento**: todo se mueve a saltos. Los menús entran con un barrido, el chat se redibuja desde una línea al cambiar de canal, las filas destellan al pasar el cursor y se invierten al pulsar.
- **Iconos**: 103 iconos pixel originales de 16 x 16. Los glifos de Discord se identifican por su forma vectorial, así que se sustituyen en todos los sitios donde aparecen (barra superior, menús, ajustes, lista de canales, lista de miembros) y en cualquier idioma. Los indicadores de estado son glifos pixel cuadrados: bloque para conectado, muesca para ausente, barra para no molestar, hueco para desconectado. Galería en `docs/icons.html`.
- **Avatares**: cuadrados, con marco y filtro cálido.
- **Arranque**: la pantalla de carga de Discord muestra la marca pixel. Para el splash de Vesktop elige `assets/brand/splash.gif` en `Vesktop Settings` -> `Customize App Assets`.

## Estructura

```text
ReCord/
├── ReCord.theme.css     built theme, self-contained
├── install.sh           installer for Linux, macOS, Git Bash, WSL
├── install.ps1          installer for Windows PowerShell
├── src/                 CSS modules, bundled in numeric order
├── plugin/record/       Vencord userplugin: settings and sounds
├── assets/              fonts (CC0), pixel icons, brand art, splash
├── sounds/              signal pack (CC0) and manifest
├── docs/                landing page, configurator, galleries
└── scripts/             build, check, icon and sound generators
```

## Desarrollo

```bash
npm install
npm run build     # empaqueta src/ en ReCord.theme.css
npm run check     # sintaxis CSS, assets y que el paquete esté al día
npm run serve     # http://127.0.0.1:8123/docs/index.html
```

Edita `src/` y ejecuta `npm run build`; el `ReCord.theme.css` del repositorio es lo que instalan los usuarios. `npm run icons` y `npm run sounds` regeneran los assets generados.

## Compatibilidad

Vencord, Vesktop, Equicord, Equibop y BetterDiscord en Discord de escritorio. Desarrollado y comprobado en Vesktop sobre Linux. El instalador de PowerShell y las rutas de macOS todavía no se han ejecutado en máquinas reales; se agradecen reportes. Pixel Operator cubre glifos latinos; otros alfabetos usan la fuente de Discord.

## Créditos

- Código del tema: Apache-2.0. Plugin: GPL-3.0-or-later, como exigen los plugins de Vencord.
- Pixel Operator, de Jayvee Enaguas (HarvettFox96): CC0 1.0, licencia en `assets/fonts/LICENSE-PixelOperator.txt`.
- Referencia visual: REPLACED, un juego de Sad Cat Studios publicado por Thunderful. [playreplaced.com](https://playreplaced.com/)
- Proyecto de fans no oficial, sin relación con Sad Cat Studios ni Thunderful. No incluye assets del juego.

[English](README.md)
