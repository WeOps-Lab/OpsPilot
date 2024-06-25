from typing import List

import cv2
import fitz
import numpy as np
import pdfplumber
from PIL.Image import Image
from langchain_core.documents import Document
from rapidocr_onnxruntime import RapidOCR
from tqdm import tqdm
from loguru import logger


class PDFLoader:

    def __init__(self, file_path):
        self.ocr = RapidOCR()
        self.file_path = file_path

    def rotate_img(self, img, angle):
        """
        img   --image
        angle --rotation angle
        return--rotated img
        """

        h, w = img.shape[:2]
        rotate_center = (w / 2, h / 2)
        # 获取旋转矩阵
        # 参数1为旋转中心点;
        # 参数2为旋转角度,正值-逆时针旋转;负值-顺时针旋转
        # 参数3为各向同性的比例因子,1.0原图，2.0变成原来的2倍，0.5变成原来的0.5倍
        M = cv2.getRotationMatrix2D(rotate_center, angle, 1.0)
        # 计算图像新边界
        new_w = int(h * np.abs(M[0, 1]) + w * np.abs(M[0, 0]))
        new_h = int(h * np.abs(M[0, 0]) + w * np.abs(M[0, 1]))
        # 调整旋转矩阵以考虑平移
        M[0, 2] += (new_w - w) / 2
        M[1, 2] += (new_h - h) / 2

        rotated_img = cv2.warpAffine(img, M, (new_w, new_h))
        return rotated_img

    def load(self) -> List[Document]:
        logger.info(f'开始解析PDF文件：{self.file_path}')

        docs = []

        raw_text_list = []
        table_text_list = []
        ocr_text_list = []

        with pdfplumber.open(self.file_path) as pdf:
            # 解析文本和表格
            for page in tqdm(pdf.pages):
                raw_text_list.append(page.extract_text())
                table = page.extract_table()

                if table:
                    table_text_list.append(table)

            # 移除重复的表格信息
            table_texts = ['\n'.join([' '.join(row) for row in table_entity]) for table_entity in table_text_list]
            for i, text in enumerate(raw_text_list):
                for table_text in table_texts:
                    if table_text in text:
                        raw_text_list[i] = text.replace(table_text, ' ')

            # OCR识别图片
            doc = fitz.open(self.file_path)
            for i, page in tqdm(enumerate(doc)):
                img_list = page.get_image_info(xrefs=True)
                for img in img_list:
                    if xref := img.get("xref"):
                        pix = fitz.Pixmap(doc, xref)

                        if int(page.rotation) != 0:
                            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, -1)
                            tmp_img = Image.fromarray(img_array)
                            ori_img = cv2.cvtColor(np.array(tmp_img), cv2.COLOR_RGB2BGR)
                            rot_img = self.rotate_img(img=ori_img, angle=360 - page.rotation)
                            img_array = cv2.cvtColor(rot_img, cv2.COLOR_RGB2BGR)
                        else:
                            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, -1)
                        result, _ = self.ocr(img_array)
                        if result:
                            ocr_result = [line[1] for line in result]
                            ocr_text_list.append('\n'.join(ocr_result))

            # 组装数据
            for text in raw_text_list:
                docs.append(Document(text))

            for table_entity in table_text_list:
                table_text = '\n'.join([' '.join(row) for row in table_entity])
                docs.append(Document(table_text, metadata={"format": "table"}))

            for text in ocr_text_list:
                docs.append(Document(text))

        return docs
