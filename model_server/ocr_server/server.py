from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from paddleocr import PPStructure

app = FastAPI()

# Initialize the PaddleOCR engine
table_engine = PPStructure(table=False, ocr=True, show_log=True, lang='ch',
                           det_model_dir='./models/ch_PP-OCRv4_det_infer/',
                           rec_model_dir='./models/ch_PP-OCRv4_rec_infer/',
                           cls_model_dir='./models/ch_ppocr_mobile_v2.0_cls_infer/',
                           use_angle_cls=True, )


@app.post("/paddleocr/ocr")
async def ocr(file: UploadFile):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = table_engine(img)

    try:
        recognized_texts = ''
        for line in result:
            for i in line['res']:
                recognized_texts += i['text'] + ' '

        return JSONResponse(content={"text": recognized_texts})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8109)
