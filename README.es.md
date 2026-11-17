# RETROLESS

Tema de Discord inspirado en REPLACED. Naranja de señal, tipografía Pixel Operator, paneles rectos, scanlines, grano y bordes tramados. Hecho para Vencord y Equicord.

![RETROLESS](docs/banner.png)

## Resumen

RETROLESS traslada el lenguaje visual de los menús de REPLACED a Discord:

- Un único naranja de señal tomado del menú de pausa: `#E94221`
- Tipografía píxel para títulos, cuerpo y monoespaciado
- Geometría recta, reglas de un píxel y esquinas marcadas
- Capa CRT fija: scanlines, grano, viñeta y corchetes
- Cobertura completa: chat, servidores, miembros, perfiles, ajustes, modales, menús, pickers, voz y ajustes de Vencord
- Animación de menús estilo REPLACED: barrido de terminal de izquierda a derecha, entrada escalonada, glitch al pasar el cursor, barrido y pulso de badges
- CSS modular cargado directamente desde GitHub raw
- Soporte para movimiento reducido

No incluye arte del juego. La marca, el skyline, el grano y las esquinas son originales.

## Notas de referencia

- Menú principal: fondo negro, wordmark rojo-naranja tramado y una sola fila de opciones en mayúsculas.
- Pantalla de pausa: el mismo naranja de señal en título y acciones, sin cajas, tracking amplio y versión en la esquina inferior.
- Dispositivo Wingman: reproductor de lore diegético inspirado en la Game Boy Camera, el Walkman y el iPod de primera generación; LCD color papel, etiquetas naranjas, bisel y sombra en teal profundo.
- Arte del mundo: sombras teal profundas contra luz naranja intensa, con grano y scanlines marcados.

Esas observaciones guían la paleta, la escala tipográfica, la geometría de paneles y la capa CRT. El objetivo es una interfaz usable de Discord, no una copia literal del juego.

## Vista previa

![Vista previa](docs/preview.png)

## Instalación

### Vencord / Equicord

1. Abre los ajustes de Discord.
2. Entra en `Vencord` -> `Themes`.
3. Abre `Online Themes`.
4. Pega esta URL en una línea:

```text
https://raw.githubusercontent.com/leriart/Retroless/main/Retroless.theme.css
```

5. Activa `RETROLESS`. Reinicia Discord si la interfaz no se actualiza.

El archivo de entrada importa todos los módulos desde `raw.githubusercontent.com`. Vencord permite ese dominio para temas y fuentes.

Si una actualización de CSS no aparece, elimina el tema online y vuelve a agregarlo con un query de versión, o cierra Discord por completo desde la bandeja y vuelve a abrirlo:

```text
https://raw.githubusercontent.com/leriart/Retroless/main/Retroless.theme.css?v=1.0.3
```

Los imports de módulos también incluyen ese query, así que una entrada nueva carga módulos nuevos.

### Local

Clona el repositorio y carga `Retroless.theme.css` desde `Vencord` -> `Themes` -> `Local Themes`. Las importaciones online siguen activas, así que necesita conexión.

### Paquete offline

```bash
npm install
npm run build
```

Carga `dist/Retroless.theme.css` como tema local. El paquete incluye todos los módulos y copia las fuentes y los assets a su lado.

### Conflictos entre temas

Usa RETROLESS como único tema. ClearVision, Midnight, System24, Ryoku, Selene y otros temas completos sobrescriben las mismas variables de Discord y se mezclan con este, produciendo texto oscuro sobre fondos oscuros, buscadores claros o iconos redondeados.

Usa también la apariencia `Dark` o `Darker` de Discord. RETROLESS fuerza superficies oscuras, pero el modo claro puede filtrarse en componentes nativos.

Instala RETROLESS desde `Online Themes` o `Local Themes`. No pegues el tema completo en QuickCSS; usa QuickCSS solo para sobrescribir tokens.

## Movimiento

Los menús contextuales y modales abren con un barrido CRT por pasos. Los elementos del menú entran en secuencia, hacen glitch al pasar el cursor y reciben un barrido corto. Los canales y servidores seleccionados parpadean una vez, y los badges de no leídos pulsan. Todo se desactiva automáticamente con `prefers-reduced-motion: reduce`.

```css
:root {
    --rl-menu-duration: 190ms;
    --rl-item-duration: 150ms;
    --rl-glitch-duration: 220ms;
}
```

## Paleta

| Token | Hex | Origen |
| --- | --- | --- |
| Naranja de señal | `#E94221` | Menú de pausa / logo |
| Óxido | `#A8231B` | Sombra del logo |
| Papel Wingman | `#D4B496` | Interfaz del dispositivo |
| Teal de canal | `#14322A` | Tonos de sombra |
| Teal profundo | `#051F1C` | Bisel del dispositivo |
| Vacío | `#050605` | Base de superficie |

Estados:

| Estado | Hex |
| --- | --- |
| En línea | `#79B59A` |
| Ausente | `#DDA052` |
| No molestar | `#FF4626` |
| Desconectado | `#6F655A` |

## Personalización

Sobrescribe los tokens desde QuickCSS de Vencord. La paleta completa vive en `src/00-tokens.css`.

```css
:root {
    --rl-signal: #ff5a2e;
    --rl-signal-hot: #ff7a4f;
    --rl-panel: #10120e;
    --rl-line: #33271f;
    --rl-scanline-opacity: 0.35;
    --rl-grain-opacity: 0.22;
    --rl-vignette-opacity: 0.8;
}
```

| Variable | Valor | Efecto |
| --- | --- | --- |
| `--rl-signal` | `#e94221` | Acento principal, selección, badges |
| `--rl-signal-hot` | `#ff6a3d` | Hover y foco |
| `--rl-paper` | `#d4b496` | Texto secundario cálido |
| `--rl-bone` | `#e4cdb1` | Texto de cuerpo |
| `--rl-panel` | `#0e100c` | Barras laterales y tarjetas |
| `--rl-ink` | `#080907` | Chat y superficie principal |
| `--rl-void` | `#050605` | Fondo profundo e inputs |
| `--rl-line` | `#2c241d` | Bordes y reglas |
| `--rl-scanline-opacity` | `0.25` | Intensidad de scanlines |
| `--rl-grain-opacity` | `0.18` | Intensidad del grano |
| `--rl-vignette-opacity` | `0.55` | Intensidad de la viñeta |
| `--rl-flicker-duration` | `0s` | `9s` activa un parpadeo sutil |
| `--rl-font` | Pixel Operator | Tipografía de cuerpo e interfaz |
| `--rl-font-mono` | Pixel Operator Mono | Código y timestamps |
| `--rl-radius` | `0px` | Radio de componentes por token |

Para quitar el efecto CRT:

```css
:root {
    --rl-scanline-opacity: 0;
    --rl-grain-opacity: 0;
    --rl-vignette-opacity: 0;
}
```

## Estructura

```text
Retroless/
├── Retroless.theme.css      entrada / imports raw
├── src/
│   ├── 00-tokens.css        paleta, tipografía, efectos
│   ├── 01-fonts.css         fuentes Pixel Operator
│   ├── 02-tokens-discord.css
│   ├── 03-base.css
│   ├── 04-shell.css
│   ├── 05-navigation.css
│   ├── 06-chat.css
│   ├── 07-members.css
│   ├── 08-controls.css
│   ├── 09-overlays.css
│   ├── 10-settings.css
│   ├── 11-effects.css
│   ├── 12-priority.css
│   └── 13-motion.css
├── assets/
│   ├── brand/               marca, esquinas, grano, skyline
│   └── fonts/               Pixel Operator (CC0)
├── docs/                    landing y preview
├── scripts/                 validación y bundle
└── LICENSE
```

## Desarrollo

```bash
npm install
npm run check
npm run build
npm run serve
```

- `npm run check` valida imports raw, assets y sintaxis CSS.
- `npm run build` genera el paquete offline en `dist/`.
- `npm run serve` sirve el repositorio en `http://127.0.0.1:8123`.
- Preview: `http://127.0.0.1:8123/docs/preview.html`
- Landing: `http://127.0.0.1:8123/docs/index.html`

La base raw está definida en `Retroless.theme.css` y `scripts/build.mjs`. Cambia ambas si haces un fork.

## Compatibilidad

- Vencord
- Equicord
- Vesktop
- Discord desktop

Discord web no es objetivo. Las clases de Discord pueden cambiar entre versiones; el tema usa atributos de datos y prefijos estables cuando es posible.

Pixel Operator cubre glifos latinos. Otros alfabetos usan el fallback normal de Discord.

## Créditos

- Código del tema: Apache-2.0
- Pixel Operator de Jayvee Enaguas (HarvettFox96): CC0 1.0, licencia en `assets/fonts/LICENSE-PixelOperator.txt`
- Paleta tomada de capturas de menú de REPLACED
- Referencia de diseño: [Game Developer / The Wingman](https://www.gamedeveloper.com/design/replaced-wingman)
- Página oficial: [playreplaced.com](https://playreplaced.com/)
- REPLACED es un juego de Sad Cat Studios, publicado por Thunderful
- Proyecto fan no oficial. Sin afiliación con Sad Cat Studios ni Thunderful. No incluye assets del juego.
