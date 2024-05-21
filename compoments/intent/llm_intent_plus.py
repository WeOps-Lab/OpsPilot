import json
from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

from utils.llm_driver import LLMDriver

'''
大模型意图分类器与实体识别器，提供分类和识别功能

- name: "compoments.intent.llm_intent_plus.LLMIntentClassifierPlus"
  intents:
    - yes "是的"
    - no "不是"
    - out_of_scope "不在上述任何的意图里面"
  entities:
   - city
   - street
   - number  
'''

prompt_template = """
你是一个Rasa的ChatGPT的意图分类引擎，请严格按照以下json格式回复数据：
{ "intent": {"name": "test", "confidence": 1.0}, intent_ranking: [{"name": "test", "confidence": 1.0}] }

你将会接到用户的文本输入，请在以下intent中选择合适的intent，并返回json格式的数据。

{{content}}

数组的格式是 ['intent "描述信息"']，其中描述信息是可选的，只是为了方便你理解这个意图的内容。

注意：

只允许在上述的意图中进行选择，不要选择其他的意图。
请严格按照json格式回复数据，不要包含多余的内容。

请按照以下json格式回复识别到的entity属性
{{"entity": "entity_name", "value": "entity_value", "start": 0, "end": 4, "extractor": "DualIntentAndEntityLLM"}}.

entity "描述信息"的格式是 ['entity "描述信息"']，其中描述信息是可选的，只是为了方便你理解这个entity的内容。

以下是可选的entity列表：

{{entities}}

最终返回的格式示例如下，请严格遵守，
{{
  "intent": {{
    "name": "example_intent_name",
    "confidence": 1.0
  }},
  "entities": [],
  "intent_ranking": [
    {{
      "name": "",
      "confidence": 1.0
    }}
  ]
}}

"""

from openai import OpenAI


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=False
)
class LLMIntentClassifierPlus(GraphComponent):
    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {}

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config)

    def __init__(self, config: Dict[Text, Any]):
        super().__init__()

        if "intents" in config:
            self.intents = config["intents"]
        else:
            self.intents = []

        if "entities" in config:
            self.entities = config["entities"]
        else:
            self.entities = []

        if "model" in config:
            self.model = config["model"]
        else:
            self.model = "gpt-3.5-turbo"

        if "temperature" in config:
            self.temperature = config["temperature"]
        else:
            self.temperature = 0

        if "max_tokens" in config:
            self.max_tokens = config["max_tokens"]
        else:
            self.max_tokens = 1024

        self.prompt = prompt_template.replace('{{content}}', str(self.intents)).replace('{{entities}}',
                                                                                        str(self.entities))

        self.llm = LLMDriver(self.prompt, self.model, self.temperature, self.max_tokens)

    def train(self, training_data: TrainingData) -> Resource:
        pass

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        return training_data

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            message = self.classify_intents_with_llm(message)

        return messages

    def classify_intents_with_llm(self, message: Message) -> Message:
        text = message.get("text")

        # get intent and intent_ranking from LLM model

        llm_response_as_string = self.llm.chat(text)

        llm_response = json.loads(llm_response_as_string)

        intent_dict = llm_response["intent"]

        message.set("intent", intent_dict, add_to_output=True)

        intent_ranking_dict = llm_response["intent_ranking"]

        message.set("intent_ranking", intent_ranking_dict, add_to_output=True)

        entities = llm_response["entities"]
        message.set("entities", entities, add_to_output=True)
        return message
