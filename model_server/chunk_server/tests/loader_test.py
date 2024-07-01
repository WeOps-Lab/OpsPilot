import unittest

from loader.doc_loader import DocLoader
from loader.excel_loader import ExcelLoader
from loader.pdf_loader import PDFLoader
from loguru import logger

from loader.ppt_loader import PPTLoader
from loader.text_loader import TextLoader


class LoaderTest(unittest.TestCase):
    def test_load_pdf(self):
        loader = PDFLoader('./asserts/WeOps用户指南.pdf')
        docs = loader.load()
        logger.info(f'共[{len(docs)}]个文档')

    def test_load_excel(self):
        loader = ExcelLoader('./asserts/需求.xlsx')
        docs = loader.load()
        logger.info(f'共[{len(docs)}]个文档')

    def test_load_word(self):
        loader = DocLoader('./asserts/事件管理用户手册.docx')
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
