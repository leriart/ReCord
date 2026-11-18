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
    sets?: Record<string, { label: string; sounds: Record<string, string>; }>;
}

type SoundContext = ((key: string) => string) & { keys(): string[]; resolve(key: string): unknown; };

const Native = VencordNative.pluginHelpers.ReCord as PluginNative<typeof import("./native")>;

const ACCENT_PRESETS = ["#e94221", "#dda052", "#3ddc97", "#4fb8c9", "#b58cff", "#ff5fa2"];

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
                {ACCENT_PRESETS.map(color => (
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

function colorSetting(key: "backgroundColor" | "textColor", title: string, note: string) {
    return function ColorSetting() {
        const store = settings.use([key, "customColors"]);
        return (
            <section>
                <Heading>{title}</Heading>
                <div style={{ display: "flex", alignItems: "center", gap: 8, opacity: store.customColors ? 1 : 0.5 }}>
                    <input
                        type="color"
                        value={store[key]}
                        disabled={!store.customColors}
                        onChange={event => { settings.store[key] = event.currentTarget.value; applyTheme(); }}
                        style={{ width: 48, height: 32, padding: 0, border: "1px solid var(--border-subtle)", background: "none", cursor: "pointer" }}
                    />
                    <Paragraph>{store[key]} {note}</Paragraph>
                </div>
            </section>
        );
    };
}

function SoundList() {
    const { disabledSounds, soundSources } = settings.use(["disabledSounds", "uiSet", "soundSources"]);
    const [, refresh] = React.useReducer((count: number) => count + 1, 0);
    React.useEffect(() => {
        const timer = setInterval(() => { if (manifest) { clearInterval(timer); refresh(); } }, 500);
        return () => clearInterval(timer);
    }, []);

    if (!manifest) return <Paragraph>The sound pack is still loading.</Paragraph>;
    const pack = manifest;

    const disabled = new Set(disabledSounds.split(",").filter(Boolean));
    const flip = (key: string) => {
        if (disabled.has(key)) disabled.delete(key); else disabled.add(key);
        settings.store.disabledSounds = [...disabled].join(",");
    };

    const sources = { ...parseSources(soundSources) };
    const choose = (name: string, value: string) => {
        if (value) sources[name] = value; else delete sources[name];
        settings.store.soundSources = JSON.stringify(sources);
        void loadNeeded();
    };

    const events = new Map<string, string[]>();
    for (const [event, file] of Object.entries(pack.customSounds)) {
        events.set(file, [...(events.get(file) ?? []), event]);
    }

    const row = (key: string, name: string, detail: string, fallback: string) => (
        <div key={key} style={{ display: "flex", alignItems: "center", gap: 8, padding: "4px 0" }}>
            <input type="checkbox" checked={!disabled.has(key)} onChange={() => flip(key)} />
            <span style={{ flex: "0 0 96px", color: "var(--text-default)" }}>{name}</span>
            <select
                value={sources[name] ?? ""}
                onChange={event => choose(name, event.currentTarget.value)}
                style={{ flex: "0 0 150px", background: "var(--input-background-default, #000)", color: "var(--text-default)", border: "1px solid var(--border-subtle)", padding: "2px 4px", font: "inherit", fontSize: 12 }}
            >
                <option value="">(sound theme)</option>
                <option value="synth">Synth</option>
                {Object.entries(pack.sets ?? {}).filter(([, set]) => set.sounds[name]).map(([id, set]) => <option key={id} value={id}>{set.label}</option>)}
            </select>
            <span style={{ flex: 1, minWidth: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", color: "var(--text-muted)", fontSize: 12 }}>{detail}</span>
            <Button size="small" variant="secondary" onClick={() => { void preview(name, fallback); }}>Play</Button>
        </div>
    );

    return (
        <section>
            <Heading>Interface sounds / Sonidos de interfaz</Heading>
            <Paragraph>Untick to silence a sound. The list picks a different theme for that one sound.</Paragraph>
            {Object.entries(pack.ui).map(([name, file]) => row(`ui:${name}`, name, "", file))}
            <Heading style={{ marginTop: 16 }}>Discord sounds / Sonidos de Discord</Heading>
            <Paragraph>Untick to get Discord's original back for those events.</Paragraph>
            {[...events].map(([file, names]) => row(`discord:${stem(file)}`, stem(file), names.join(", "), file))}
        </section>
    );
}

const PRESETS: Record<string, { accent: string; mode: string; customColors: boolean; backgroundColor?: string; textColor?: string; }> = {
    amber: { accent: "#e94221", mode: "dark", customColors: false },
    phosphor: { accent: "#3ddc97", mode: "dark", customColors: false },
    ice: { accent: "#4fb8c9", mode: "dark", customColors: false },
    paper: { accent: "#b8401f", mode: "light", customColors: false },
    terminal: { accent: "#3ddc97", mode: "dark", customColors: true, backgroundColor: "#020a05", textColor: "#b8f5cf" },
    custom: { accent: "#e94221", mode: "auto", customColors: false }
};

function Presets() {
    const [name, setName] = React.useState("amber");
    return (
        <section>
            <Heading>Palette presets / Paletas listas</Heading>
            <Paragraph>One click sets the accent, the dark or light mode, and the custom colors.</Paragraph>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 8 }}>
                {Object.keys(PRESETS).map(key => (
                    <Button
                        key={key}
                        size="small"
                        variant={key === name ? "primary" : "secondary"}
                        onClick={() => {
                            setName(key);
                            Object.assign(settings.store, PRESETS[key]);
                            applyTheme();
                        }}
                    >
                        {key}
                    </Button>
                ))}
            </div>
        </section>
    );
}

function SettingsFile() {
    const [message, setMessage] = React.useState("");
    return (
        <section>
            <Heading>Backup / Copia de seguridad</Heading>
            <Paragraph>Save every ReCord setting to a file, or load them on another computer.</Paragraph>
            <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
                <Button size="small" onClick={async () => {
                    const keys = Object.keys(settings.def);
                    const data = Object.fromEntries(keys.map(key => [key, settings.store[key]]));
                    setMessage(await Native.exportSettings(JSON.stringify(data, null, 4)) ? "Saved / Guardado" : "Cancelled / Cancelado");
                }}>Export / Exportar</Button>
                <Button size="small" variant="secondary" onClick={async () => {
                    const text = await Native.importSettings();
                    if (!text) return setMessage("Cancelled / Cancelado");
                    try {
                        const data = JSON.parse(text);
                        for (const [key, value] of Object.entries(data)) if (key in settings.def) (settings.store as any)[key] = value;
                        applyTheme();
                        setMessage("Imported / Importado");
                    } catch {
                        setMessage("Invalid file / Archivo no válido");
                    }
                }}>Import / Importar</Button>
                <Paragraph>{message}</Paragraph>
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
            const media = await action();
            if (media !== null) setBackground(media ?? null);
        } finally {
            setBusy(false);
            refresh();
        }
    };

    return (
        <section>
            <Heading>Background / Fondo</Heading>
            <Paragraph>
                Pick an image, GIF or video. Images and GIFs sit behind the interface; videos play muted on a loop.
                A 1080p (or smaller) video runs much smoother than a 4K one.
                Use the two sliders below to control how dark it is and how see-through the panels are.
                Elige una imagen, GIF o vídeo. Las imágenes y GIFs quedan detrás; los vídeos se reproducen en bucle y sin sonido.
                Un vídeo de 1080p o menos va mucho más fluido que uno en 4K.
            </Paragraph>
            <div style={{ display: "flex", gap: 8, marginTop: 8, alignItems: "center" }}>
                <Button size="small" disabled={busy} onClick={() => run(() => Native.pickBackground())}>Choose file / Elegir archivo</Button>
                <Button size="small" variant="secondary" disabled={busy || !backgroundUrl} onClick={() => run(() => Native.clearBackground())}>Remove / Quitar</Button>
                <Paragraph>{backgroundUrl ? "Background set / Fondo puesto" : "No background / Sin fondo"}</Paragraph>
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
    presets: {
        type: OptionType.COMPONENT,
        component: Presets
    },
    settingsFile: {
        type: OptionType.COMPONENT,
        component: SettingsFile
    },
    mode: choice("Color mode / Modo de color", [["Follow Discord appearance", "auto"], ["Dark (terminal)", "dark"], ["Light (paper)", "light"]], "auto"),
    accent: {
        type: OptionType.COMPONENT,
        default: "#e94221",
        component: AccentPicker
    },
    customColors: toggle("Custom colors / Colores propios en vez de la paleta oscura o clara", false),
    backgroundColor: {
        type: OptionType.COMPONENT,
        default: "#050605",
        component: colorSetting("backgroundColor", "Background color", "(panels are derived from it)")
    },
    textColor: {
        type: OptionType.COMPONENT,
        default: "#f0dec6",
        component: colorSetting("textColor", "Text color", "(secondary text and borders are derived from it)")
    },
    background: {
        type: OptionType.COMPONENT,
        component: BackgroundPicker
    },
    backgroundDim: percent("Background darkening / Oscurecer el fondo (imagen o vídeo)", 50),
    panelOpacity: percent("Panel opacity / Opacidad de paneles (menos, más fondo)", 75),
    motionLevel: choice("Animations / Animaciones", [["Full (everything moves in steps)", "full"], ["Subtle (menus and dialogs only)", "subtle"], ["Off", "off"]], "full"),
    font: choice("Typeface / Tipografía", [["Pixel Operator", "pixel"], ["Pixel Operator Mono", "mono"], ["System monospace", "system"], ["Discord default", "discord"]], "pixel"),
    scanlines: percent("Scanline strength", 25),
    grain: percent("Film grain", 18),
    vignette: percent("Vignette", 55),
    lowPower: toggle("Low power / Bajo consumo: no scan beam, grain, flicker, constant animations, profile effects or video banners", false),
    flicker: toggle("CRT flicker", false),
    beam: toggle("Rolling scan beam"),
    frame: toggle("Corner brackets and screen frame"),
    pixelIcons: toggle("Pixel icons"),
    avatarFilter: toggle("Warm filter and scanlines on avatars"),
    baseUrl: {
        type: OptionType.STRING,
        description: "Sound pack folder / Carpeta del pack de sonidos",
        default: "https://raw.githubusercontent.com/leriart/ReCord/main/sounds/",
        restartNeeded: true
    },
    soundFolder: {
        type: OptionType.COMPONENT,
        component: SoundFolder
    },
    replaceDiscord: {
        type: OptionType.BOOLEAN,
        description: "Replace Discord sounds / Sustituir sonidos de Discord",
        default: true
    },
    interfaceSounds: {
        type: OptionType.BOOLEAN,
        description: "Interface sounds / Sonidos de interfaz",
        default: true
    },
    hoverSounds: {
        type: OptionType.BOOLEAN,
        description: "Hover tick / Tic al pasar el cursor",
        default: true
    },
    typingSounds: {
        type: OptionType.BOOLEAN,
        description: "Typing ticks / Tics al escribir",
        default: true
    },
    bootSound: {
        type: OptionType.BOOLEAN,
        description: "Boot signal / Señal de arranque",
        default: true
    },
    uiSet: {
        type: OptionType.SELECT,
        description: "Sound theme / Tema de sonido (interface and Discord sounds)",
        options: [
            { label: "Synth (original terminal blips)", value: "synth", default: true },
            { label: "Kenney UI SFX (clicks, switches)", value: "kenney" },
            { label: "Kenney Interface (ticks, plucks)", value: "kenney-interface" },
            { label: "UI SFX Arcade", value: "arcade" },
            { label: "UI SFX Sci-fi", value: "scifi" },
            { label: "UI SFX Mechanical", value: "mechanical" },
            { label: "UI SFX Minimal", value: "minimal" },
            { label: "UI SFX Glass", value: "glass" },
            { label: "UI SFX Cinematic", value: "cinematic" },
            { label: "UI SFX Studio", value: "studio" },
            { label: "UI SFX Soft", value: "soft" },
            { label: "UI SFX Rubber", value: "rubber" },
            { label: "UI SFX Organic", value: "organic" },
            { label: "UI SFX Dreamy", value: "dreamy" },
            { label: "UI SFX Zen", value: "zen" }
        ],
        onChange: () => { void loadNeeded(); }
    },
    soundSources: {
        type: OptionType.STRING,
        description: "Per-sound themes (managed by the list below)",
        default: "{}",
        hidden: true
    },
    soundList: {
        type: OptionType.COMPONENT,
        component: SoundList
    },
    disabledSounds: {
        type: OptionType.STRING,
        description: "Disabled sounds / Sonidos desactivados (gestionados por la lista)",
        default: "",
        hidden: true
    },
    discordVolume: {
        type: OptionType.SLIDER,
        description: "Discord sounds volume / Volumen de los sonidos de Discord",
        default: 100,
        markers: [0, 25, 50, 75, 100],
        stickToMarkers: false,
        onChange: () => rebuildBlobs()
    },
    volume: {
        type: OptionType.SLIDER,
        description: "Interface volume / Volumen de interfaz",
        default: 45,
        markers: [0, 25, 50, 75, 100],
        stickToMarkers: false
    }
});

let backgroundUrl: string | null = null;
let backgroundKind: "image" | "video" | null = null;
let videoPausedByVisibility = false;

function syncBackgroundVideo(url: string | null) {
    let layer = document.getElementById("record-background-video");
    if (!url) {
        layer?.remove();
        videoPausedByVisibility = false;
        return;
    }
    if (!document.body) return;
    if (!layer) {
        layer = document.createElement("div");
        layer.id = "record-background-video";
        const video = document.createElement("video");
        video.autoplay = true;
        video.loop = true;
        video.muted = true;
        video.playsInline = true;
        video.controls = false;
        video.setAttribute("aria-hidden", "true");
        video.setAttribute("disablepictureinpicture", "");
        layer.append(video);
        document.body.append(layer);
    }
    const video = layer.querySelector("video");
    if (!video) return;
    if (video.getAttribute("src") !== url) video.src = url;
    if (document.hidden) {
        video.pause();
        videoPausedByVisibility = true;
    } else if (video.paused) {
        videoPausedByVisibility = false;
        void video.play().catch(() => { });
    }
}

function setBackground(media: { type: string; data: Uint8Array; } | null) {
    const previous = backgroundUrl;
    backgroundUrl = media ? URL.createObjectURL(new Blob([new Uint8Array(media.data)], { type: media.type })) : null;
    backgroundKind = media ? (media.type.startsWith("video/") ? "video" : "image") : null;
    applyTheme();
    if (previous) URL.revokeObjectURL(previous);
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
    // Low power keeps the look but drops everything that repaints all the time,
    // which is what hurts when the client composites on the CPU.
    if (store.lowPower) {
        rules.push(
            "--rl-beam-duration: 0s",
            "--rl-beam-opacity: 0",
            "--rl-flicker-duration: 0s",
            "--rl-scanline-opacity: 0",
            "--rl-grain-opacity: 0",
            "--rl-vignette-opacity: 0",
            "--rl-avatar-filter: none",
            "--rl-avatar-scanline: 0",
            "--rl-lite: on",
            `--rl-motion: ${store.motionLevel === "off" ? "off" : "subtle"}`
        );
    }

    // The CSS only paints the beam/flicker when these attributes are present;
    // an off effect must not keep a full-screen compositor layer alive.
    const root = document.documentElement;
    root.toggleAttribute("data-rl-beam", store.beam && store.motionLevel !== "off" && !store.lowPower);
    root.toggleAttribute("data-rl-flicker", store.flicker && store.motionLevel !== "off" && !store.lowPower);

    if (backgroundUrl && backgroundKind === "image") rules.push(`--rl-background-image: url("${backgroundUrl}")`);
    else rules.push("--rl-background-image: none");

    const videoUrl = backgroundKind === "video" ? backgroundUrl : null;
    if (backgroundKind) document.documentElement.dataset.rlBackground = backgroundKind;
    else delete document.documentElement.dataset.rlBackground;
    syncBackgroundVideo(videoUrl);

    const hex = /^#[0-9a-f]{6}$/i;
    if (store.customColors && hex.test(store.backgroundColor) && hex.test(store.textColor)) {
        const bg = store.backgroundColor;
        const fg = store.textColor;
        const surface = (amount: number) => `color-mix(in srgb, ${fg} ${amount}%, ${bg})`;
        const channel = (offset: number) => parseInt(bg.slice(offset, offset + 2), 16);
        const light = channel(1) * 0.299 + channel(3) * 0.587 + channel(5) * 0.114 > 140;
        rules.push(
            `color-scheme: ${light ? "light" : "dark"}`,
            `--rl-tint: ${fg}`,
            `--rl-void: ${bg}`,
            `--rl-ink-base: ${surface(2)}`,
            `--rl-coal-base: ${surface(4)}`,
            `--rl-panel-base: ${surface(6)}`,
            `--rl-raised-base: ${surface(9)}`,
            `--rl-high-base: ${surface(13)}`,
            `--rl-higher-base: ${surface(17)}`,
            `--rl-line: ${surface(24)}`,
            `--rl-cream: ${fg}`,
            `--rl-bone: ${surface(90)}`,
            `--rl-paper: ${surface(82)}`,
            `--rl-smoke: ${surface(62)}`,
            `--rl-ash: ${surface(50)}`,
            `--rl-faint: ${surface(38)}`
        );
    }
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

// Both settings are strings that change rarely but are read on every sound,
// so the parsed form is kept until the string itself changes.
let sourcesText = "";
let sourcesValue: Record<string, string> = {};

function parseSources(text: string): Record<string, string> {
    if (text === sourcesText) return sourcesValue;
    sourcesText = text;
    try {
        const value = JSON.parse(text || "{}");
        sourcesValue = value && typeof value === "object" ? value : {};
    } catch {
        sourcesValue = {};
    }
    return sourcesValue;
}

// A sound comes from the theme chosen for it, or from the global sound theme,
// or from the synthesized base pack when the theme has no file for it.
function themedFile(name: string, fallback?: string) {
    const source = parseSources(settings.store.soundSources)[name] ?? settings.store.uiSet;
    return manifest?.sets?.[source]?.sounds[name] ?? fallback;
}

const uiFile = (name: string) => themedFile(name, manifest?.ui[name]);
let disabledText = "";
let disabledSet = new Set<string>();

function isDisabled(key: string) {
    const text = settings.store.disabledSounds;
    if (text !== disabledText) {
        disabledText = text;
        disabledSet = new Set(text.split(","));
    }
    return disabledSet.has(key);
}

function blobFor(file: string) {
    const cached = blobs.get(file);
    if (cached) return cached;
    const buffer = buffers.get(file);
    if (!buffer) return null;
    const url = URL.createObjectURL(encodeWav(buffer, settings.store.discordVolume / 100));
    blobs.set(file, url);
    return url;
}

function resolveSound(key: string) {
    if (!settings.store.replaceDiscord) return null;
    const name = key.replace(/^\.\//, "").replace(/\.mp3$/, "");
    const base = fileFor(name);
    if (!base) return localBlobs.get(name) ?? null;
    if (isDisabled(`discord:${stem(base)}`)) return null;
    const file = themedFile(stem(base), base)!;
    return localBlobs.get(name) ?? localBlobs.get(stem(base)) ?? blobFor(file) ?? blobFor(base);
}

// Discord plays its sounds through its own Audio element, so the only way to
// set their level is to hand it audio that is already scaled.
function encodeWav(buffer: AudioBuffer, gain: number) {
    const channels = buffer.numberOfChannels;
    const frames = buffer.length;
    const view = new DataView(new ArrayBuffer(44 + frames * channels * 2));
    const text = (offset: number, value: string) => { for (let i = 0; i < value.length; i++) view.setUint8(offset + i, value.charCodeAt(i)); };

    text(0, "RIFF");
    view.setUint32(4, 36 + frames * channels * 2, true);
    text(8, "WAVEfmt ");
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, channels, true);
    view.setUint32(24, buffer.sampleRate, true);
    view.setUint32(28, buffer.sampleRate * channels * 2, true);
    view.setUint16(32, channels * 2, true);
    view.setUint16(34, 16, true);
    text(36, "data");
    view.setUint32(40, frames * channels * 2, true);

    const data = Array.from({ length: channels }, (_, channel) => buffer.getChannelData(channel));
    let offset = 44;
    for (let frame = 0; frame < frames; frame++) {
        for (let channel = 0; channel < channels; channel++) {
            const sample = Math.max(-1, Math.min(1, data[channel][frame] * gain));
            view.setInt16(offset, sample * 32767, true);
            offset += 2;
        }
    }
    return new Blob([view.buffer], { type: "audio/wav" });
}

function rebuildBlobs() {
    for (const url of blobs.values()) URL.revokeObjectURL(url);
    blobs.clear();
    for (const url of localBlobs.values()) URL.revokeObjectURL(url);
    localBlobs.clear();
    const gain = settings.store.discordVolume / 100;
    for (const [name, buffer] of localBuffers) localBlobs.set(name, URL.createObjectURL(encodeWav(buffer, gain)));
}

async function reloadSounds() {
    localBuffers.clear();
    try {
        for (const sound of await Native.readLocalSounds()) {
            const bytes = new Uint8Array(sound.data);
            if (audio) localBuffers.set(sound.name, await audio.decodeAudioData(bytes.buffer.slice(0)));
        }
    } catch (error) {
        console.error("[ReCord] could not read the local sound folder", error);
    }
    rebuildBlobs();
}

const loading = new Map<string, Promise<void>>();

function ensure(file: string) {
    if (buffers.has(file)) return Promise.resolve();
    let task = loading.get(file);
    if (!task) {
        const base = settings.store.baseUrl.replace(/\/?$/, "/");
        task = (async () => {
            try {
                const response = await fetch(base + file);
                if (response.ok && audio) buffers.set(file, await audio.decodeAudioData(await response.arrayBuffer()));
            } catch { }
            loading.delete(file);
        })();
        loading.set(file, task);
    }
    return task;
}

// Only the files the current configuration can play are fetched, so adding
// more sound themes does not slow the start down.
function loadNeeded() {
    if (!manifest) return Promise.resolve();
    const files = new Set<string>();
    for (const [name, file] of Object.entries(manifest.ui)) {
        files.add(file);
        files.add(themedFile(name, file)!);
    }
    for (const file of Object.values(manifest.customSounds)) {
        files.add(file);
        files.add(themedFile(stem(file), file)!);
    }
    return Promise.all([...files].map(ensure)).then(() => { });
}

async function load() {
    const base = settings.store.baseUrl.replace(/\/?$/, "/");
    manifest = await (await fetch(base + "manifest.json")).json() as Manifest;
    audio = new AudioContext();
    await loadNeeded();
}

function output(buffer: AudioBuffer) {
    if (!audio) return;
    if (audio.state === "suspended") void audio.resume();
    const source = audio.createBufferSource();
    const gain = audio.createGain();
    gain.gain.value = settings.store.volume / 100;
    source.buffer = buffer;
    source.connect(gain).connect(audio.destination);
    source.start();
}

async function preview(name: string, fallback: string) {
    const local = localBuffers.get(name) ?? localBuffers.get(stem(fallback));
    if (local) return output(local);
    const file = themedFile(name, fallback) ?? fallback;
    await ensure(file);
    const buffer = buffers.get(file) ?? buffers.get(fallback);
    if (buffer) output(buffer);
}

function play(name: string, gap = 0) {
    if (!settings.store.interfaceSounds || isDisabled(`ui:${name}`)) return;
    const file = uiFile(name);
    const buffer = localBuffers.get(name) ?? (file && buffers.get(file));
    if (!buffer) return;

    const now = performance.now();
    if (gap && now - (lastPlayed.get(name) ?? 0) < gap) return;
    lastPlayed.set(name, now);
    output(buffer);
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
    const options = { capture: true, passive: true };
    document.addEventListener(type, handler, options);
    disposers.push(() => document.removeEventListener(type, handler, options));
}

function hookInterface() {
    let lastTarget: EventTarget | null = null;

    listen("pointerover", event => {
        // The pointer crosses many nodes inside one control; only a new node is worth a lookup.
        if (event.target === lastTarget) return;
        lastTarget = event.target;
        if (!settings.store.hoverSounds || !settings.store.interfaceSounds) return;
        const target = (event.target as Element | null)?.closest?.(INTERACTIVE) ?? null;
        if (target === hovered) return;
        hovered = target;
        if (target) play("hover", 45);
    });

    listen("click", event => {
        if (!settings.store.interfaceSounds) return;
        const target = event.target as Element | null;
        if (!target?.closest) return;
        if (target.closest('[aria-label="Close"], [aria-label="Cerrar"], [class*="closeButton_"], [class*="backdrop_"]')) return play("back", 60);
        if (target.closest('[role="switch"], [role="checkbox"], [role="radio"], input[type="checkbox"]')) return play("toggle", 60);
        if (target.closest('a[data-list-item-id^="channels___"], [data-list-item-id^="guildsnav___"], [data-list-item-id^="private-channels"], [role="tab"]')) return play("navigate", 60);
        if (target.closest(INTERACTIVE)) play("select", 60);
    });

    listen("keydown", event => {
        if (!settings.store.interfaceSounds) return;
        if (event.key === "Escape") return play("back", 80);
        const target = event.target as HTMLElement | null;
        if (!target || !(target.isContentEditable || target.tagName === "INPUT" || target.tagName === "TEXTAREA")) return;
        if (event.key === "Enter" && !event.shiftKey && target.closest('[class*="channelTextArea_"]')) return play("send", 80);
        if (settings.store.typingSounds && (event.key.length === 1 || event.key === "Backspace")) play("type", 28);
    });

    // Discord mutates the DOM constantly. Menus and dialogs are counted at most
    // once per frame, and only when something was actually added or removed.
    let scheduled = false;
    const check = () => {
        scheduled = false;
        const count = document.querySelectorAll('[role="dialog"], [role="menu"]').length;
        if (count > layers) play("open", 80);
        else if (count < layers) play("close", 80);
        layers = count;
    };
    const observer = new MutationObserver(records => {
        if (scheduled || !settings.store.interfaceSounds) return;
        for (const record of records) {
            if (record.addedNodes.length || record.removedNodes.length) {
                scheduled = true;
                requestAnimationFrame(check);
                return;
            }
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
    disposers.push(() => observer.disconnect());
}

function hookBackgroundVideo() {
    // A looping wallpaper keeps decoding even while the window is hidden.
    listen("visibilitychange", () => {
        const video = document.querySelector<HTMLVideoElement>("#record-background-video video");
        if (!video) return;
        if (document.hidden) {
            if (!video.paused) {
                video.pause();
                videoPausedByVisibility = true;
            }
        } else if (videoPausedByVisibility) {
            videoPausedByVisibility = false;
            void video.play().catch(() => { });
        }
    });
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
        hookBackgroundVideo();
        if (settings.store.bootSound) play("boot");
    },

    stop() {
        document.getElementById("record-config")?.remove();
        document.getElementById("record-background-video")?.remove();
        delete document.documentElement.dataset.rlMode;
        delete document.documentElement.dataset.rlBackground;
        delete document.documentElement.dataset.rlBeam;
        delete document.documentElement.dataset.rlFlicker;
        videoPausedByVisibility = false;
        if (backgroundUrl) URL.revokeObjectURL(backgroundUrl);
        backgroundUrl = null;
        backgroundKind = null;
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
