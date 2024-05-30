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
大模型实体识别器，仅提供识别功能
- name: "compoments.entity.llm_entities_extractor.LLMEntitiesExtractor"
  entities:
   - city
   - street
   - number
'''

prompt_template = """
你是一个Rasa的ChatGPT的意图分类引擎，请严格按照以下json格式回复数据：
{{"entity": "entity_name", "value": "entity_value", "start": 0, "end": 4, "extractor": "llm_entity_extractor_component"}}.

请按照以下json格式回复识别到的entity属性
{{"entity": "entity_name", "value": "entity_value", "start": 0, "end": 4, "extractor": "DualIntentAndEntityLLM"}}.

entity "描述信息"的格式是 ['entity "描述信息"']，其中描述信息是可选的，只是为了方便你理解这个entity的内容。

以下是可选的entity列表：

{{entities}}

用户的输入是:

"""


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR], is_trainable=False
)
class LLMEntitiesExtractor(GraphComponent):
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

        llm_response_as_string = self.llm.chat(text)

        llm_response = json.loads(llm_response_as_string)

        message.set("entities", llm_response)
        return message
