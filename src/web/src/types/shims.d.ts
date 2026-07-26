declare module '*.css';

declare module 'node:fs' {
  export function readFileSync(path: string): { byteLength: number };
  export function readFileSync(path: string, encoding: BufferEncoding): string;
}

declare module 'node:path' {
  export function dirname(path: string): string;
  export function join(...paths: string[]): string;
  export function resolve(...paths: string[]): string;

  const path: {
    dirname(path: string): string;
    join(...paths: string[]): string;
    resolve(...paths: string[]): string;
  };
  export default path;
}

declare module 'node:url' {
  export function fileURLToPath(url: string | URL): string;
}

declare const process: {
  cwd(): string;
};

type BufferEncoding = 'utf8' | 'utf-8' | string;

declare module 'tailwindcss' {
  export type Config = Record<string, unknown>;
}

declare module 'tailwindcss/plugin' {
  type PluginApi = {
    addUtilities: (utilities: Record<string, unknown>) => void;
  };

  const plugin: (callback: (api: PluginApi) => void) => unknown;
  export default plugin;
}
