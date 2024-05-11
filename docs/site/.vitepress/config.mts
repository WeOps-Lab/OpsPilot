import {defineConfig} from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    title: "OpsPilot",
    description: "OpsPilot Site",
    themeConfig: {
        search: {
            provider: 'local'
        },

        // https://vitepress.dev/reference/default-theme-config
        nav: [
            {text: '首页', link: '/'},
            {text: '文档', link: '/introduction'},
            {text: '|', link: '#'},
            {text: 'WeOps', link: 'https://wedoc.canway.net/'},
        ],

        sidebar: [
            {
                text: '文档',
                items: [
                    {text: '简介', link: '/introduction'},
                    {text: '快速入门', link: '/quick-start'},
                    {text: '系统架构', link: '/architecture'},
                    {text: '模型下载', link: '/models'},
                    {
                        text: '通道概览', link: '#', items: [
                            {text: '企业微信', link: '/channel/enterprise-wechat'},
                            {text: 'Web', link: '/channel/web'}
                        ]
                    },
                    {
                        text: '能力概览', link: '/skills/index', items: [
                            {
                                text: '日常', link: '/skills/common'
                            },
                            {
                                text: '安全', link: '/skills/security'
                            },
                            {
                                text: 'DevOps', link: '/skills/devops'
                            },
                            {
                                text: '智能工单', link: '/skills/itsm',
                            },
                            {
                                text: '自动化', link: '/skills/automation',
                            }
                        ]
                    },
                    {text: '本地开发', link: 'development'},
                ]
            }
        ],

        socialLinks: [
            {icon: 'github', link: 'https://github.com/WeOps-Lab/OpsPilot'}
        ]
    }
})
