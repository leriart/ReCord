import { access, readFile, readdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = fileURLToPath(new URL("..", import.meta.url));
const errors = [];
const warnings = [];

const read = relative => readFile(path.join(root, relative), "utf8");
const exists = async relative => {
    try {
        await access(path.join(root, relative));
        return true;
    } catch {
        return false;
    }
};

const entry = await read("Retroless.theme.css");
const header = entry.split("*/", 1)[0] ?? "";

for (const field of ["@name", "@author", "@description", "@version", "@license", "@source"]) {
    if (!header.includes(field)) errors.push(`Theme header is missing ${field}`);
}

const files = [
    ...(await readdir(path.join(root, "src"))).filter(file => file.endsWith(".css")).map(file => `src/${file}`),
    "docs/demo.css",
    "docs/site.css"
];

for (const file of files) {
    const css = await read(file);
    for (const match of css.matchAll(/url\((["']?)([^)"']+)\1\)/g)) {
        const url = match[2].trim();
        if (!url || url.startsWith("data:") || url.startsWith("http") || url.startsWith("var(")) continue;
        const target = path.normalize(path.join(path.dirname(file), url));
        if (!(await exists(target))) errors.push(`${file} references missing asset: ${url}`);
    }
}

let csstree;
try {
    csstree = await import("css-tree");
} catch {
    warnings.push("css-tree is not installed; syntax validation skipped (run npm install)");
}

if (csstree) {
    for (const file of files) {
        const css = await read(file);
        const parseErrors = [];
        csstree.parse(css, { positions: true, onParseError: error => parseErrors.push(error) });
        for (const error of parseErrors) {
            errors.push(`${file}:${error.line}:${error.column} ${error.message}`);
        }
    }
}

for (const warning of warnings) console.warn(`warning: ${warning}`);
for (const error of errors) console.error(`error: ${error}`);

if (errors.length) {
    process.exitCode = 1;
} else {
    console.log(`Checked ${files.length} stylesheets`);
}
