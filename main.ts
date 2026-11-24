import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';

const BOT_DIR = resolve(process.env.MAKEFUN_BOT_DIR ?? '/bot');
const OUTPUT_DIR = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? '/output');
const POST_FILE = 'POST.json';

// An X post address, as the gate reads it: https://x.com/<handle>/status/<id>
// (or the same on twitter.com). The placeholder this repository ships with
// is not a real post, so it only warns instead of failing: the gate refuses
// it on its own, and the program must still run and copy it.
const X_POST_URL =
  /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/]+\/status\/\d+\/?([?#].*)?$/;

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

const source = join(BOT_DIR, POST_FILE);
const target = join(OUTPUT_DIR, POST_FILE);

let raw: string;
try {
  raw = readFileSync(source, 'utf8');
} catch (err) {
  fail(`cannot read ${source}: ${(err as Error).message}`);
}

if (Buffer.byteLength(raw!, 'utf8') > 16384) {
  fail('POST.json is over the 16384 byte cap');
}

let parsed: unknown;
try {
  parsed = JSON.parse(raw!);
} catch (err) {
  fail(`POST.json is not valid JSON: ${(err as Error).message}`);
}

if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
  fail('POST.json must hold a JSON object with a url field');
}

const entry = parsed as Record<string, unknown>;
if (typeof entry.url !== 'string' || entry.url.length === 0) {
  fail('POST.json must hold a non-empty string url');
}
if (!X_POST_URL.test(entry.url)) {
  console.error(
    'main.ts: warning: url is not an X post address yet; ' +
      'replace the placeholder with the posted address before submitting',
  );
}

mkdirSync(OUTPUT_DIR, { recursive: true });

try {
  copyFileSync(source, target);
} catch (err) {
  fail(`cannot write ${target}: ${(err as Error).message}`);
}

// Confirm the copy landed byte for byte before reporting success.
const sourceSize = statSync(source).size;
const targetSize = statSync(target).size;
if (sourceSize !== targetSize) {
  fail(`copy mismatch: ${source} is ${sourceSize} bytes, ${target} is ${targetSize}`);
}
