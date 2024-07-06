import io
import os
import subprocess
import uuid
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form
from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.post("/convert")
async def convert(output: Optional[str] = Form(...), file: UploadFile = File(...)):
    if output not in ["docx", "pdf"]:
        logger.warning(f"不支持的转换格式: {output}")
        raise HTTPException(status_code=400, detail="不支持的转换格式")

    file_name = str(uuid.uuid4())

    with open(file_name, "wb") as buffer:
        buffer.write(await file.read())

    try:
        if output == "pdf":
            subprocess.run(
                [
                    "pandoc",
                    "-s",
                    file_name,
                    "-o",
                    f"{file_name}.{output}",
                    "--pdf-engine",
                    "xelatex",
                    "-V",
                    "CJKmainfont=WenQuanYi Zen Hei Mono",
                    "--template",
                    "./latex/eisvogel.latex",
                    "--listings",
                    "-f",
                    "markdown-raw_tex"
                ],
                capture_output=True,
                text=True,
            )
        else:
            subprocess.run(["pandoc", file_name, "-o", f"{file_name}.{output}"], check=True)

        with open(f"{file_name}.{output}", "rb") as f:
            data = io.BytesIO(f.read())
        os.remove(f"{file_name}.{output}")

        # 假如转换成功则删除文件，转换失败则保留文件，方便排查原因
        os.remove(file_name)
        
        return StreamingResponse(data, media_type="application/octet-stream",
                                 headers={'Content-Disposition': f'attachment; filename={file_name}.{output}'})

    except Exception as e:
        logger.error(f"文件[{file_name}] 转换失败: {e}")
        raise HTTPException(status_code=500, detail="转换失败")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8103)
