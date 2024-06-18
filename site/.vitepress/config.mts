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
          { text: '快速入门', link: '/quick-start' },
          { text: '系统架构', link: '/architecture' },
          { text: '模型下载', link: '/models' },
          {
            text: '功能模块',
            link: '#',
            items: [
              { text: '机器人', link: '/features/bot' },
              { text: 'AI模型', link: '/features/ai_models' },
              { text: '通道管理', link: '/features/channels' },
              { text: '知识管理', link: '/features/knowledges' },
              { text: '扩展包', link: '/features/contentpack' },
              { text: '系统管理', link: '/features/system' },
            ],
          },
          {
            text: '技能',
            link: '#',
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
