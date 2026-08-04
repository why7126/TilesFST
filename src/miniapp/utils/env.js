const MINIAPP_API_CONFIGS = {
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

function resolveMiniappEnvironment() {
  return 'production';
}

function resolveMiniappApiConfig(environment = resolveMiniappEnvironment()) {
  return MINIAPP_API_CONFIGS[environment];
}

const miniappApiConfig = resolveMiniappApiConfig();

module.exports = {
  MINIAPP_API_CONFIGS,
  resolveMiniappEnvironment,
  resolveMiniappApiConfig,
  miniappApiConfig,
};
