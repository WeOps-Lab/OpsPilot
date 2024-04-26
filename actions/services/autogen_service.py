import autogen
from typing import Annotated
from IPython import get_ipython

from actions.constants.server_settings import server_settings
from actions.services.chat_service import ChatService


class AutogenService:
    def __init__(self):
        self.chat_service = ChatService(server_settings.fastgpt_endpoint, server_settings.fastgpt_content_summary_key)
        config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
        llm_config = {
            "seed": 42,
            "config_list": config_list,
            "temperature": 0,
            "timeout": 600,
            "model": "gpt-3.5-turbo-16k"
        }
        self.assistant = autogen.AssistantAgent(
            name="assistant",
            max_consecutive_auto_reply=3, llm_config=llm_config, )

        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            llm_config=llm_config,
            system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
        Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            max_consecutive_auto_reply=5,
            code_execution_config={
                "work_dir": "coding",
                "use_docker": False
            },
        )

        self.register_functions()

    def register_functions(self):
        @self.user_proxy.register_for_execution()
        @self.assistant.register_for_llm(name="sh", description="run a shell script and return the execution result.")
        def exec_sh(script: Annotated[str, "Valid Python cell to execute."]) -> str:
            return self.user_proxy.execute_code_blocks([("sh", script)])

        @self.user_proxy.register_for_execution()
        @self.assistant.register_for_llm(name="python",
                                         description="run a python script and return the execution result.")
        def exec_python(cell: Annotated[str, "Valid Python cell to execute."]) -> str:
            ipython = get_ipython()
            result = ipython.run_cell(cell)
            log = str(result.result)
            if result.error_before_exec is not None:
                log += f"\n{result.error_before_exec}"
            if result.error_in_exec is not None:
                log += f"\n{result.error_in_exec}"
            return log

    def chat(self, prompt):
        chat_res = self.user_proxy.initiate_chat(
            self.assistant,
            message=prompt,
            summary_method="reflection_with_llm",
        )

        return chat_res

#
# service = AutogenService()
# chat_res = service.chat('https://github.com/是一个什么网站？')
# print(f'执行结果:[{chat_res.summary}]')
# print(f'共消费:[{chat_res.cost}]')
# print(f'对话历史:[{chat_res.chat_history}]')
