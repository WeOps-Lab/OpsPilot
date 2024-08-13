The pandoc server provides the document format conversion service

## Convert document format

```python
import requests

content="" #base64 encoded content
pure_filename="" #filename without extension
file_type="" #file extension

with tempfile.NamedTemporaryFile(delete=False) as f:
    response = requests.post(
        f'{pandoc_server_host}/convert',
        data={'output': 'docx'},
        files={'file': (pure_filename + file_type, content)}
    )
    response.raise_for_status()
    f.write(response.content)
```

or use the following curl command

```bash
curl -X POST "http://your-pandoc-server/convert" \
    -F "output=pdf" \
    -F "file=@example.md" \
    --output converted.pdf
```    