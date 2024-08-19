The chat server provides the ability to interact with the LLM, including single-round chat, multi-round chat, and multi agent


## OpenAI Chat

### LangServer API

```
chat_server = RemoteRunnable(f'{CHAT_SERVICE_URL}/openai')
result = chat_server.invoke({
            "system_message_prompt": "",
            "openai_api_base": "",
            "openai_api_key": "",
            "temperature": 0.7,
            "model": "gpt-3.5-turbo",
            "user_message": "",
            "chat_history": [
                {
                    "event":"bot",
                    "text":""
                },
                {
                    "event":"user",
                    "text":""
                }
            ],
            "conversation_window_size": 6,
            "rag_context": "",
        })
```

| param                    | desc                                                                                                                                                     |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| system_message_prompt    | The prompt to be used to generate the system message                                                                                                     |
| openai_api_base          | The base URL for the OpenAI API                                                                                                                          |
| openai_api_key           | The API key for the OpenAI API                                                                                                                           |
| temperature              | The temperature to be used for the OpenAI API                                                                                                            |
| model                    | The model to be used for the OpenAI API                                                                                                                  |
| user_message             | The message from the user                                                                                                                                |
| chat_history             | The chat history                                                                                                                                         |
| conversation_window_size | The size of the conversation window                                                                                                                      |
| rag_context              | background on the use of LLM                                                                                                                             |
| tools                    | when given tools,the chat server will change to llm agent mode,tools is a list of tools that the agent can use,for example ["shell","duckduckgo-search"] |


## Zhipu Chat
### LangServer API

```
chat_server = RemoteRunnable(f'{CHAT_SERVICE_URL}/zhipu')
result = chat_server.invoke({
            "system_message_prompt": "",
            "api_base": "",
            "api_key": "",
            "temperature": 0.7,
            "model": "glm-4",
            "user_message": "",
            "chat_history": [
                {
                    "event":"bot",
                    "text":""
                },
                {
                    "event":"user",
                    "text":""
                }
            ],
            "conversation_window_size": 6,
            "rag_context": "",
        })
```

| param                    | desc                                                                                                                                                     |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| system_message_prompt    | The prompt to be used to generate the system message                                                                                                     |
| api_base                 | The base URL for the Zhipu API                                                                                                                           |
| api_key                  | The API key for the Zhipu API                                                                                                                            |
| temperature              | The temperature to be used for the Zhipu API                                                                                                             |
| model                    | The model to be used for the Zhipu API                                                                                                                   |
| user_message             | The message from the user                                                                                                                                |
| chat_history             | The chat history                                                                                                                                         |
| conversation_window_size | The size of the conversation window                                                                                                                      |
| rag_context              | background on the use of LLM                                                                                                                             |
| tools                    | when given tools,the chat server will change to llm agent mode,tools is a list of tools that the agent can use,for example ["shell","duckduckgo-search"] |
```


