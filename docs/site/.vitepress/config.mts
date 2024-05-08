import {defineConfig} from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    title: "OpsPilot",
    description: "OpsPilot Site",
    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        nav: [
            {text: '首页', link: '/'},
            {text: '文档', link: '/markdown-examples'}
        ],

        sidebar: [
            {
                text: '文档',
                items: [
                    {text: '简介', link: '/markdown-examples'},
                    {text: '快速入门', link: '/api-examples'},
                    {text: '系统架构', link: '/api-examples'},
                    {
                        text: '消息通道', link: '#', items: [
                            {text: '企业微信', link: '/api-examples'},
                            {text: 'Web', link: '/api-examples1'}
                        ]
                    },
                    {
                        text: '能力介绍', link: '#', items: [
                            {
                                text: '日常', link: '#', items: [
                                    {text: '知识问答', link: '#'},
                                    {text: '对话总结', link: '#'},
                                    {text: 'OCR识别', link: '#'},
                                ]
                            },
                            {
                                text: '安全', link: '#', items: [
                                    {text: '资产测绘', link: '#'},
                                ]
                            },
                            {
                                text: 'DevOps', link: '#', items: [
                                    {text: '构建分析', link: '#'},
                                ]
                            },
                            {
                                text: 'ITSM', link: '#', items: [
                                    {text: '智能提单', link: '#'},
                                ]
                            }
                        ]
                    },
                    {text: '本地开发', link: '/api-examples'}
                ]
            }
        ],

        socialLinks: [
            {icon: 'github', link: 'https://github.com/vuejs/vitepress'}
        ]
    }
})
