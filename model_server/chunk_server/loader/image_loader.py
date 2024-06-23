from typing import List

from langchain_community.document_loaders import UnstructuredFileLoader
from unstructured.partition.text import partition_text


class ImageLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        from utils.image import img2text

        text = img2text(self.file_path)

        return partition_text(text=text, **self.unstructured_kwargs)
