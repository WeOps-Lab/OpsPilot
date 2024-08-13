import { defineConfig } from 'vitepress';

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: 'OpsPilot',
  description: 'OpsPilot Site',
  themeConfig: {
    search: {
      provider: 'local',
    },

    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Doc', link: '/introduction' },
      { text: '|', link: '#' },
      { text: 'WeOps', link: 'https://wedoc.canway.net/' },
    ],

    sidebar: [
      {
        text: 'Document',
        items: [
          { text: 'Introduction', link: '/introduction' },
          { text: 'Quick Start', link: '/quick-start' },
          {
            text: 'API',
            items: [
              { text: 'RAG Server', link: '/api/rag_server' },
              { text: 'Chunk Server', link: '/api/chunk_server' },
              { text: 'Pandoc Server', link: '/api/pandoc_server' },
              { text: 'OCR Server', link: '/api/ocr_server' },
              { text: 'Fast Embed Server', link: '/api/fast_embed_server' },
              { text: 'BCE Embed Server', link: '/api/bce_embed_server' },
              { text: 'Chat Server', link: '/api/chat_server' },
              { text: 'Bionics', link: '/api/bionics' },
              { text: 'SaltStack Server', link: '/api/saltstack_server' },
              {
                text: 'Classicfy AIOPS Server',
                link: '/api/classicfy_aiops_server',
                items: [
                  {
                    text: 'Anomaly Detection',
                    items: [
                      {
                        text: 'ABOD',
                        link: '/api/aiops/anomaly/abod',
                      },
                      {
                        text: 'ECOD',
                        link: '/api/aiops/anomaly/ecod',
                      },
                      {
                        text: 'IForest',
                        link: '/api/aiops/anomaly/iforest',
                      },
                      {
                        text: 'INNE',
                        link: '/api/aiops/anomaly/inne',
                      },
                      {
                        text: 'KNN',
                        link: '/api/aiops/anomaly/knn',
                      },
                      {
                        text: 'KPCA',
                        link: '/api/aiops/anomaly/kpca',
                      },
                      {
                        text: 'MAD',
                        link: '/api/aiops/anomaly/mad',
                      },
                      {
                        text: 'OneClassSVM',
                        link: '/api/aiops/anomaly/oneclasssvm',
                      },
                      {
                        text: 'SUOD',
                        link: '/api/aiops/anomaly/suod',
                      },
                      {
                        text: 'XGBOD',
                        link: '/api/aiops/anomaly/xgbod',
                      },
                    ],
                  },
                  {
                    text: 'Causal Analysis',
                    items: [
                      {
                        text: 'FPGrowth',
                        link: '/api/aiops/causation/fpgrowth',
                      },
                      {
                        text: 'Causality',
                        link: '/api/aiops/causation/causality',
                      },
                    ],
                  },
                  {
                    text: 'Pattern Discovery',
                    items: [
                      {
                        text: 'Drain3',
                        link: '/api/aiops/logreduce/drain3',
                      },
                    ],
                  },
                  {
                    text: 'Timeseries Prediction',
                    items: [
                      {
                        text: 'SARIMA',
                        link: '/api/aiops/timeseries/sarima',
                      },
                      {
                        text: 'Holt-Winter',
                        link: '/api/aiops/timeseries/holtwinter',
                      },
                    ],
                  },
                ],
              },
            ],
          },
        ],
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/WeOps-Lab/OpsPilot' },
    ],
  },
});
