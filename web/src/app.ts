// 运行时配置
import { history } from '@umijs/max';
import Cookies from 'js-cookie';

// 全局初始化数据配置，用于 Layout 用户信息和权限初始化
// 更多信息见文档：https://umijs.org/docs/api/runtime-config#getinitialstate
export async function getInitialState(): Promise<{ name: string }> {
  return { name: '@umijs/max' };
}

export const layout = () => {
  return {
    logo: 'https://img.alicdn.com/tfs/TB1YHEpwUT1gK0jSZFhXXaAtVXa-28-27.svg',
    menu: {
      locale: false,
    },
  };
};

export function onRouteChange({ location }) {
  const bkToken = Cookies.get('accessToken');
  if (!bkToken && location.pathname !== '/login') {
    history.push('/login');
  }
}

// Request 拦截器
const authHeaderInterceptor = (url: string, options: any) => {
  const token = Cookies.get('accessToken');
  const authHeader = { Authorization: `Bearer ${token}` };
  return {
    url: url,
    options: { ...options, interceptors: true, headers: { ...options.headers, ...authHeader } },
  };
};

export const request: RequestConfig = {
  errorHandler: (error) => {
    if (error.response) {
      // 请求已发送但服务端返回状态码非 2xx 的响应
      const { status, data } = error.response;
      message.error(data.message || `请求错误 ${status}`);
    } else if (error.request) {
      // 请求已发送但未收到响应
      message.error('请求超时或服务器错误');
    } else {
      // 其他错误
      message.error(error.message);
    }
    throw error;
  },
  requestInterceptors: [authHeaderInterceptor],
};
