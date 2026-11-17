# RECORD Signal Pack

Original synthesized terminal sounds inspired by REPLACED's interface. No audio from the game is included or redistributed.

All files are CC0 1.0. Replace any WAV with your own capture using the same filename and the mapping in `manifest.json` keeps working.

## ReCordSounds plugin

`plugin/record` is a Vencord userplugin that loads this folder, replaces Discord's sounds using the `customSounds` map in `manifest.json` and plays the `ui` sounds on hover, select, back, navigation, toggles, menus, typing and send. Seasonal variants such as `halloween_mute` or `winter_user_join` resolve to the same file as the base event. Install it on Vesktop with `install.sh --plugin`.

## Mapping for Equicord CustomSounds

Enable `CustomSounds` in Equicord, open its settings, enable each event you want and upload the matching file as a custom sound.

| Equicord event | File |
| --- | --- |
| Message 1 (Generic) | `receive.wav` |
| Message 2 (Reply) | `reply.wav` |
| Message 3 (DMs) | `receive.wav` |
| Mention 1/2/3 | `mention.wav` |
| Mute / Unmute | `mute.wav` / `unmute.wav` |
| Deafen / Undeafen | `deafen.wav` / `undeafen.wav` |
| User Join / Leave | `join.wav` / `leave.wav` |
| Disconnect / Reconnect | `disconnect.wav` / `reconnect.wav` |
| Call Ringing / Calling | `ring.wav` |
| Success | `success.wav` |
| Clip Error | `error.wav` |
| Stream Started / Ended | `stream-on.wav` / `stream-off.wav` |
| PTT Start / Stop | `ptt-on.wav` / `ptt-off.wav` |

`hover.wav`, `select.wav`, `back.wav`, `send.wav`, `type.wav`, `open.wav`, `close.wav`, `navigate.wav`, `toggle.wav` and `boot.wav` are interface sounds played by the plugin.

## Regenerate

```bash
python3 scripts/generate-sounds.py
```

The generator uses only the Python standard library.

## Kenney set

`kenney/` holds nine files from the UI SFX Set by Kenney Vleugels (kenney.nl), released under CC0 1.0; the license is in `kenney/LICENSE.txt`. They are mapped in the `sets.kenney` block of `manifest.json` and can be selected in the plugin as the interface sound set.
