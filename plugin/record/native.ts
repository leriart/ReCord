/*
 * RECORD, a Vencord userplugin
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

import { app, dialog, IpcMainInvokeEvent, shell } from "electron";
import { copyFile, mkdir, readdir, readFile, rm, writeFile } from "fs/promises";
import { extname, join } from "path";

const TYPES: Record<string, string> = {
    ".wav": "audio/wav",
    ".ogg": "audio/ogg",
    ".mp3": "audio/mpeg",
    ".flac": "audio/flac",
    ".m4a": "audio/mp4"
};

const folder = () => join(app.getPath("userData"), "record-sounds");

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

const IMAGES: Record<string, string> = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".avif": "image/avif"
};

const VIDEOS: Record<string, string> = {
    ".mp4": "video/mp4",
    ".m4v": "video/mp4",
    ".webm": "video/webm",
    ".ogv": "video/ogg",
    ".mov": "video/quicktime"
};

const BACKGROUNDS: Record<string, string> = { ...IMAGES, ...VIDEOS };

const backgroundBase = () => join(app.getPath("userData"), "record-background");

async function findBackground() {
    for (const extension of Object.keys(BACKGROUNDS)) {
        try {
            const file = backgroundBase() + extension;
            return { type: BACKGROUNDS[extension], data: await readFile(file) as Uint8Array };
        } catch { }
    }
    return null;
}

export async function clearBackground(_: IpcMainInvokeEvent) {
    await Promise.all(Object.keys(BACKGROUNDS).map(extension => rm(backgroundBase() + extension, { force: true })));
}

export async function readBackground(_: IpcMainInvokeEvent) {
    return findBackground();
}

export async function pickBackground(event: IpcMainInvokeEvent) {
    const result = await dialog.showOpenDialog({
        title: "RECORD background",
        properties: ["openFile"],
        filters: [{ name: "Images, GIFs and videos", extensions: Object.keys(BACKGROUNDS).map(extension => extension.slice(1)) }]
    });
    const source = result.filePaths[0];
    if (result.canceled || !source) return null;

    const extension = extname(source).toLowerCase();
    if (!BACKGROUNDS[extension]) return null;

    await clearBackground(event);
    await copyFile(source, backgroundBase() + extension);
    return findBackground();
}

export async function exportSettings(event: IpcMainInvokeEvent, json: string) {
    const result = await dialog.showSaveDialog({
        title: "ReCord settings",
        defaultPath: "record-settings.json",
        filters: [{ name: "JSON", extensions: ["json"] }]
    });
    if (result.canceled || !result.filePath) return false;
    await writeFile(result.filePath, json, "utf8");
    return true;
}

export async function importSettings(_: IpcMainInvokeEvent) {
    const result = await dialog.showOpenDialog({
        title: "ReCord settings",
        properties: ["openFile"],
        filters: [{ name: "JSON", extensions: ["json"] }]
    });
    if (result.canceled || !result.filePaths[0]) return null;
    return readFile(result.filePaths[0], "utf8");
}
