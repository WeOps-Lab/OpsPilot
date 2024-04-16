import logging

from actions.services.ocr_service import OcrService


def test_extract_content():
    service = OcrService()
    content = service.extract_content('tests/asserts/demo.png')
    logging.info(f'识别到的内容为:{content}')
