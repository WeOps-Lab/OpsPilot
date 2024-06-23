from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.memory import ChatMessageHistory
from langchain_core.runnables import RunnableLambda
from langserve import add_routes, CustomUserType
from starlette.middleware.cors import CORSMiddleware

from utils.openai_driver import OpenAIDriver

load_dotenv()

app = FastAPI(
    title="chat-server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


class ChatHistory(CustomUserType):
    event: str
    text: str


class OpenAIChatRequest(CustomUserType):
    system_message_prompt: Optional[str] = ''
    openai_api_base: str = 'https://api.openai.com'
    openai_api_key: str
    temperature: float = 0.7
    model: str = 'gpt-3.5-turbo-16k'
    user_message: str
    chat_history: List[ChatHistory] = []
    conversation_window_size: Optional[int] = 10
    rag_context: Optional[str] = ''


def openai_chat(req: OpenAIChatRequest) -> List[float]:
    driver = OpenAIDriver(
        openai_api_key=req.openai_api_key,
        openai_base_url=req.openai_api_base,
        temperature=req.temperature,
        model=req.model,
    )

    llm_chat_history = ChatMessageHistory()
    if req.chat_history:
        for event in req.chat_history:
            if event.event == "user":
                llm_chat_history.add_user_message(event.text)
            elif event.event == "bot":
                llm_chat_history.add_ai_message(event.text)

        result = driver.chat_with_history(
            system_message_prompt=req.system_message_prompt,
            user_message=req.user_message,
            message_history=llm_chat_history,
            window_size=req.conversation_window_size,
            rag_content=req.rag_context,
        )
        return result
    else:
        system_skill_prompt = req.system_message_prompt.replace("{", "").replace("}", "")
        result = driver.chat(
            system_message_prompt=system_skill_prompt,
            user_message=req.user_message,
        )
        return result


runnable = RunnableLambda(openai_chat).with_types(input_type=OpenAIChatRequest, output_type=str)

add_routes(app, runnable, path='/openai')

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8105)
