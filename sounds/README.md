# RECORD Signal Pack

Original synthesized terminal sounds inspired by REPLACED's interface. No audio from the game is included or redistributed.

All files are CC0 1.0. Replace any WAV with your own capture using the same filename and the mapping in `manifest.json` keeps working.

## ReCordSounds plugin

`plugin/record` is a Vencord userplugin that loads this folder, replaces Discord's sounds using the `customSounds` map in `manifest.json` and plays the `ui` sounds on hover, select, back, navigation, toggles, menus, typing and send. Seasonal variants such as `halloween_mute` or `winter_user_join` resolve to the same file as the base event. The installer sets it up on Vesktop by default.

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

## Sound themes

`manifest.json` has a `sets` block. Each set has a label and a `sounds` map from a sound name to a file. A name is either an interface sound (`hover`, `select`, `back`...) or the name of a file in the synthesized pack (`mention`, `receive`, `join`...), which is how a set also replaces Discord's sounds. A set does not need every name; missing ones fall back to the synthesized pack.

| Folder | Source | License |
| --- | --- | --- |
| `kenney/` | UI SFX Set, Kenney Vleugels (kenney.nl) | CC0 1.0, `kenney/LICENSE.txt` |
| `kenney-interface/` | Interface Sounds, Kenney Vleugels (kenney.nl) | CC0 1.0, `kenney-interface/LICENSE.txt` |
| `uisfx/` | UI SFX, Yuki Capital (github.com/romainsimon/uisfx), twelve packs | CC0 1.0, `uisfx/LICENSE-AUDIO.txt` |

To add a set, drop the files in a new folder, add an entry to `sets`, and add its label to the `uiSet` options in `plugin/record/index.tsx`.
