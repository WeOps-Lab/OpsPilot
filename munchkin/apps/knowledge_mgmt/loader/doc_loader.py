from langchain_community.document_loaders import UnstructuredFileLoader
from typing import List

from unstructured.partition.text import partition_text

from apps.knowledge_mgmt.utils.doc import doc2text


class DocLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        text = doc2text(self.file_path)
        return partition_text(text=text, **self.unstructured_kwargs)
