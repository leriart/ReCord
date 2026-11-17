import { cp, mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = fileURLToPath(new URL("..", import.meta.url));
const entryPath = path.join(root, "Retroless.theme.css");
const distPath = path.join(root, "dist");
const rawBase = "https://raw.githubusercontent.com/leriart/Retroless/main/";

const entry = await readFile(entryPath, "utf8");
const headerEnd = entry.indexOf("*/") + 2;
if (headerEnd < 2) throw new Error("Theme header is missing");

const header = entry.slice(0, headerEnd);
const importPattern = /^@import url\("([^"]+)"\);\s*$/gm;
const imports = [...entry.matchAll(importPattern)];
if (imports.length === 0) throw new Error("No theme imports found");

const modules = [];
for (const match of imports) {
    const url = match[1];
    if (!url.startsWith(rawBase)) {
        throw new Error(`Import does not use the repository raw base: ${url}`);
    }

    const relative = url.slice(rawBase.length);
    const modulePath = path.join(root, relative);
    const css = await readFile(modulePath, "utf8");
    modules.push({ relative, css });
}

const bundle = [
    header,
    "",
    `/* Offline bundle generated from ${imports.length} raw modules. */`,
    "",
    ...modules.map(({ relative, css }) => `/* ${relative} */\n${css.trim()}`),
    ""
].join("\n").replaceAll("../assets/", "assets/");

await rm(distPath, { recursive: true, force: true });
await mkdir(distPath, { recursive: true });
await cp(path.join(root, "assets"), path.join(distPath, "assets"), { recursive: true });
await cp(path.join(root, "LICENSE"), path.join(distPath, "LICENSE"));
await writeFile(path.join(distPath, "Retroless.theme.css"), bundle);
await writeFile(
    path.join(distPath, "README.txt"),
    [
        "RETROLESS - offline bundle",
        "",
        "Load Retroless.theme.css from this folder as a local Vencord theme.",
        "The bundled file includes all CSS modules and references only the local assets folder.",
        "",
        "Online distribution: Retroless.theme.css in the repository root."
    ].join("\n")
);

const total = modules.reduce((sum, module) => sum + module.css.length, 0);
console.log(`Built dist/Retroless.theme.css (${modules.length} modules, ${(total / 1024).toFixed(1)} KiB CSS)`);
console.log(`Copied assets and fonts (${(await readdir(path.join(distPath, "assets", "fonts"))).length} font files)`);
