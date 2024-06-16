import React from 'react';
import { ConfigProvider } from 'antd';
import theme from './theme/themeConfig';

export default function App({ Component, pageProps }) {
  return (
    <ConfigProvider theme={theme}>
      <Component {...pageProps} />
    </ConfigProvider>
  )
}
