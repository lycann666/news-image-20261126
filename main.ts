// news-image-20261126 — "Sum up 26 November's world news in one image".
//
// The entry is a newspaper front page for Thursday 26 November 2026,
// drawn by render_image.py (kept in this repository so the image can be
// rebuilt) and shipped here as entry.png. This program's only job is to
// place that image at /output/entry.png, exactly as the grader expects.
//
// Node 22, standard library only. No network, no randomness, no clock:
// every run copies the same bytes, so two runs always write identical
// output. Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
