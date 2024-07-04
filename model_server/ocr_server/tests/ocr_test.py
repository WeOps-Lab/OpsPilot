import os
import cv2
from paddleocr import PPStructure, save_structure_res

table_engine = PPStructure(table=False, ocr=True, show_log=True, lang='ch',
                           det_model_dir='./models/ch_PP-OCRv4_det_infer/',
                           rec_model_dir='./models/ch_PP-OCRv4_rec_infer/',
                           cls_model_dir='./models/ch_ppocr_mobile_v2.0_cls_infer/',
                           use_angle_cls=True, )

img_path = './tests/asserts/海报.png'
img = cv2.imread(img_path)
result = table_engine(img)

for line in result:
    for i in line['res']:
        print(i['text'])
