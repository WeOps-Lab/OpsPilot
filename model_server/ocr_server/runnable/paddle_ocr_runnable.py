import base64
from typing import List
import cv2
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
import numpy as np
from paddleocr import PPStructure
from loguru import logger

from user_types.paddle_ocr_request import PaddleOcrRequest


class PaddleOcrRunnable:
    def __init__(self):
        self.table_engine = PPStructure(table=False, ocr=True, show_log=True, lang='ch',
                                        det_model_dir='./models/ch_PP-OCRv4_det_infer/',
                                        rec_model_dir='./models/ch_PP-OCRv4_rec_infer/',
                                        cls_model_dir='./models/ch_ppocr_mobile_v2.0_cls_infer/',
                                        use_angle_cls=True, )

    def execute(self, request: PaddleOcrRequest) -> str:
        # base64 str to opencv img
        base_image = base64.b64decode(request.file)
        nparr = np.fromstring(base_image, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        result = self.table_engine(img)
        try:
            recognized_texts = ''
            for line in result:
                for i in line['res']:
                    recognized_texts += i['text'] + ' '

            return recognized_texts
        except Exception as e:
            logger.info(e)
            return ''

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=PaddleOcrRequest, output_type=str)
