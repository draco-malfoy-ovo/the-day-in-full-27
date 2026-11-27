/**
 * The Day in Full — Friday 27 November 2026.
 *
 * Entry for make.fun's "Sum up today's world news in one image"
 * (news-image-20261127). The deliverable is the picture next to this
 * file: a hand-drawn newspaper front page summing up Friday
 * 27 November 2026 — the Iran war and the Kuwait drone deaths,
 * New Zealand's one-short coalition, Australia's IRGC-linked arson
 * sanctions, Japan's defence plan, the EU's collapsed budget talks,
 * oil's Hormuz-driven climb, and the US storm aftermath — each story
 * cross-checked in at least two outlets (see SOURCES.md).
 *
 * The grader runs this file offline in Node with no arguments and no
 * environment variables set, so all it does is copy the committed
 * entry.png into the output directory: $MAKEFUN_OUTPUT_DIR when set,
 * otherwise /output. Same input, same bytes, every run.
 */

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}

copyFileSync(source, join(outDir, "entry.png"));
