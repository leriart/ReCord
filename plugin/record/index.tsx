/*
 * RECORD, a Vencord userplugin
 * Companion for the RECORD theme: in-app theme settings, replaced Discord sounds and interface sounds.
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

import { definePluginSettings } from "@api/Settings";
import { Button } from "@components/Button";
import { Heading } from "@components/Heading";
import { Paragraph } from "@components/Paragraph";
import definePlugin, { OptionType, PluginNative } from "@utils/types";
import { find, wreq } from "@webpack";
import { React } from "@webpack/common";

interface Manifest {
    customSounds: Record<string, string>;
    ui: Record<string, string>;
}

type SoundContext = ((key: string) => string) & { keys(): string[]; resolve(key: string): unknown; };

const Native = VencordNative.pluginHelpers.ReCord as PluginNative<typeof import("./native")>;

const PRESETS = ["#e94221", "#dda052", "#3ddc97", "#4fb8c9", "#b58cff", "#ff5fa2"];

function AccentPicker() {
    const { accent } = settings.use(["accent"]);
    return (
        <section>
            <Heading>Accent color</Heading>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <input
                    type="color"
                    value={accent}
                    onChange={event => { settings.store.accent = event.currentTarget.value; applyTheme(); }}
                    style={{ width: 48, height: 32, padding: 0, border: "1px solid var(--border-subtle)", background: "none", cursor: "pointer" }}
                />
                {PRESETS.map(color => (
                    <button
                        key={color}
                        aria-label={color}
                        onClick={() => { settings.store.accent = color; applyTheme(); }}
                        style={{ width: 28, height: 28, background: color, border: color === accent ? "2px solid var(--text-default)" : "1px solid var(--border-subtle)", cursor: "pointer" }}
                    />
                ))}
                <Paragraph>{accent}</Paragraph>
            </div>
        </section>
    );
}

function BackgroundPicker() {
    const [busy, setBusy] = React.useState(false);
    const [, refresh] = React.useReducer((count: number) => count + 1, 0);

    const run = async (action: () => Promise<{ type: string; data: Uint8Array; } | null | void>) => {
        setBusy(true);
        try {
            const image = await action();
            if (image !== null) setBackground(image ?? null);
        } finally {
            setBusy(false);
            refresh();
        }
    };

    return (
        <section>
            <Heading>Background image</Heading>
            <Paragraph>
                Pick a picture from your computer. It sits behind the interface; use the two sliders below
                to control how dark it is and how see-through the panels are.
            </Paragraph>
            <div style={{ display: "flex", gap: 8, marginTop: 8, alignItems: "center" }}>
                <Button size="small" disabled={busy} onClick={() => run(() => Native.pickBackground())}>Choose image</Button>
                <Button size="small" variant="secondary" disabled={busy || !backgroundUrl} onClick={() => run(() => Native.clearBackground())}>Remove</Button>
                <Paragraph>{backgroundUrl ? "Image set" : "No image"}</Paragraph>
            </div>
        </section>
    );
}

function SoundFolder() {
    const [folder, setFolder] = React.useState("");
    React.useEffect(() => { void Native.getSoundFolder().then(setFolder); }, []);
    return (
        <section>
            <Heading>Your own sounds</Heading>
            <Paragraph>
                Audio files in this folder replace the bundled pack. Name a file after a pack sound
                (mention, receive, hover, select...) or a Discord event (message1, user_join, call_ringing...).
                WAV, OGG, MP3, FLAC and M4A are supported.
            </Paragraph>
            <Paragraph style={{ margin: "8px 0", userSelect: "text" }}>{folder}</Paragraph>
            <div style={{ display: "flex", gap: 8 }}>
                <Button size="small" onClick={() => Native.openSoundFolder()}>Open folder</Button>
                <Button size="small" variant="secondary" onClick={() => reloadSounds()}>Reload sounds</Button>
            </div>
        </section>
    );
}

const percent = (description: string, fallback: number) => ({
    type: OptionType.SLIDER as const,
    description,
    default: fallback,
    markers: [0, 25, 50, 75, 100],
    stickToMarkers: false,
    onChange: () => applyTheme()
});

const toggle = (description: string, fallback = true) => ({
    type: OptionType.BOOLEAN as const,
    description,
    default: fallback,
    onChange: () => applyTheme()
});

const choice = (description: string, options: Array<[string, string]>, fallback: string) => ({
    type: OptionType.SELECT as const,
    description,
    options: options.map(([label, value]) => ({ label, value, default: value === fallback })),
    onChange: () => applyTheme()
});

const FONTS: Record<string, string> = {
    pixel: '"Pixel Operator", "Pixel Operator Mono", "Courier New", monospace',
    mono: '"Pixel Operator Mono", "Pixel Operator", "Courier New", monospace',
    system: 'ui-monospace, "JetBrains Mono", "Cascadia Mono", "DejaVu Sans Mono", Consolas, monospace',
    discord: '"gg sans", "Noto Sans", "Helvetica Neue", Helvetica, Arial, sans-serif'
};

const settings = definePluginSettings({
    mode: choice("Color mode", [["Follow Discord appearance", "auto"], ["Dark (terminal)", "dark"], ["Light (paper)", "light"]], "auto"),
    accent: {
        type: OptionType.COMPONENT,
        default: "#e94221",
        component: AccentPicker
    },
    background: {
        type: OptionType.COMPONENT,
        component: BackgroundPicker
    },
    backgroundDim: percent("Background darkening (with an image)", 70),
    panelOpacity: percent("Panel opacity (lower shows more background)", 100),
    motionLevel: choice("Animations", [["Full (everything moves in steps)", "full"], ["Subtle (menus and dialogs only)", "subtle"], ["Off", "off"]], "full"),
    font: choice("Typeface", [["Pixel Operator", "pixel"], ["Pixel Operator Mono", "mono"], ["System monospace", "system"], ["Discord default", "discord"]], "pixel"),
    scanlines: percent("Scanline strength", 25),
    grain: percent("Film grain", 18),
    vignette: percent("Vignette", 55),
    flicker: toggle("CRT flicker", false),
    beam: toggle("Rolling scan beam"),
    frame: toggle("Corner brackets and screen frame"),
    pixelIcons: toggle("Pixel icons"),
    avatarFilter: toggle("Warm filter and scanlines on avatars"),
    baseUrl: {
        type: OptionType.STRING,
        description: "Sound pack folder (manifest.json and audio files)",
        default: "https://raw.githubusercontent.com/leriart/ReCord/main/sounds/",
        restartNeeded: true
    },
    soundFolder: {
        type: OptionType.COMPONENT,
        component: SoundFolder
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

let backgroundUrl: string | null = null;

function setBackground(image: { type: string; data: Uint8Array; } | null) {
    if (backgroundUrl) URL.revokeObjectURL(backgroundUrl);
    backgroundUrl = image ? URL.createObjectURL(new Blob([new Uint8Array(image.data)], { type: image.type })) : null;
    applyTheme();
}

function applyTheme() {
    const store = settings.store;
    if (store.mode === "dark" || store.mode === "light") document.documentElement.dataset.rlMode = store.mode;
    else delete document.documentElement.dataset.rlMode;

    let style = document.getElementById("record-config") as HTMLStyleElement | null;
    if (!style) {
        style = document.createElement("style");
        style.id = "record-config";
        document.head.append(style);
    }

    const rules = [
        `--rl-accent: ${/^#[0-9a-f]{6}$/i.test(store.accent) ? store.accent : "#e94221"}`,
        `--rl-scanline-opacity: ${store.scanlines / 100}`,
        `--rl-grain-opacity: ${store.grain / 100}`,
        `--rl-vignette-opacity: ${store.vignette / 100}`,
        `--rl-flicker-duration: ${store.flicker ? "6s" : "0s"}`,
        `--rl-icons: ${store.pixelIcons ? "on" : "off"}`,
        `--rl-motion: ${["full", "subtle", "off"].includes(store.motionLevel) ? store.motionLevel : "full"}`,
        `--rl-frame-opacity: ${store.frame ? 0.6 : 0}`,
        `--rl-beam-duration: ${store.beam && store.motionLevel !== "off" ? "9s" : "0s"}`,
        `--rl-beam-opacity: ${store.beam && store.motionLevel !== "off" ? 0.5 : 0}`,
        `--rl-font: ${FONTS[store.font] ?? FONTS.pixel}`,
        `--rl-font-display: ${FONTS[store.font] ?? FONTS.pixel}`,
        `--rl-background-dim: ${store.backgroundDim}%`,
        `--rl-surface: ${store.panelOpacity}%`
    ];
    if (backgroundUrl) rules.push(`--rl-background-image: url("${backgroundUrl}")`);
    if (!store.avatarFilter) rules.push("--rl-avatar-filter: none", "--rl-avatar-scanline: 0");

    style.textContent = `:root:root {\n${rules.map(rule => `    ${rule};`).join("\n")}\n}`;
}

const SEASONAL = /^(halloween|winter|asmr|bit|bop|ducky|lofi)_/;
const ALIASES: Record<string, string> = { defean: "deafen", undefean: "undeafen" };
const INTERACTIVE = 'a[href], button, [role="button"], [role="tab"], [role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"], [role="option"], [role="switch"], [role="listitem"], [role="treeitem"], [data-list-item-id]';

const blobs = new Map<string, string>();
const localBlobs = new Map<string, string>();
const localBuffers = new Map<string, AudioBuffer>();
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

const stem = (file: string) => file.replace(/\.[^.]+$/, "").toLowerCase();

function resolveSound(key: string) {
    if (!settings.store.replaceDiscord) return null;
    const name = key.replace(/^\.\//, "").replace(/\.mp3$/, "");
    const file = fileFor(name);
    return localBlobs.get(name) ?? (file && (localBlobs.get(stem(file)) ?? blobs.get(file))) ?? null;
}

async function reloadSounds() {
    for (const url of localBlobs.values()) URL.revokeObjectURL(url);
    localBlobs.clear();
    localBuffers.clear();

    try {
        for (const sound of await Native.readLocalSounds()) {
            const bytes = new Uint8Array(sound.data);
            localBlobs.set(sound.name, URL.createObjectURL(new Blob([bytes], { type: sound.type })));
            if (audio) localBuffers.set(sound.name, await audio.decodeAudioData(bytes.buffer.slice(0)));
        }
    } catch (error) {
        console.error("[ReCord] could not read the local sound folder", error);
    }
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
    const buffer = localBuffers.get(name) ?? (file && (localBuffers.get(stem(file)) ?? buffers.get(file)));
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
    name: "ReCord",
    description: "RECORD companion: theme settings (dark or light, accent, background, CRT, icons, animations, typeface), replaced Discord sounds and interface sounds",
    authors: [{ name: "leriart", id: 0n }],
    settings,

    async start() {
        applyTheme();
        void Native.readBackground().then(setBackground).catch(() => { });

        try {
            await load();
        } catch (error) {
            console.error("[ReCord] could not load the sound pack", error);
            audio ??= new AudioContext();
            manifest ??= { customSounds: {}, ui: {} };
        }
        await reloadSounds();

        hookDiscordSounds();
        hookInterface();
        if (settings.store.bootSound) play("boot");
    },

    stop() {
        document.getElementById("record-config")?.remove();
        delete document.documentElement.dataset.rlMode;
        if (backgroundUrl) URL.revokeObjectURL(backgroundUrl);
        backgroundUrl = null;
        for (const url of localBlobs.values()) URL.revokeObjectURL(url);
        localBlobs.clear();
        localBuffers.clear();
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
