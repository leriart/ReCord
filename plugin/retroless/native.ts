/*
 * RETROLESS, a Vencord userplugin
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

import { app, IpcMainInvokeEvent, shell } from "electron";
import { mkdir, readdir, readFile } from "fs/promises";
import { extname, join } from "path";

const TYPES: Record<string, string> = {
    ".wav": "audio/wav",
    ".ogg": "audio/ogg",
    ".mp3": "audio/mpeg",
    ".flac": "audio/flac",
    ".m4a": "audio/mp4"
};

const folder = () => join(app.getPath("userData"), "retroless-sounds");

export async function getSoundFolder(_: IpcMainInvokeEvent) {
    await mkdir(folder(), { recursive: true });
    return folder();
}

export async function openSoundFolder(_: IpcMainInvokeEvent) {
    await mkdir(folder(), { recursive: true });
    await shell.openPath(folder());
}

export async function readLocalSounds(_: IpcMainInvokeEvent) {
    await mkdir(folder(), { recursive: true });
    const sounds: Array<{ name: string; type: string; data: Uint8Array; }> = [];

    for (const file of await readdir(folder())) {
        const extension = extname(file).toLowerCase();
        const type = TYPES[extension];
        if (!type) continue;
        sounds.push({ name: file.slice(0, -extension.length).toLowerCase(), type, data: await readFile(join(folder(), file)) });
    }

    return sounds;
}
