from rapidocr_onnxruntime import RapidOCR


def img2text(filepath):
    resp = ""
    ocr = RapidOCR()
    result, _ = ocr(filepath)
    if result:
        ocr_result = [line[1] for line in result]
        resp += "\n".join(ocr_result)
    return resp


