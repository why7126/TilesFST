import { defineConfig } from 'orval';

export default defineConfig({
  tileApi: {
    input: './openapi.json',
    output: {
      target: './src/shared/api/generated.ts',
      client: 'axios',
    },
  },
});
