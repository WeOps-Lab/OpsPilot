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
          {
            text: 'AIOPS算法',
            items: [
              {
                text: '时序预测',
                items: [
                  { text: 'HoltWinter', link: '/aiops/timeseries/holtwinter' },
                  { text: 'SARIMA', link: '/aiops/timeseries/sarima' },
                ],
              },
              {
                text: '异常检测',
                items: [
                  { text: 'MAD', link: '/aiops/anomaly/mad' },
                  { text: 'ABOD', link: '/aiops/anomaly/abod' },
                  { text: 'SUOD', link: '/aiops/anomaly/suod' },
                  { text: 'IForest', link: '/aiops/anomaly/iforest' },
                  { text: 'KNN', link: '/aiops/anomaly/knn' },
                  { text: 'ECOD', link: '/aiops/anomaly/ecod' },
                  { text: 'XGBOD', link: '/aiops/anomaly/xgbod' },
                  { text: 'INNE', link: '/aiops/anomaly/inne' },
                  { text: 'KPCA', link: '/aiops/anomaly/kpca' },
                  { text: 'One Class SVM', link: '/aiops/anomaly/oneclasssvm' },
                ],
              },
              {
                text: '模式发现',
                items: [{ text: 'Drain3', link: '/aiops/logreduce/drain3' }],
              },
              {
                text: '根因分析',
                items: [
                  { text: '概率因果模型', link: '/aiops/causation/causality' },
                  { text: 'FP-Growth', link: '/aiops/causation/fpgrowth' },
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
