import unittest

from loader.doc_loader import DocLoader
from loader.excel_loader import ExcelLoader
from loader.pdf_loader import PDFLoader
from loguru import logger

from loader.ppt_loader import PPTLoader
from loader.text_loader import TextLoader
from user_types.base_chunk_request import BaseChunkRequest
from user_types.file_chunk_request import FileChunkRequest


class LoaderTest(unittest.TestCase):
    def test_load_pdf(self):
        loader = PDFLoader('./asserts/WeOps用户指南.pdf')
        docs = loader.load()
        logger.info(f'共[{len(docs)}]个文档')

    def test_load_excel(self):
        req = BaseChunkRequest()
        loader = ExcelLoader('./asserts/需求.xlsx', req)
        docs = loader.load()
        logger.info(f'共[{len(docs)}]个文档')

    def test_load_word(self):
        loader = DocLoader('./asserts/老白教你用分栏.docx')
        docs = loader.load()
        logger.info(f'共[{len(docs)}]个文档')

    def test_load_ppt(self):
        loader = PPTLoader('./asserts/OpsPilot 智能运维助理.pptx')
        docs = loader.load()
        logger.info(f'共[{len(docs)}]个文档')

    def test_load_text(self):
        loader = TextLoader('../requirements.txt')
        docs = loader.load()
        logger.info(f'共[{len(docs)}]个文档')


if __name__ == '__main__':
    unittest.main()
