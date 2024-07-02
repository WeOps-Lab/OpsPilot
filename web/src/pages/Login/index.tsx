import React, { useEffect, useState } from 'react';
import { Button, Form, Input, Layout, Typography, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { request, history } from '@umijs/max';
import './index.less';
import Cookies from 'js-cookie';
import loginAnimationVideo from '@/assets/video/login_animation_video.mp4'; // 直接引用视频文件


const { Title } = Typography;
const { Content } = Layout;

interface LoginFormValues {
  username: string;
  password: string;
}

const LoginPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    // 移除 bk_token
    Cookies.remove('accessToken', { path: '/' });
  }, []);

  const onFinish = async (values: LoginFormValues) => {
    setLoading(true);
    try {
      const data = await request('/api/token/', {
        method: 'POST',
        data: values,
      });

      if (data) {
        const { access } = data;
        Cookies.set('accessToken', access, { path: '/', expires: 1 });
        message.success('登录成功');
        history.push('/home');
      } else {
        message.error('登录失败,服务器未返回令牌,请稍后再试');
      }
    } catch (error) {
      message.error('登录失败,请检查用户名和密码');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Content className="login-form-container">
      <video className="video-background" autoPlay muted loop>
        <source src={loginAnimationVideo} type="video/mp4" />
      </video>
      <div className="login-box">
        <Title level={2}>
          欢迎登录OpsPilot
        </Title>
        <Form
          name="login_form"
          initialValues={{ remember: true }}
          onFinish={onFinish}
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: '请输入用户名!' }]}
          >
            <Input
              prefix={<UserOutlined className="site-form-item-icon" />}
              placeholder="请输入用户名"
            />
          </Form.Item>
          <Form.Item
            name="password"
            rules={[{ required: true, message: '请输入密码!' }]}
          >
            <Input.Password
              prefix={<LockOutlined className="site-form-item-icon" />}
              type="password"
              placeholder="请输入密码"
            />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block loading={loading}>
              登录
            </Button>
          </Form.Item>
        </Form>
      </div>
    </Content>
  );
};

export default LoginPage;
