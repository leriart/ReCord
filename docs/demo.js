const $ = id => document.getElementById(id);
const app = document.querySelector(".app");
const messages = document.querySelector(".messages");
const translate = text => (window.t ? window.t(text) : text);

const INTERACTIVE = ".channel, .dm, .server, .server-add, .member, .reaction, .user-actions button, .chat-actions span, .composer-tools span, .attachment-action, .code-copy, .demo-bar button, .demo-bar select";
const REPLIES = [
    "Copy. Signal is clean on my side.",
    "Logged. Moving to the next node.",
    "Received. Keep the channel open.",
    "Acknowledged. No trace on the relay."
];

let manifest = null;
let audio = null;
let hovered = null;
let replyIndex = 0;
const buffers = new Map();
const loading = new Map();
const lastPlayed = new Map();

// Same resolution as the plugin: the chosen sound theme first, then the
// synthesized pack when the theme has no file for that sound.
function fileFor(name) {
    if (!manifest) return null;
    const base = manifest.ui[name] ?? `${name}.wav`;
    return manifest.sets?.[$("demo-set").value]?.sounds[name] ?? base;
}

function ensure(file) {
    if (buffers.has(file) || !audio) return Promise.resolve();
    if (!loading.has(file)) {
        loading.set(file, (async () => {
            try {
                const response = await fetch(`../sounds/${file}`);
                if (response.ok) buffers.set(file, await audio.decodeAudioData(await response.arrayBuffer()));
            } catch {}
            loading.delete(file);
        })());
    }
    return loading.get(file);
}

async function play(name, gap = 0) {
    if (!audio || !manifest) return;
    const now = performance.now();
    if (gap && now - (lastPlayed.get(name) ?? 0) < gap) return;
    lastPlayed.set(name, now);

    const file = fileFor(name);
    await ensure(file);
    const buffer = buffers.get(file);
    if (!buffer) return;

    if (audio.state === "suspended") await audio.resume();
    const source = audio.createBufferSource();
    const gain = audio.createGain();
    gain.gain.value = $("demo-volume").value / 100;
    source.buffer = buffer;
    source.connect(gain).connect(audio.destination);
    source.start();
}

function preload() {
    if (!manifest) return;
    for (const name of [...Object.keys(manifest.ui), "receive", "mention"]) void ensure(fileFor(name));
}

function clock() {
    const now = new Date();
    return `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;
}

function addMessage({ author, initial, tone, text, mention = false }) {
    const article = document.createElement("article");
    article.className = `msg msg--new${mention ? " msg--mention" : ""}`;

    const avatar = document.createElement("div");
    avatar.className = `avatar avatar--${tone}`;
    avatar.textContent = initial;

    const body = document.createElement("div");
    body.className = "msg-body";
    const head = document.createElement("div");
    head.className = "msg-head";
    const name = document.createElement("span");
    name.className = tone === "orange" ? "name name--orange" : tone === "teal" ? "name name--teal" : "name";
    name.textContent = author;
    const time = document.createElement("span");
    time.className = "time";
    time.textContent = clock();
    head.append(name, time);

    const paragraph = document.createElement("p");
    if (mention) {
        const tag = document.createElement("span");
        tag.className = "mention";
        tag.textContent = "@R.E.C.O.R.D.";
        paragraph.append(tag, " ");
    }
    paragraph.append(text);

    body.append(head, paragraph);
    article.append(avatar, body);
    messages.append(article);
    messages.scrollTop = messages.scrollHeight;
}

function reply() {
    addMessage({ author: "KESTREL", initial: "K", tone: "cream", text: translate(REPLIES[replyIndex++ % REPLIES.length]) });
    void play("receive");
}

function selectIn(selector, target) {
    for (const element of document.querySelectorAll(selector)) element.classList.toggle("active", element === target);
}

$("demo-power").addEventListener("click", async () => {
    audio = new AudioContext();
    try {
        manifest = await (await fetch("../sounds/manifest.json")).json();
    } catch {
        manifest = { ui: {}, sets: {} };
    }

    const select = $("demo-set");
    for (const [id, set] of Object.entries(manifest.sets ?? {})) {
        const option = document.createElement("option");
        option.value = id;
        option.textContent = set.label;
        select.append(option);
    }

    app.classList.add("is-on");
    preload();
    void play("boot");
});

document.addEventListener("pointerover", event => {
    const target = event.target.closest?.(INTERACTIVE) ?? null;
    if (target === hovered) return;
    hovered = target;
    if (target) void play("hover", 45);
});

document.addEventListener("click", event => {
    const target = event.target.closest?.(INTERACTIVE);
    if (!target || target.id === "demo-mention" || target.id === "demo-message") return;

    if (target.matches(".channel, .dm")) {
        selectIn(".channel, .dm", target);
        const label = target.querySelector(".dm-name")?.textContent ?? target.children[1]?.textContent ?? "";
        document.querySelector(".chat-title").lastChild.textContent = ` ${label.toLowerCase()}`;
        target.querySelector(".channel-badge, .channel-dot")?.remove();
        return void play("navigate", 60);
    }
    if (target.matches(".server")) {
        selectIn(".server", target);
        return void play("navigate", 60);
    }
    if (target.matches(".reaction")) {
        target.classList.toggle("active");
        return void play("toggle", 60);
    }
    if (target.matches(".user-actions button")) {
        target.classList.toggle("is-off");
        return void play(target.classList.contains("is-off") ? "back" : "toggle", 60);
    }
    void play("select", 60);
});

$("demo-input").addEventListener("keydown", event => {
    if (event.key === "Enter") {
        const text = event.currentTarget.value.trim();
        if (!text) return;
        event.currentTarget.value = "";
        addMessage({ author: "R.E.C.O.R.D.", initial: "R", tone: "orange", text });
        void play("send");
        setTimeout(reply, 1100);
    } else if (event.key.length === 1 || event.key === "Backspace") {
        void play("type", 28);
    }
});

$("demo-mention").addEventListener("click", () => {
    addMessage({ author: "SABLE", initial: "S", tone: "teal", text: translate("Check the relay when you can."), mention: true });
    void play("mention");
});

$("demo-message").addEventListener("click", reply);

$("demo-accent").addEventListener("input", event => document.documentElement.style.setProperty("--rl-accent", event.currentTarget.value));
$("demo-mode").addEventListener("change", event => { document.documentElement.dataset.rlMode = event.currentTarget.value; });
$("demo-set").addEventListener("change", () => { preload(); void play("select"); });
$("demo-motion").addEventListener("change", event => app.classList.toggle("is-moving", event.currentTarget.checked));
app.classList.add("is-moving");
