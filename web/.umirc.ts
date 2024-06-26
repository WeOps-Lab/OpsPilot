import {defineConfig} from '@umijs/max';

export default defineConfig({
    antd: {},
    access: {},
    model: {},
    initialState: {},
    request: {},
    layout: {
        title: '@umijs/max',
    },
    proxy: {
        '/api': {
            'target': 'http://munchkin.japanwest.cloudapp.azure.com/',
            'changeOrigin': true,
        },
    },
    routes: [
        {
            path: '/',
            redirect: '/home',
        },
        {
            name: '首页',
            path: '/home',
            component: './Home',
        },
        {
            name: '权限演示',
            path: '/access',
            component: './Access',
        },
        {
            name: ' CRUD 示例',
            path: '/table',
            component: './Table',
        },
        {
            name: '登录',
            path: '/login',
            component: './Login',
            layout: false,
        },
    ],
    npmClient: 'pnpm',
});

