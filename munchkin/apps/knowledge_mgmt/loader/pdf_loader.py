from typing import List

from langchain.document_loaders.unstructured import UnstructuredFileLoader

from apps.knowledge_mgmt.utils.pdf import pdf2text


class PDFLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        text = pdf2text(self.file_path)
        from unstructured.partition.text import partition_text
        return partition_text(text=text, **self.unstructured_kwargs)
