from typing import List

from langchain_community.document_loaders import UnstructuredFileLoader


class PDFLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        from utils.pdf import pdf2text

        text = pdf2text(self.file_path)
        from unstructured.partition.text import partition_text

        return partition_text(text=text, **self.unstructured_kwargs)
