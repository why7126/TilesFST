export type MiniappEnvironment = 'development' | 'production';

export type MiniappApiConfig = {
  environment: MiniappEnvironment;
  apiBaseUrl: string;
  apiFallbackBaseUrls: string[];
};

export const MINIAPP_API_CONFIGS: Record<MiniappEnvironment, MiniappApiConfig> = {
  development: {
    environment: 'development',
    apiBaseUrl: 'http://127.0.0.1:8010',
    apiFallbackBaseUrls: ['http://localhost:8010', 'http://localhost:8000'],
  },
  production: {
    environment: 'production',
    apiBaseUrl: 'https://tilesfst.wjoyhappy.site',
    apiFallbackBaseUrls: [],
  },
};

export function resolveMiniappEnvironment(): MiniappEnvironment {
  return 'production';
}

export function resolveMiniappApiConfig(environment = resolveMiniappEnvironment()): MiniappApiConfig {
  return MINIAPP_API_CONFIGS[environment];
}

export const miniappApiConfig = resolveMiniappApiConfig();
