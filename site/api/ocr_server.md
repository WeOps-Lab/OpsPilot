OCR Server service provides the ability to extract text from images

## Paddle OCR
```
ocr_remote = RemoteRunnable(f'{ocr_server}/paddle_ocr')
with open(image_path, "rb") as file:
    content = file_remote.invoke({
                "file": base64.b64encode(file.read()).decode('utf-8'),
    })
```

## Azure OCR

```
ocr_remote = RemoteRunnable(f'{ocr_server}/azure_ocr')
with open(image_path, "rb") as file:
    content = file_remote.invoke({
                "file": base64.b64encode(file.read()).decode('utf-8'),
    })
```            