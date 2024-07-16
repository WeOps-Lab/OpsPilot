import base64
import re
from io import BytesIO
from typing import List

import fitz
import pdfplumber
from langchain_core.documents import Document
from langserve import RemoteRunnable
from loguru import logger
from tqdm import tqdm


class PDFLoader:

    def __init__(self, file_path, ocr_provider_address, enable_ocr_parse):
        self.file_path = file_path
        self.ocr_provider_address = ocr_provider_address
        self.enable_ocr_parse = enable_ocr_parse

    def table_to_markdown(self, table: List[List[str]]) -> str:
        # 清理数据并创建Markdown表格
        markdown_table = "| " + " | ".join(
            (cell or "").replace("\n", " ") for cell in table[0]) + " |\n"  # table headers
        markdown_table += "|---" * len(table[0]) + "|\n"  # table header-row separator

        for row in table[1:]:
            markdown_table += "| " + " | ".join(
                (cell or "").replace("\n", " ") if cell else "" for cell in row) + " |\n"

        return markdown_table

    def remove_unicode_chars(self, text):
        return re.sub(r'\\u[fF]{1}[0-9a-fA-F]{3}', '', text)

    def load(self) -> List[Document]:

        table_docs = []
        text_docs = []

        if self.enable_ocr_parse:
            file_remote = RemoteRunnable(self.ocr_provider_address)
            # 解析图片
            with fitz.Document(self.file_path) as pdf:
                for page_number in tqdm(range(1, len(pdf) + 1), desc=f"解析PDF图片[{self.file_path}]"):
                    page = pdf[page_number - 1]
                    for image_number, image in enumerate(page.get_images(), start=1):
                        xref_value = image[0]
                        base_image = pdf.extract_image(xref_value)
                        image_bytes = base_image["image"]
                        file = BytesIO(image_bytes)

                        # 完善这部分的代码
                        content = file_remote.invoke({
                            "file": base64.b64encode(file.read()).decode('utf-8'),
                        })

                        text_docs.append(Document(content))

        with pdfplumber.open(self.file_path) as pdf:

            # 解析文本
            full_text = ""
            for page in tqdm(pdf.pages, desc=f"解析PDF文本[{self.file_path}]"):
                raw_text = page.extract_text().replace("\n", " ").strip()
                raw_text = self.remove_unicode_chars(raw_text)
                if raw_text != '':
                    full_text += raw_text

            if full_text:
                text_docs.append(Document(full_text))

            # 解析表格
            for page in tqdm(pdf.pages, desc=f"解析PDF表格[{self.file_path}]"):
                table_list = page.extract_tables()
                for table in table_list:
                    if table is not None:
                        # 如果表格的所有单元格都为空或None，跳过这个表格
                        if all(not cell or cell.isspace() for row in table for cell in row):
                            continue
                        content = self.table_to_markdown(table)
                        content = self.remove_unicode_chars(content)
                        table_docs.append(Document(content, metadata={"format": "table"}))

            logger.info(f'解析PDF文件完成：{self.file_path}')

        all_docs = text_docs + table_docs
        return all_docs
