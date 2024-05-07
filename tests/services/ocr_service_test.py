from actions.services.ocr_service import OcrService


def test_ocr():
    service = OcrService()
    result = service.extract_content('tests/asserts/umaru.jpeg')
    print(result)
