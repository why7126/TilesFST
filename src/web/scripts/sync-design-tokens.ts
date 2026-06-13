/**
 * Sync TypeScript design tokens to Web CSS variables.
 *
 * Usage: cd src/web && pnpm sync:tokens
 * Note: Commit tokens.generated.css after token changes (Docker build uses src/web context only).
 */

import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { generateTokensCss } from '../../shared/design-system/tokens/css.ts';

const webDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const outputPath = path.join(webDir, 'src/styles/tokens.generated.css');

writeFileSync(outputPath, `${generateTokensCss()}\n`, 'utf8');
console.log(`Wrote ${outputPath}`);
