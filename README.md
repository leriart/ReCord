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

The [website](https://leriart.github.io/ReCord/) detects your system and shows the right command.

One command installs three things. Fully close Discord and open it again afterwards; run the same command to update.

| What | Where | Notes |
| --- | --- | --- |
| Theme | Vencord, Vesktop, Equicord, Equibop, BetterDiscord, Dorion, Legcord, GoofCord, Replugged (native and Flatpak) | Copied to each themes folder and switched on |
| Startup splash | Vesktop | The pixel mark instead of Vesktop's splash window |
| Plugin | Vesktop | In-app settings and sounds. A ready-made build is downloaded; no git or Node.js needed |

| Option | Windows | Effect |
| --- | --- | --- |
| `--no-plugin` | `-NoPlugin` | Theme and splash only; Vencord stays as it is |
| `--no-enable` | `-NoEnable` | Copy the theme without switching it on |
| `--uninstall` | `-Uninstall` | Remove everything and restore the settings it changed |
| `--doctor` | `-Doctor` | Report what is installed and whether the plugin build downloads; changes nothing |

Pass options after `bash -s --`:

```bash
curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash -s -- --no-plugin
curl -fsSL https://raw.githubusercontent.com/leriart/ReCord/main/install.sh | bash -s -- --uninstall
```

On PowerShell:

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -Uninstall
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/leriart/ReCord/main/install.ps1))) -Doctor
```

Both installers stop if Discord is still running, because a client rewrites its settings on exit and would undo the plugin setup. Close it from the tray as well.

### Without the installer

- **Online theme**: paste `https://raw.githubusercontent.com/leriart/ReCord/main/ReCord.theme.css` in `Vencord` -> `Themes` -> `Online Themes`.
- **File**: download [`ReCord.theme.css`](https://raw.githubusercontent.com/leriart/ReCord/main/ReCord.theme.css) and drop it into `Themes` -> `Local Themes` -> `Open Themes Folder`.

The file is self-contained: fonts, icons and textures are embedded, so it works offline.

Want to try before installing? The [live demo](https://leriart.github.io/ReCord/docs/preview.html) is a working mock: hover, click and type to hear every sound theme, and switch accent and mode.

Use ReCord as the only enabled theme. Other full themes override the same Discord variables and the two will mix.

## Configure

| Option | Values |
| --- | --- |
| Color mode | Follow Discord appearance, dark terminal, light paper |
| Accent | Any color; every accent shade derives from it. Presets: amber, phosphor, ice, paper, terminal |
| Free colors | Your own background and text colors; panels, borders and secondary text follow |
| Background | Your own image, GIF or video (plugin), with darkening and panel opacity |
| Animations | Full, subtle (menus and dialogs only), off |
| Typeface | Pixel Operator, Pixel Operator Mono, system monospace, Discord default |
| CRT layer | Scanlines, grain, vignette, flicker, rolling scan beam, corner frame |
| Pixel icons | On, or Discord's native icons |
| Low power | Turns off the scan beam, grain, flicker and constant animations, and hides profile effects, video banners and reaction glow |
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

Light mode follows Discord's own `Appearance` -> `Light`. A background URL in QuickCSS must be on a host Vencord allows (GitHub, Imgur, Discord CDN, Catbox); images and GIFs work there. The plugin and the configurator take a file from your computer instead, and the plugin also plays videos. The full palette is in `src/00-tokens.css`.

## Plugin

`plugin/record` is a Vencord userplugin, installed by default on Vesktop. Themes are CSS-only, so the plugin provides what CSS cannot:

- **Settings panel** for every option above.
- **Replaced Discord sounds**: messages, mentions, mute, deafen, join, leave, calls, streams, camera, push-to-talk, activities.
- **Interface sounds**: hover, select, back, navigation, toggles, menu open and close, typing, send, boot.
- **Sound themes**: 15 to choose from. The synthesized terminal set, twelve UI SFX sets (arcade, sci-fi, mechanical, minimal, glass, cinematic, studio, soft, rubber, organic, dreamy, zen) and two Kenney sets. A theme changes the interface sounds and the replaced Discord sounds.
- **Mixing**: each sound has its own theme selector, so hover can come from one set and mentions from another.
- **Sound control**: a switch and a Play button per sound, one volume for interface sounds and another for the replaced Discord sounds.
- **Your own sounds**: any audio file in the `record-sounds` folder (button in the settings) replaces the bundled sound with the same name, either a pack name (`mention`, `hover`...) or a Discord event (`message1`, `user_join`...). WAV, OGG, MP3, FLAC and M4A.

The installer points Vesktop at a Vencord build that includes the plugin, so Vencord stops updating itself there; run the installer again to update. The build is published by the `plugin.yml` workflow, and the Linux and macOS installer can also build it locally when git and Node.js are present. For any other Vencord built from source, copy `plugin/record` into `src/userplugins/` and run `pnpm build && pnpm inject`.

The bundled pack in `sounds/` is original synthesized audio (CC0). A second interface set, Kenney's UI SFX Set (CC0, by Kenney Vleugels, kenney.nl), is in `sounds/kenney/` and can be chosen in the plugin. No game audio is included or distributed. Preview it at `docs/sounds.html`.

## What it changes

- **Selections**: the active channel, DM, menu item and settings entry are solid accent blocks with dark type.
- **Motion**: everything moves in steps. Menus wipe in, the chat redraws from a beam on channel switch, rows flash on hover and invert on press.
- **Icons**: 139 original 16 x 16 pixel icons. Every glyph in Discord's current icon set is mapped and matched by its vector shape, so icons are replaced everywhere they appear (toolbar, menus, settings, channel list, member list) in any language. Status indicators are square pixel glyphs: block for online, notch for idle, bar for do not disturb, hollow for offline. Gallery at `docs/icons.html`.
- **Background**: your own image, GIF or video behind the interface, with darkening and panel opacity. Videos play muted on a loop. Video files are a plugin feature; the website configurator accepts images and GIFs.
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

| Client | Theme | Plugin | How |
| --- | --- | --- | --- |
| Vesktop | Yes | Yes | Installer |
| Vencord, Equicord, Equibop, BetterDiscord | Yes | No | Installer |
| Dorion | Yes | No | Installer; copied to its themes folder and enabled in `config.json` |
| Legcord | Yes | No | Installer; written as a Legcord theme folder with its manifest |
| GoofCord | Yes | No | Installer; copied to its assets folder, which loads every `.css` |
| Replugged | Yes | No | Installer; enable it afterwards in Settings > Themes |
| Discord in a browser | Yes | No | Install [`ReCord.user.css`](https://raw.githubusercontent.com/leriart/ReCord/main/ReCord.user.css) with the Stylus extension |
| moonlight | Manual | No | It has no theme loader of its own; paste the import link into an extension that adds custom CSS |
| Yapfast and other native clients | No | No | They do not use Discord's web interface, so there is no CSS to restyle |

The plugin is a Vencord user plugin and is installed for Vesktop only. Everywhere else every option still works: they are CSS variables, and the [configurator](https://leriart.github.io/ReCord/#configure) writes the block to paste into the client's custom CSS box. Sounds need the plugin.

Developed and checked against Vesktop on Linux. Dorion, Legcord, GoofCord and Replugged follow the paths and formats in each client's source code and were tested against stand-in folders, not the real apps. The PowerShell installer and the macOS paths have not been run on real machines yet; reports are welcome. Pixel Operator covers Latin glyphs; other scripts fall back to Discord's font.

## Performance

The theme adds no blur, no blend modes and no JavaScript. It behaves the same on NVIDIA, AMD and Intel graphics because it never touches GPU flags: the right ones depend on the driver, and a wrong one can leave the window black.

- Keep hardware acceleration on in the client. It matters more than any theme option
- Low power turns off the scan beam, grain, flicker and constant animations, and hides Discord's profile effects, video banners and reaction glow
- `install.sh --doctor` (`-Doctor` on Windows) reports what is installed, whether the plugin build downloads, which GPU the system has and whether the client is drawing on the GPU. It changes nothing
- In Discord, Settings > Accessibility: turn off autoplay for GIFs, animated emoji and stickers

## Credits

- Theme code: Apache-2.0. Plugin: GPL-3.0-or-later, as required for Vencord plugins.
- Pixel Operator by Jayvee Enaguas (HarvettFox96): CC0 1.0, license at `assets/fonts/LICENSE-PixelOperator.txt`.
- UI SFX by Yuki Capital ([romainsimon/uisfx](https://github.com/romainsimon/uisfx)): audio CC0 1.0, license at `sounds/uisfx/LICENSE-AUDIO.txt`.
- Kenney Interface Sounds by Kenney Vleugels ([kenney.nl](https://kenney.nl/assets/interface-sounds)): CC0 1.0, license at `sounds/kenney-interface/LICENSE.txt`.
- Kenney UI SFX Set by Kenney Vleugels ([kenney.nl](https://kenney.nl/assets/ui-audio)): CC0 1.0, license at `sounds/kenney/LICENSE.txt`.
- Visual reference: REPLACED, a game by Sad Cat Studios published by Thunderful. [playreplaced.com](https://playreplaced.com/)
- Unofficial fan project, not affiliated with Sad Cat Studios or Thunderful. No game assets are included.

[Español](README.es.md)
