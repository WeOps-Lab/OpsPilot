from paddleocr import PaddleOCR, draw_ocr


class OcrService:

    def extract_content(self, img_path) -> str:
        engine = PaddleOCR(use_angle_cls=True, lang="ch")
        result = engine.ocr(img_path, cls=True)
        content = ''
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                if line[1][1] >= 0.75:
                    content += line[1][0] + ' '
        return content
