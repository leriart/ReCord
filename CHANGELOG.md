# Changelog

## 2.0.0

- Fixed attachments, GIFs and embeds staying hidden: a forced `opacity: 1` kept Discord's blurred placeholder on top of the loaded image
- `Retroless.theme.css` is now one self-contained file with embedded fonts, icons and textures; it can be used as an online link or downloaded and dropped into the themes folder, and works offline
- Added `--rl-accent`: one variable recolors the whole interface, including Discord's brand tokens
- Added the `RetrolessSounds` userplugin: replaces Discord's sounds with the signal pack and adds hover, select, back, navigation, toggle, menu, typing and send sounds; `scripts/install-sounds.sh` installs it for Vesktop
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
