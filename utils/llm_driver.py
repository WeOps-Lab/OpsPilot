from openai import OpenAI

from core.server_settings import server_settings


class LLMDriver:
    def __init__(self, prompt: str, model="gpt-3.5-turbo-16k", temperature=0.7, max_tokens=4000):
        self.prompt = prompt
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI(
            api_key=server_settings.openai_api_key,
            base_url=server_settings.openai_base_url
        )

    def chat(self, text: str):
        chat_completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": text}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return chat_completion.choices[0].message.content
