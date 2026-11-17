# Changelog

## 3.1.0

- Status indicators are now matched by fill color, so the pixel glyphs also apply in the DM list and wherever Discord uses per-avatar masks
- Fixed pixel icons hidden inside guild rail badges and folders
- 103 icons: added chevron-up, play, poll, eye and more path signatures (attach menu, server menu, inbox)
- Retro pass: CRT power-on when the app loads, rolling scan beam, blinking online and streaming status, chromatic split on avatar and server hover, blinking cursor in the empty message box and typing indicator
- Terminal punctuation: `>` marker on the active channel, DM and menu item, `//` on list headers, `[ ]` around date dividers
- Plugin and configurator: scan beam switch

## 3.0.0

- Renamed to ReCord: repository, theme file (`ReCord.theme.css`), plugin (`plugin/record`) and local folders
- One-line installers: `install.sh` (Linux, macOS, Git Bash, WSL) and `install.ps1` (Windows). They find every supported client, install and enable the theme, update, and uninstall; `--plugin` builds the plugin for Vesktop
- Light paper mode: follows Discord's Light appearance, or can be forced from the plugin or the configurator
- Background image with darkening and panel opacity
- Animation levels: full, subtle, off
- Typeface choice and corner frame switch
- Icons: 99 in total (38 new). Discord icons are now matched by SVG path, so menus, settings, channel list and member list are covered in every language
- Status indicators (online, idle, do not disturb, offline, streaming, mobile) redrawn as square pixel glyphs; voice connection signal icon added
- Plugin: background picker that reads a local file, mode, animation and typeface selectors
- Configurator: all options, forced mode palettes, embedded background on download
- `scripts/install-plugin.sh` replaced by `install.sh --plugin`

## 2.1.0

- Fixed images and videos not opening in the viewer: the modal animation left a `clip-path` on Discord's zero-size dialog wrapper, which clipped the whole viewer
- The plugin is now `ReCord` (`plugin/record`) and has in-app theme settings: accent picker, scanlines, grain, vignette, flicker, pixel icons, animations and avatar filter
- Added a local `record-sounds` folder: any audio file placed there replaces the bundled sound with the same name
- Landing page configurator: same controls, downloads a theme with the settings baked in or copies a QuickCSS block
- Added `--rl-icons` and `--rl-motion` switches
- Motion pass: stepped transitions everywhere, beam redraw on channel switch, list slide-in, hover flash, press invert, icon jitter, reaction pop, typing cursor
- `scripts/install-sounds.sh` renamed to `scripts/install-plugin.sh`

## 2.0.0

- Fixed attachments, GIFs and embeds staying hidden: a forced `opacity: 1` kept Discord's blurred placeholder on top of the loaded image
- `ReCord.theme.css` is now one self-contained file with embedded fonts, icons and textures; it can be used as an online link or downloaded and dropped into the themes folder, and works offline
- Added `--rl-accent`: one variable recolors the whole interface, including Discord's brand tokens
- Added the `ReCordSounds` userplugin: replaces Discord's sounds with the signal pack and adds hover, select, back, navigation, toggle, menu, typing and send sounds; `scripts/install-sounds.sh` installs it for Vesktop
- Added nine sounds (type, open, close, navigate, toggle, camera on/off, clip, stage)
- New interface layer checked against the live client: inverted solid selections for channels, DMs, menus and settings, like REPLACED's menus
- Rebuilt avatar styling on Discord's real avatar markup: square portraits without layout side effects, no boxes around navigation icons
- Rebuilt icon replacement: only mapped buttons are replaced, unmapped ones keep their native glyph instead of a fallback diamond
- Landing page: accent picker with a download button that bakes the chosen color into the file

## 1.1.0

- Added 61 original 16 x 16 pixel icons and CSS mask replacements for toolbar, panel, chat bar, channel and sidebar actions
- Contact avatars forced square with a warm CRT filter, scanline overlay and pixel frame
- Restored native absolute positioning for cozy message avatars so chat rows align again
- Server icons squared, filtered and framed with a scanline layer
- Selected DM and channel states forced to the dark terminal palette
- Hidden the large top/bottom unread banners in the channel list
- Added REPLACED-style menu motion: CRT wipe, staggered items, glitch hover, scan sweep, modal power-on
- Added signal sound pack and soundboard page
- Added animated Vesktop splash and CSS replacement for Discord's loading screen
- Added cache-busting version queries to every raw module import

## 1.0.3

- Fixed folder preview icons and square icon geometry
- Reduced unread pills and removed reply/mention divider lines
- Forced dark surface tokens against light mode and conflicting themes
- Added motion base and reduced-motion support

## 1.0.2

- Initial public theme structure
- Token layer, raw module imports, fonts, preview and landing page
