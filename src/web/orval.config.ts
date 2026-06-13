import { defineConfig } from 'orval';

export default defineConfig({
  tileApi: {
    input: 'http://localhost:8000/openapi.json',
    output: {
      target: './src/shared/api/generated.ts',
      client: 'axios',
    },
  },
});
