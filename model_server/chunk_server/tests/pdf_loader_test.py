import unittest

from loader.pdf_loader import PDFLoader


class PDFLoaderTest(unittest.TestCase):
    def test_load_pdf(self):
        loader = PDFLoader('./asserts/WeOps用户指南.pdf')
        docs = loader.load()


if __name__ == '__main__':
    unittest.main()
