from __future__ import annotations

import glob
import logging
import os
import re
import shutil
from typing import Any, Dict, List, Optional, Text

from rasa.engine.graph import ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.constants import (
    INTENT,
    RESPONSE_IDENTIFIER_DELIMITER,
    ACTION_NAME,
)
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

logger = logging.getLogger(__name__)


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER, is_trainable=True
)
class JiebaTokenizer(Tokenizer):
    """This tokenizer is a wrapper for Jieba (https://github.com/fxsjy/jieba)."""

    # 返回支持的语言列表，这里仅支持中文（简体）
    @staticmethod
    def supported_languages() -> Optional[List[Text]]:
        """Supported languages (see parent class for full docstring)."""
        return ["zh"]

    # 返回默认配置，包括自定义词典路径、意图分词标志、意图分割符号和用于检测词汇的正则表达式。
    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """Returns default config (see parent class for full docstring)."""
        return {
            # default don't load custom dictionary
            "dictionary_path": None,
            # Flag to check whether to split intents
            "intent_tokenization_flag": False,
            # Symbol on which intent should be split
            "intent_split_symbol": "_",
            # Regular expression to detect tokens
            "token_pattern": None,
        }

    # 初始化函数，主要用于设置模型存储和资源对象
    def __init__(
            self, config: Dict[Text, Any], model_storage: ModelStorage, resource: Resource
    ) -> None:
        """Initialize the tokenizer."""
        super().__init__(config)
        self._model_storage = model_storage
        self._resource = resource

    # 用于创建新的 Jieba 分词器实例。如果配置中提供了自定义词典路径，它会加载自定义词典。
    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> JiebaTokenizer:
        """Creates a new component (see parent class for full docstring)."""
        # Path to the dictionaries on the local filesystem.
        dictionary_path = config["dictionary_path"]

        if dictionary_path is not None:
            cls._load_custom_dictionary(dictionary_path)
        return cls(config, model_storage, resource)

    # 列出运行此组件所需的第三方 Python 依赖包
    @staticmethod
    def required_packages() -> List[Text]:
        """Any extra python dependencies required for this component to run."""
        return ["jieba"]

    # 静态方法，用于加载自定义词典。
    @staticmethod
    def _load_custom_dictionary(path: Text) -> None:
        """Load all the custom dictionaries stored in the path.

        More information about the dictionaries file format can
        be found in the documentation of jieba.
        https://github.com/fxsjy/jieba#load-dictionary
        """
        import jieba

        jieba_userdicts = glob.glob(f"{path}/*")
        for jieba_userdict in jieba_userdicts:
            logger.info(f"Loading Jieba User Dictionary at {jieba_userdict}")
            jieba.load_userdict(jieba_userdict)

    def train(self, training_data: TrainingData) -> Resource:
        """Copies the dictionary to the model storage."""
        self.persist()
        return self._resource

    # 重写_apply_token_pattern方法，使之接收ExtendedToken
    def _apply_token_pattern(self, tokens: List[ExtendedToken]) -> List[ExtendedToken]:
        if not self._config["token_pattern"]:
            return tokens

        compiled_pattern = re.compile(self._config["token_pattern"])

        final_tokens = []
        for token in tokens:
            new_tokens = compiled_pattern.findall(token.text)
            new_tokens = [t for t in new_tokens if t]

            if not new_tokens:
                final_tokens.append(token)

            running_offset = 0
            for new_token in new_tokens:
                word_offset = token.text.index(new_token, running_offset)
                word_len = len(new_token)
                running_offset = word_offset + word_len
                final_tokens.append(
                    ExtendedToken(
                        new_token,
                        token.start + word_offset,
                        data=token.data,
                        lemma=token.lemma,
                        pos=token.pos
                    )
                )

        return final_tokens

    # 对给定的消息属性进行分词，并返回分词后的 Token 列表。
    def tokenize(self, message: Message, attribute: Text) -> List[ExtendedToken]:
        """Tokenizes the text of the provided attribute of the incoming message."""
        import jieba

        text = message.get(attribute)

        tokenized = jieba.tokenize(text)
        tokens = [Token(word, start) for (word, start, end) in tokenized if word.strip()]

        return self._apply_token_pattern(tokens)

    def process(self, messages: List[Message]) -> List[Message]:
        """Tokenize the incoming messages."""
        for message in messages:
            for attribute in MESSAGE_ATTRIBUTES:
                if isinstance(message.get(attribute), str):
                    if attribute in [
                        INTENT,
                        ACTION_NAME,
                        RESPONSE_IDENTIFIER_DELIMITER,
                    ]:
                        tokens = self._split_name(message, attribute)
                    else:
                        tokens = self.tokenize(message, attribute)

                    # Store the original text_tokens without POS information
                    message.set(TOKENS_NAMES[attribute], tokens)

                    # Store the text_tokens with POS information in a new field
                    text_tokens_with_pos = [
                        {"text": t.text, "start": t.start, "end": t.end, "pos": t.pos}
                        for t in tokens if isinstance(t, ExtendedToken)
                    ]
                    message.set("text_tokens_with_pos", text_tokens_with_pos, True)
        return messages

    # 类方法，用于从模型存储中加载自定义词典。
    @classmethod
    def load(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
            **kwargs: Any,
    ) -> JiebaTokenizer:
        """Loads a custom dictionary from model storage."""
        dictionary_path = config["dictionary_path"]

        # If a custom dictionary path is in the config we know that it should have
        # been saved to the model storage.
        if dictionary_path is not None:
            try:
                with model_storage.read_from(resource) as resource_directory:
                    cls._load_custom_dictionary(str(resource_directory))
            except ValueError:
                logger.debug(
                    f"Failed to load {cls.__name__} from model storage. "
                    f"Resource '{resource.name}' doesn't exist."
                )
        return cls(config, model_storage, resource)

    # 用于将一个目录中的文件复制到另一个目录
    @staticmethod
    def _copy_files_dir_to_dir(input_dir: Text, output_dir: Text) -> None:
        # make sure target path exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        target_file_list = glob.glob(f"{input_dir}/*")
        for target_file in target_file_list:
            shutil.copy2(target_file, output_dir)

    # 将自定义词典持久化到模型存储中
    def persist(self) -> None:
        """Persist the custom dictionaries."""
        dictionary_path = self._config["dictionary_path"]
        if dictionary_path is not None:
            with self._model_storage.write_to(self._resource) as resource_directory:
                self._copy_files_dir_to_dir(dictionary_path, str(resource_directory))


# 扩展 rasa.nlu.tokenizers.tokenizer.Token 类以添加一个新属性来存储词性信息。
# 用于在输出中观察到词性标注信息
class ExtendedToken(Token):
    def __init__(
            self,
            text: Text,
            start: int,
            end: Optional[int] = None,
            data: Optional[Dict[Text, Any]] = None,
            lemma: Optional[Text] = None,
            pos: Optional[Text] = None,
    ) -> None:
        super().__init__(text, start, end, data, lemma)
        self.pos = pos

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExtendedToken):
            return NotImplemented

        return (
                self.text == other.text
                and self.start == other.start
                and self.end == other.end
                and self.data == other.data
                and self.lemma == other.lemma
                and self.pos == other.pos
        )

    def __repr__(self) -> Text:
        return f"ExtendedToken(text={self.text!r}, start={self.start}, end={self.end}, pos={self.pos!r})"
