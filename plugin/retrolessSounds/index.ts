/*
 * RETROLESS Sounds, a Vencord userplugin
 * Replaces Discord's sounds with the RETROLESS signal pack and adds interface sounds.
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

import { definePluginSettings } from "@api/Settings";
import definePlugin, { OptionType } from "@utils/types";
import { find, wreq } from "@webpack";

interface Manifest {
    customSounds: Record<string, string>;
    ui: Record<string, string>;
}

type SoundContext = ((key: string) => string) & { keys(): string[]; resolve(key: string): unknown; };

const settings = definePluginSettings({
    baseUrl: {
        type: OptionType.STRING,
        description: "Folder that holds manifest.json and the WAV files",
        default: "https://raw.githubusercontent.com/leriart/Retroless/main/sounds/",
        restartNeeded: true
    },
    replaceDiscord: {
        type: OptionType.BOOLEAN,
        description: "Replace Discord sounds (messages, mentions, calls, voice, streams)",
        default: true
    },
    interfaceSounds: {
        type: OptionType.BOOLEAN,
        description: "Play interface sounds (hover, select, back, menus, navigation)",
        default: true
    },
    hoverSounds: {
        type: OptionType.BOOLEAN,
        description: "Play a tick when the pointer enters a control",
        default: true
    },
    typingSounds: {
        type: OptionType.BOOLEAN,
        description: "Play key ticks while typing a message",
        default: true
    },
    bootSound: {
        type: OptionType.BOOLEAN,
        description: "Play the boot signal when Discord starts",
        default: true
    },
    volume: {
        type: OptionType.SLIDER,
        description: "Interface sound volume",
        default: 45,
        markers: [0, 25, 50, 75, 100],
        stickToMarkers: false
    }
});

const SEASONAL = /^(halloween|winter|asmr|bit|bop|ducky|lofi)_/;
const ALIASES: Record<string, string> = { defean: "deafen", undefean: "undeafen" };
const INTERACTIVE = 'a[href], button, [role="button"], [role="tab"], [role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"], [role="option"], [role="switch"], [role="listitem"], [role="treeitem"], [data-list-item-id]';

const blobs = new Map<string, string>();
const buffers = new Map<string, AudioBuffer>();
const disposers: Array<() => void> = [];
const lastPlayed = new Map<string, number>();

let manifest: Manifest | null = null;
let audio: AudioContext | null = null;
let original: SoundContext | null = null;
let moduleId: string | null = null;
let hovered: Element | null = null;
let layers = 0;

function fileFor(name: string) {
    if (!manifest) return null;
    const base = name.replace(SEASONAL, "");
    return manifest.customSounds[name] ?? manifest.customSounds[base] ?? manifest.customSounds[ALIASES[base] ?? ""] ?? null;
}

function resolveSound(key: string) {
    const name = key.replace(/^\.\//, "").replace(/\.mp3$/, "");
    const file = settings.store.replaceDiscord ? fileFor(name) : null;
    return (file && blobs.get(file)) || null;
}

async function load() {
    const base = settings.store.baseUrl.replace(/\/?$/, "/");
    manifest = await (await fetch(base + "manifest.json")).json() as Manifest;
    audio = new AudioContext();

    const files = new Set([...Object.values(manifest.customSounds), ...Object.values(manifest.ui)]);
    await Promise.all([...files].map(async file => {
        try {
            const response = await fetch(base + file);
            if (!response.ok) return;
            const data = await response.arrayBuffer();
            blobs.set(file, URL.createObjectURL(new Blob([data], { type: "audio/wav" })));
            buffers.set(file, await audio!.decodeAudioData(data.slice(0)));
        } catch { }
    }));
}

function play(name: string, gap = 0) {
    const file = manifest?.ui[name];
    const buffer = file && buffers.get(file);
    if (!buffer || !audio || !settings.store.interfaceSounds) return;

    const now = performance.now();
    if (gap && now - (lastPlayed.get(name) ?? 0) < gap) return;
    lastPlayed.set(name, now);

    if (audio.state === "suspended") void audio.resume();
    const source = audio.createBufferSource();
    const gain = audio.createGain();
    gain.gain.value = settings.store.volume / 100;
    source.buffer = buffer;
    source.connect(gain).connect(audio.destination);
    source.start();
}

function hookDiscordSounds() {
    const context = find(m => {
        try {
            return typeof m === "function" && typeof m.keys === "function" && typeof m.resolve === "function" && m.keys().includes("./message1.mp3");
        } catch {
            return false;
        }
    }) as SoundContext | undefined;
    if (!context) return;

    moduleId = Object.keys(wreq.c).find(id => wreq.c[id]?.exports === context) ?? null;
    if (!moduleId) return;

    original = context;
    const replacement = ((key: string) => resolveSound(key) ?? context(key)) as SoundContext;
    replacement.keys = () => context.keys();
    replacement.resolve = key => context.resolve(key);
    wreq.c[moduleId].exports = replacement;
}

function listen<K extends keyof DocumentEventMap>(type: K, handler: (event: DocumentEventMap[K]) => void) {
    document.addEventListener(type, handler, true);
    disposers.push(() => document.removeEventListener(type, handler, true));
}

function hookInterface() {
    listen("pointerover", event => {
        if (!settings.store.hoverSounds) return;
        const target = (event.target as Element | null)?.closest?.(INTERACTIVE) ?? null;
        if (target === hovered) return;
        hovered = target;
        if (target) play("hover", 45);
    });

    listen("click", event => {
        const target = event.target as Element | null;
        if (!target?.closest) return;
        if (target.closest('[aria-label="Close"], [aria-label="Cerrar"], [class*="closeButton_"], [class*="backdrop_"]')) return play("back", 60);
        if (target.closest('[role="switch"], [role="checkbox"], [role="radio"], input[type="checkbox"]')) return play("toggle", 60);
        if (target.closest('a[data-list-item-id^="channels___"], [data-list-item-id^="guildsnav___"], [data-list-item-id^="private-channels"], [role="tab"]')) return play("navigate", 60);
        if (target.closest(INTERACTIVE)) play("select", 60);
    });

    listen("keydown", event => {
        const target = event.target as HTMLElement | null;
        const editing = !!target && (target.isContentEditable || /^(INPUT|TEXTAREA)$/.test(target.tagName));
        if (event.key === "Escape") return play("back", 80);
        if (!editing) return;
        if (event.key === "Enter" && !event.shiftKey && target!.closest('[class*="channelTextArea_"]')) return play("send", 80);
        if (settings.store.typingSounds && (event.key.length === 1 || event.key === "Backspace")) play("type", 28);
    });

    const observer = new MutationObserver(() => {
        const count = document.querySelectorAll('[role="dialog"], [role="menu"], [class*="layer_"][class*="baseLayer_"] ~ [class*="layer_"]').length;
        if (count > layers) play("open", 80);
        else if (count < layers) play("close", 80);
        layers = count;
    });
    observer.observe(document.body, { childList: true, subtree: true });
    disposers.push(() => observer.disconnect());
}

export default definePlugin({
    name: "RetrolessSounds",
    description: "Replaces Discord sounds with the RETROLESS signal pack and adds terminal interface sounds",
    authors: [{ name: "leriart", id: 0n }],
    settings,

    async start() {
        try {
            await load();
        } catch (error) {
            console.error("[RetrolessSounds] could not load the sound pack", error);
            return;
        }

        hookDiscordSounds();
        hookInterface();
        if (settings.store.bootSound) play("boot");
    },

    stop() {
        for (const dispose of disposers.splice(0)) dispose();
        if (moduleId && original) wreq.c[moduleId].exports = original;
        for (const url of blobs.values()) URL.revokeObjectURL(url);
        blobs.clear();
        buffers.clear();
        void audio?.close();
        audio = null;
        original = null;
        moduleId = null;
        manifest = null;
    }
});
