import {PageContainer} from '@ant-design/pro-components';
import {useModel, request} from '@umijs/max';
import {ProChat} from '@ant-design/pro-chat';

const HomePage: React.FC = () => {
    const {name} = useModel('global');

    return (
        <PageContainer ghost>
            <ProChat
                style={{height: '750px'}}
                helloMessage={
                    '欢迎使用 ProChat ，我是你的专属机器人，这是我们的 Github：[ProChat](https://github.com/ant-design/pro-chat)'
                }
                request={async (messages) => {
                    // 获取最后一条messages
                    const lastMessage = messages[messages.length - 1].content;
                    const chat_history = messages.map((item) => {
                        return {
                            event: item.role,
                            text: item.content,
                        }
                    });
                    let {result} = await request('/api/llm/execute/', {
                        headers: {
                            'accept': 'application/json',
                            'Content-Type': 'application/json',
                            'Authorization': `Token `
                        },
                        method: 'POST',
                        data: {
                            llm_skill_id: 19,
                            user_message: lastMessage,
                            chat_history: chat_history,
                            super_system_prompt: "",
                        }
                    });
                    return new Response(result);
                }}
            />
        </PageContainer>
    );
};

export default HomePage;
