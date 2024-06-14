from typing import List

from langchain_community.document_loaders import UnstructuredFileLoader
from unstructured.partition.text import partition_text


class DocLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        from apps.knowledge_mgmt.utils.doc import doc2text

        text = doc2text(self.file_path)
        return partition_text(text=text, **self.unstructured_kwargs)
