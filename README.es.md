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

La [página](https://leriart.github.io/ReCord/) detecta tu sistema y te muestra el comando correcto.

Un solo comando instala tres cosas. Después cierra Discord por completo y vuelve a abrirlo; el mismo comando sirve para actualizar.

| Qué | Dónde | Notas |
| --- | --- | --- |
| Tema | Vencord, Vesktop, Equicord, Equibop, BetterDiscord, Dorion, Legcord, GoofCord, Replugged (nativos y Flatpak) | Se copia a cada carpeta de temas y se activa |
| Splash de arranque | Vesktop | La marca pixel en lugar de la ventana de arranque de Vesktop |
| Plugin | Vesktop | Ajustes dentro de Discord y sonidos. Se descarga ya compilado; no hace falta git ni Node.js |

| Opción | Windows | Efecto |
| --- | --- | --- |
| `--no-plugin` | `-NoPlugin` | Solo tema y splash; Vencord se queda como está |
| `--no-enable` | `-NoEnable` | Copia el tema sin activarlo |
| `--uninstall` | `-Uninstall` | Lo quita todo y restaura los ajustes que cambió |
| `--doctor` | `-Doctor` | Informa de lo instalado y de si se descarga el plugin; no cambia nada |

Las opciones van después de `bash -s --`:

```bash
curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash -s -- --no-plugin
curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash -s -- --uninstall
```

En PowerShell:

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -Uninstall
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -Doctor
```

Los dos instaladores se detienen si Discord sigue abierto, porque el cliente reescribe sus ajustes al cerrarse y desharía la instalación del plugin. Ciérralo también desde la bandeja.

### Sin el instalador

- **Tema online**: pega `https://raw.githubusercontent.com/leriart/ReCord/main/ReCord.theme.css` en `Vencord` -> `Themes` -> `Online Themes`.
- **Archivo**: descarga [`ReCord.theme.css`](https://raw.githubusercontent.com/leriart/ReCord/main/ReCord.theme.css) y suéltalo en `Themes` -> `Local Themes` -> `Open Themes Folder`.

El archivo es autocontenido: fuentes, iconos y texturas van embebidos, así que funciona sin conexión.

¿Quieres probarlo antes de instalar? La [demo en vivo](https://leriart.github.io/ReCord/docs/preview.html) es una maqueta funcional: pasa el cursor, haz clic y escribe para oír cada tema de sonido, y cambia el acento y el modo.

Usa ReCord como único tema activo. Otros temas completos sobrescriben las mismas variables de Discord y se mezclan.

## Configuración

| Opción | Valores |
| --- | --- |
| Modo de color | Seguir la apariencia de Discord, terminal oscuro, papel claro |
| Acento | Cualquier color; todos los tonos de acento salen de él. Preajustes: ámbar, fósforo, hielo, papel, terminal |
| Colores libres | Tu propio color de fondo y de texto; paneles, bordes y texto secundario los siguen |
| Fondo | Tu propia imagen, GIF o vídeo (plugin), con oscurecido y opacidad de paneles |
| Animaciones | Completas, sutiles (solo menús y diálogos), desactivadas |
| Tipografía | Pixel Operator, Pixel Operator Mono, monoespaciada del sistema, la de Discord |
| Capa CRT | Scanlines, grano, viñeta, parpadeo, haz de barrido, marco de esquinas |
| Iconos pixel | Activados, o los iconos nativos de Discord |
| Bajo consumo | Apaga el haz de barrido, el grano, el parpadeo y las animaciones continuas, y oculta efectos de perfil, banners de vídeo y el brillo de las reacciones |
| Avatares | Filtro cálido y scanlines, sí o no |

Tres formas de cambiarlas:

1. **Dentro de Discord**, con el plugin: `Ajustes` -> `Plugins` -> `ReCord`. Los cambios se aplican al momento. Los preajustes cambian la paleta entera de una vez, y `Export`/`Import` guardan tu configuración en un archivo JSON.
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

El modo claro sigue la `Apariencia` -> `Claro` de Discord. Una URL de fondo en QuickCSS tiene que estar en un host que Vencord permita (GitHub, Imgur, CDN de Discord, Catbox); las imágenes y los GIFs funcionan ahí. El plugin y el configurador aceptan un archivo de tu equipo, y el plugin además reproduce vídeos. La paleta completa está en `src/00-tokens.css`.

## Plugin

`plugin/record` es un userplugin de Vencord que se instala por defecto en Vesktop. Los temas son solo CSS, así que el plugin aporta lo que el CSS no puede:

- **Panel de ajustes** con todas las opciones de arriba.
- **Sonidos de Discord sustituidos**: mensajes, menciones, silenciar, ensordecer, entrar, salir, llamadas, directos, cámara, pulsar para hablar, actividades.
- **Sonidos de interfaz**: cursor, seleccionar, volver, navegar, interruptores, abrir y cerrar menús, teclear, enviar, arranque.
- **Temas de sonido**: 15 para elegir. El sintetizado de terminal, doce de UI SFX (arcade, sci-fi, mecánico, minimal, cristal, cinemático, estudio, suave, goma, orgánico, onírico, zen) y dos de Kenney. Un tema cambia los sonidos de interfaz y los sonidos de Discord sustituidos.
- **Mezcla**: cada sonido tiene su propio selector de tema, así que el cursor puede venir de un juego y las menciones de otro.
- **Control de sonidos**: un interruptor y un botón para oír cada sonido, un volumen para los de interfaz y otro para los de Discord sustituidos.
- **Tus propios sonidos**: cualquier audio en la carpeta `record-sounds` (hay un botón en los ajustes) sustituye al sonido incluido del mismo nombre, sea un nombre del pack (`mention`, `hover`...) o un evento de Discord (`message1`, `user_join`...). WAV, OGG, MP3, FLAC y M4A.

El instalador apunta Vesktop a una compilación de Vencord que incluye el plugin, así que ahí Vencord deja de actualizarse solo; vuelve a ejecutar el instalador para actualizar. La compilación la publica el flujo `plugin.yml`, y el instalador de Linux y macOS también puede hacerla en local si hay git y Node.js. En cualquier otro Vencord compilado desde el código, copia `plugin/record` en `src/userplugins/` y ejecuta `pnpm build && pnpm inject`.

El pack de `sounds/` es audio original sintetizado (CC0). Hay un segundo juego de sonidos de interfaz, el UI SFX Set de Kenney (CC0, de Kenney Vleugels, kenney.nl), en `sounds/kenney/`, que se elige en el plugin. No se incluye ni distribuye audio del juego. Se puede escuchar en `docs/sounds.html`.

## Qué cambia

- **Selecciones**: el canal, DM, elemento de menú y entrada de ajustes activos son bloques sólidos del color de acento con texto oscuro.
- **Movimiento**: todo se mueve a saltos. Los menús entran con un barrido, el chat se redibuja desde una línea al cambiar de canal, las filas destellan al pasar el cursor y se invierten al pulsar.
- **Iconos**: 139 iconos pixel originales de 16 x 16. Todos los glifos del set actual de Discord están mapeados y se identifican por su forma vectorial, así que se sustituyen en todos los sitios donde aparecen (barra superior, menús, ajustes, lista de canales, lista de miembros) y en cualquier idioma. Los indicadores de estado son glifos pixel cuadrados: bloque para conectado, muesca para ausente, barra para no molestar, hueco para desconectado. Galería en `docs/icons.html`.
- **Fondo**: tu propia imagen, GIF o vídeo detrás de la interfaz, con oscurecido y opacidad de paneles. Los vídeos se reproducen en bucle y sin sonido. Los vídeos son una función del plugin; el configurador de la web acepta imágenes y GIFs.
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

## Versiones

Al empujar una etiqueta como `v3.5.0` se publica una versión en GitHub con `ReCord.theme.css` adjunto, para poder fijar una versión concreta:

```text
https://github.com/leriart/ReCord/releases/download/v3.5.0/ReCord.theme.css
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

| Cliente | Tema | Plugin | Cómo |
| --- | --- | --- | --- |
| Vesktop | Sí | Sí | Instalador |
| Vencord, Equicord, Equibop, BetterDiscord | Sí | No | Instalador |
| Dorion | Sí | No | Instalador; se copia a su carpeta de temas y se activa en `config.json` |
| Legcord | Sí | No | Instalador; se escribe como carpeta de tema de Legcord con su manifiesto |
| GoofCord | Sí | No | Instalador; se copia a su carpeta de assets, que carga todos los `.css` |
| Replugged | Sí | No | Instalador; después actívalo en Ajustes > Temas |
| Discord en el navegador | Sí | No | Instala [`ReCord.user.css`](https://raw.githubusercontent.com/leriart/ReCord/main/ReCord.user.css) con la extensión Stylus |
| moonlight | Manual | No | No trae cargador de temas; pega el enlace de importación en una extensión que añada CSS propio |
| Yapfast y otros clientes nativos | No | No | No usan la interfaz web de Discord, así que no hay CSS que cambiar |

El plugin es un plugin de usuario de Vencord y solo se instala en Vesktop. En el resto todas las opciones siguen funcionando: son variables CSS, y el [configurador](https://leriart.github.io/ReCord/#configure) genera el bloque que se pega en el CSS personalizado del cliente. Los sonidos necesitan el plugin.

Desarrollado y comprobado en Vesktop sobre Linux. Dorion, Legcord, GoofCord y Replugged siguen las rutas y formatos del código fuente de cada cliente y se probaron con carpetas de prueba, no con las aplicaciones reales. El instalador de PowerShell y las rutas de macOS todavía no se han ejecutado en máquinas reales; se agradecen reportes. Pixel Operator cubre glifos latinos; otros alfabetos usan la fuente de Discord.

## Rendimiento

El tema no añade desenfoques, modos de mezcla ni JavaScript. Se comporta igual con gráficas NVIDIA, AMD e Intel porque nunca toca las opciones de GPU: las correctas dependen del controlador, y una equivocada puede dejar la ventana en negro.

- Mantén la aceleración por hardware activada en el cliente. Importa más que cualquier opción del tema
- Bajo consumo apaga el haz de barrido, el grano, el parpadeo y las animaciones continuas, y oculta los efectos de perfil, los banners de vídeo y el brillo de las reacciones de Discord
- `install.sh --doctor` (`-Doctor` en Windows) informa de lo instalado, de si se descarga el plugin, la GPU del sistema y si el cliente está dibujando con la GPU. No cambia nada
- En Discord, Ajustes > Accesibilidad: desactiva la reproducción automática de GIF, emojis animados y stickers

## Créditos

- Código del tema: Apache-2.0. Plugin: GPL-3.0-or-later, como exigen los plugins de Vencord.
- Pixel Operator, de Jayvee Enaguas (HarvettFox96): CC0 1.0, licencia en `assets/fonts/LICENSE-PixelOperator.txt`.
- UI SFX de Yuki Capital ([romainsimon/uisfx](https://github.com/romainsimon/uisfx)): audio CC0 1.0, licencia en `sounds/uisfx/LICENSE-AUDIO.txt`.
- Interface Sounds de Kenney Vleugels ([kenney.nl](https://kenney.nl/assets/interface-sounds)): CC0 1.0, licencia en `sounds/kenney-interface/LICENSE.txt`.
- UI SFX Set de Kenney Vleugels ([kenney.nl](https://kenney.nl/assets/ui-audio)): CC0 1.0, licencia en `sounds/kenney/LICENSE.txt`.
- Referencia visual: REPLACED, un juego de Sad Cat Studios publicado por Thunderful. [playreplaced.com](https://playreplaced.com/)
- Proyecto de fans no oficial, sin relación con Sad Cat Studios ni Thunderful. No incluye assets del juego.

[English](README.md)
