# ReCord

A REPLACED-inspired terminal for Discord. One signal color, pixel type, square panels, scanlines and grain, in a dark terminal or a light paper mode.

![ReCord](docs/banner.png)

## Install

**Linux, macOS, Git Bash, WSL**

```bash
curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash
```

**Windows PowerShell**

```powershell
irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1 | iex
```

The installer finds Vencord, Vesktop, Equicord, Equibop and BetterDiscord (native and Flatpak), copies `ReCord.theme.css` into each themes folder and switches it on. Fully close Discord and open it again. Run the same command to update.

| Option | Effect |
| --- | --- |
| `--plugin` | Also build the ReCord plugin for Vesktop: in-app settings and sounds. Needs `git` and Node.js. |
| `--no-enable` | Copy the theme without switching it on. |
| `--uninstall` | Remove the theme and the plugin build. |

Pass options after `bash -s --`:

```bash
curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash -s -- --plugin
curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash -s -- --uninstall
```

On PowerShell, uninstall with:

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -Uninstall
```

### Without the installer

- **Online theme**: paste `https://raw.githubusercontent.com/leriart/ReCord/main/ReCord.theme.css` in `Vencord` -> `Themes` -> `Online Themes`.
- **File**: download [`ReCord.theme.css`](https://raw.githubusercontent.com/leriart/ReCord/main/ReCord.theme.css) and drop it into `Themes` -> `Local Themes` -> `Open Themes Folder`.

The file is self-contained: fonts, icons and textures are embedded, so it works offline.

Use ReCord as the only enabled theme. Other full themes override the same Discord variables and the two will mix.

## Configure

| Option | Values |
| --- | --- |
| Color mode | Follow Discord appearance, dark terminal, light paper |
| Accent | Any color; every accent shade derives from it. Presets: amber, phosphor, ice, paper, terminal |
| Free colors | Your own background and text colors; panels, borders and secondary text follow |
| Background image | Your own picture, with darkening and panel opacity |
| Animations | Full, subtle (menus and dialogs only), off |
| Typeface | Pixel Operator, Pixel Operator Mono, system monospace, Discord default |
| CRT layer | Scanlines, grain, vignette, flicker, rolling scan beam, corner frame |
| Pixel icons | On, or Discord's native icons |
| Avatars | Warm filter and scanlines on or off |

Three ways to change them:

1. **In Discord**, with the plugin: `Settings` -> `Plugins` -> `ReCord`. Changes apply live. Presets set a whole palette at once, and `Export`/`Import` saves your setup to a JSON file.
2. **On the [landing page](https://leriart.github.io/ReCord/)** (English and Spanish): the `CONFIGURE` card downloads a theme with your settings baked in, or copies a block for QuickCSS.
3. **By hand** in `Vencord` -> `Themes` -> `QuickCSS`:

```css
html:root:root {
    --rl-accent: #3ddc97;
    --rl-motion: subtle;              /* full | subtle | off */
    --rl-icons: on;                   /* on | off */
    --rl-scanline-opacity: 0.25;
    --rl-grain-opacity: 0.18;
    --rl-vignette-opacity: 0.55;
    --rl-flicker-duration: 0s;        /* 6s to enable */
    --rl-frame-opacity: 0.6;
    --rl-beam-opacity: 0.5;           /* 0 hides the scan beam */
    --rl-background-image: url("https://i.imgur.com/picture.png");
    --rl-background-dim: 70%;
    --rl-surface: 70%;                /* panel opacity */
}
```

Light mode follows Discord's own `Appearance` -> `Light`. A background URL in QuickCSS must be on a host Vencord allows (GitHub, Imgur, Discord CDN, Catbox); the plugin and the configurator take a file from your computer instead. The full palette is in `src/00-tokens.css`.

## Plugin

`plugin/record` is a Vencord userplugin, installed with `--plugin`. Themes are CSS-only, so the plugin provides what CSS cannot:

- **Settings panel** for every option above.
- **Replaced Discord sounds**: messages, mentions, mute, deafen, join, leave, calls, streams, camera, push-to-talk, activities.
- **Interface sounds**: hover, select, back, navigation, toggles, menu open and close, typing, send, boot.
- **Sound control**: a list of every sound with a switch and a Play button, one volume for interface sounds and another for the replaced Discord sounds.
- **Your own sounds**: any audio file in the `record-sounds` folder (button in the settings) replaces the bundled sound with the same name, either a pack name (`mention`, `hover`...) or a Discord event (`message1`, `user_join`...). WAV, OGG, MP3, FLAC and M4A.

The installer builds Vencord with the plugin and points Vesktop at that build, so Vencord stops updating itself there; run the installer again to update. For any other Vencord built from source, copy `plugin/record` into `src/userplugins/` and run `pnpm build && pnpm inject`.

The bundled pack in `sounds/` is original synthesized audio (CC0). A second interface set, Kenney's UI SFX Set (CC0, by Kenney Vleugels, kenney.nl), is in `sounds/kenney/` and can be chosen in the plugin. No game audio is included or distributed. Preview it at `docs/sounds.html`.

## What it changes

- **Selections**: the active channel, DM, menu item and settings entry are solid accent blocks with dark type.
- **Motion**: everything moves in steps. Menus wipe in, the chat redraws from a beam on channel switch, rows flash on hover and invert on press.
- **Icons**: 104 original 16 x 16 pixel icons. Discord's glyphs are matched by their vector shape, so they are replaced everywhere they appear (toolbar, menus, settings, channel list, member list) in any language. Status indicators are square pixel glyphs: block for online, notch for idle, bar for do not disturb, hollow for offline. Gallery at `docs/icons.html`.
- **Avatars**: square, framed, with a warm filter.
- **Startup**: Discord's loading screen shows the pixel mark. For Vesktop's own splash choose `assets/brand/splash.gif` in `Vesktop Settings` -> `Customize App Assets`.

## Structure

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

## Releases

Pushing a tag such as `v3.5.0` publishes a GitHub release with `ReCord.theme.css` attached, so a specific version can be pinned:

```text
https://github.com/leriart/ReCord/releases/download/v3.5.0/ReCord.theme.css
```

## Development

```bash
npm install
npm run build     # bundle src/ into ReCord.theme.css
npm run check     # CSS syntax, asset references, bundle is up to date
npm run serve     # http://127.0.0.1:8123/docs/index.html
```

Edit `src/`, then run `npm run build`; the committed `ReCord.theme.css` is what users install. `npm run icons` and `npm run sounds` regenerate the generated assets.

## Compatibility

Vencord, Vesktop, Equicord, Equibop and BetterDiscord on Discord desktop. Developed and checked against Vesktop on Linux. The PowerShell installer and the macOS paths have not been run on real machines yet; reports are welcome. Pixel Operator covers Latin glyphs; other scripts fall back to Discord's font.

## Credits

- Theme code: Apache-2.0. Plugin: GPL-3.0-or-later, as required for Vencord plugins.
- Pixel Operator by Jayvee Enaguas (HarvettFox96): CC0 1.0, license at `assets/fonts/LICENSE-PixelOperator.txt`.
- Kenney UI SFX Set by Kenney Vleugels ([kenney.nl](https://kenney.nl/assets/ui-audio)): CC0 1.0, license at `sounds/kenney/LICENSE.txt`.
- Visual reference: REPLACED, a game by Sad Cat Studios published by Thunderful. [playreplaced.com](https://playreplaced.com/)
- Unofficial fan project, not affiliated with Sad Cat Studios or Thunderful. No game assets are included.

[Español](README.es.md)
