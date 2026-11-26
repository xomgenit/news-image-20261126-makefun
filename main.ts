// news-image-20261126-makefun — entry program for make.fun slug news-image-20261126
// "Sum up 26 November's world news in one image" (Thursday 26 November 2026)
//
// This is a copy program: it copies the entry.png shipped beside it into the
// output directory (/output in the grader; override with MAKEFUN_OUTPUT_DIR
// outside the grader) and then verifies the copy is a whole PNG within the
// competition limits (<= 1 MiB, <= 1024x1024). It never deletes or empties
// the output directory — the grader's /output is a mount. No network access.
// Deterministic: two runs write identical bytes.
//
// Run it locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1024 * 1024; // 1 MiB competition limit
const MAX_DIM = 1024; // max width/height in pixels
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function fail(message: string): never {
  console.error(`news-image-20261126: ERROR: ${message}`);
  process.exit(1);
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, "entry.png");
  const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
  const dest = join(outDir, "entry.png");

  // Create the output directory if needed (recursive). Never delete it.
  mkdirSync(outDir, { recursive: true });

  // Copy the entry image byte-for-byte.
  try {
    copyFileSync(source, dest);
  } catch (err) {
    fail(`could not copy ${source} to ${dest}: ${String(err)}`);
  }

  // Verify the copy: whole PNG (magic bytes), size limit, IHDR dimensions.
  const bytes = readFileSync(dest);
  if (bytes.length < 33) fail(`copied file too small to be a PNG (${bytes.length} bytes)`);
  if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) fail("copied file is not a PNG (bad magic bytes)");
  if (bytes.length > MAX_BYTES) fail(`copied file is ${bytes.length} bytes, over the 1 MiB limit`);

  // IHDR is the first chunk: 8 magic + 4 length + 4 "IHDR" + 4 width + 4 height.
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width === 0 || height === 0) fail(`PNG reports zero dimensions (${width}x${height})`);
  if (width > MAX_DIM || height > MAX_DIM) {
    fail(`PNG is ${width}x${height}, over the ${MAX_DIM}x${MAX_DIM} limit`);
  }

  const onDisk = statSync(dest).size;
  if (onDisk !== bytes.length) fail(`size mismatch after copy (${onDisk} on disk vs ${bytes.length} read)`);

  // The entry for this competition is exactly 1024x1024; warn (not fail) if
  // a future re-render ever drifts from the square canvas.
  if (width !== 1024 || height !== 1024) {
    console.error(`news-image-20261126: WARNING: expected 1024x1024, got ${width}x${height}`);
  }

  console.log(
    `news-image-20261126: wrote ${dest} (${bytes.length} bytes, ${width}x${height} PNG) — OK`,
  );
}

main();
