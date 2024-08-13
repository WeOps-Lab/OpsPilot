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
      { text: '首页', link: '/' },
      { text: '文档', link: '/introduction' },
      { text: '|', link: '#' },
      { text: 'WeOps', link: 'https://wedoc.canway.net/' },
    ],

    sidebar: [
      {
        text: '文档',
        items: [
          { text: '简介', link: '/introduction' },
          { text: '版本', link: '/version' },
          { text: '快速入门', link: '/quick-start' },
          { text: '系统架构', link: '/architecture' },
          { text: '模型下载', link: '/models' },
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
          {
            text: '功能模块',
            items: [
              { text: '机器人', link: '/features/bot' },
              { text: 'AI模型', link: '/features/ai_models' },
              { text: '通道管理', link: '/features/channels' },
              { text: '知识管理', link: '/features/knowledges' },
              { text: '系统管理', link: '/features/system' },
            ],
          },
          {
            text: '场景',
            items: [
              { text: '日常', link: '/skills/common' },
              { text: '自动化', link: '/skills/automation' },
              { text: 'DevOps', link: '/skills/devops' },
              { text: '安全', link: '/skills/security' },
              { text: 'ITSM', link: '/skills/itsm' },
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
