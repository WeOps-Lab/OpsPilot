Chunk-Server is responsible for knowledge partitioning, supports semantic and length partitioning of files, and has a variety of knowledge partitioning options

## File Partitioning

### LangServe API

```python
file_remote = RemoteRunnable(FILE_CHUNK_SERIVCE_URL)
remote_docs = file_remote.invoke(
              {
                  "enable_recursive_chunk_parse": true
                  "recursive_chunk_size": 128,
                  "recursive_chunk_overlap": 0,
                  "enable_semantic_chunck_parse": false,
                  "enable_ocr_parse": false,
                  "ocr_provider_address": "",
                  "semantic_embedding_address": "",
                  "excel_header_row_parse": false,
                  "excel_full_content_parse": true,
                  "file_name": "",
                  "file": ""#base46 file string,
                  "custom_metadata": {
                      "knowledge_type": "file",
                      "knowledge_id": 1,
                      "knowledge_title": "",
                      "knowledge_folder_id": 1,
                      **knowledge.custom_metadata,
                  },
              }
          )
```

### Rest API

#### Request

POST: `file_chunk/invode`

```
{
  "input":{
    "enable_recursive_chunk_parse": flase,
    "recursive_chunk_size": 128,
    "recursive_chunk_overlap": 0,
    "enable_semantic_chunck_parse": false,
    "semantic_embedding_address": "http://fast-embed-server.ops-pilot",
    "ocr_provider_address": "http://ocr-server.ops-pilot",
    "enable_ocr_parse": false,
    "excel_header_row_parse": false,
    "excel_full_content_parse": false,
    "custom_metadata": {
    
    },
    "file": "",
    "file_name": ""
  }
}
```

| param                        | desc                         |
| ---------------------------- | ---------------------------- |
| enable_recursive_chunk_parse | Enable recursive chunk parse |
| recursive_chunk_size         | Recursive chunk size         |
| recursive_chunk_overlap      | Recursive chunk overlap      |
| enable_semantic_chunck_parse | Enable semantic chunk parse  |
| semantic_embedding_address   | Semantic embedding address   |
| ocr_provider_address         | OCR provider address         |
| enable_ocr_parse             | Enable OCR parse             |
| excel_header_row_parse       | Excel header row parse       |
| excel_full_content_parse     | Excel full content parse     |
| custom_metadata              | Custom metadata              |
| file                         | File to parse,base64 string  |
| file_name                    | File name                    |

#### Response

```
{
  "output":[
    {
      "id":"",
      "metadata":{
        "format":"table", // image
      },
      "page_content":"",
      "type":"Document"
    }
  ]
}
```

## Web Page Scraping And Parsing

### LangServe API

```python
web_page_remote = RemoteRunnable(WEB_PAGE_CHUNK_SERVICE_URL)
remote_docs = web_page_remote.invoke(
              {
                  "enable_recursive_chunk_parse": true
                  "recursive_chunk_size": 256,
                  "recursive_chunk_overlap": 0,
                  "enable_semantic_chunck_parse": false,
                  "semantic_embedding_address": "",
                  "url": "",
                  "max_depth": 1,
                  "custom_metadata": {
                      "knowledge_type": "webpage",
                      "knowledge_id": knowledge.id,
                      "knowledge_title": knowledge.title,
                      "knowledge_folder_id": knowledge.knowledge_base_folder.id,
                      **knowledge.custom_metadata,
                  },
              }
          )
```

### Rest API

#### Request

POST: `webpage_chunk/invoke`

```
{
    "input":{
        "enable_recursive_chunk_parse": false,
        "recursive_chunk_size": 128,
        "recursive_chunk_overlap": 0,
        "enable_semantic_chunck_parse": false,
        "semantic_embedding_address": "http://fast-embed-server.ops-pilot",
        "ocr_provider_address": "http://ocr-server.ops-pilot",
        "enable_ocr_parse": false,
        "excel_header_row_parse": false,
        "excel_full_content_parse": false,
        "custom_metadata": {
      
        },
        "url": "",
        "max_depth": 1,
    }
}
```

| param                        | desc                         |
| ---------------------------- | ---------------------------- |
| enable_recursive_chunk_parse | Enable recursive chunk parse |
| recursive_chunk_size         | Recursive chunk size         |
| recursive_chunk_overlap      | Recursive chunk overlap      |
| enable_semantic_chunck_parse | Enable semantic chunk parse  |
| semantic_embedding_address   | Semantic embedding address   |
| ocr_provider_address         | OCR provider address         |
| enable_ocr_parse             | Enable OCR parse             |
| excel_header_row_parse       | Excel header row parse       |
| excel_full_content_parse     | Excel full content parse     |
| custom_metadata              | Custom metadata              |
| url                          | URL to parse                 |
| max_depth                    | Max depth to parse           |

#### Response

```
{
  "output":[
    {
      "id":"",
      "metadata":{
        "format":"table", // image
      },
      "page_content":"",
      "type":"Document"
    }
  ]
}
```

## Manual Content Parsing

### LangServe API
```python
manual_remote = RemoteRunnable(MANUAL_CHUNK_SERVICE_URL)
remote_docs = manual_remote.invoke(
              {
                  "enable_recursive_chunk_parse": true,
                  "recursive_chunk_size": 256,
                  "recursive_chunk_overlap": 0,
                  "enable_semantic_chunck_parse": false,
                  "semantic_embedding_address": "",
                  "content": "",
                  "custom_metadata": {
                      "knowledge_type": "manual",
                      "knowledge_id": knowledge.id,
                      "knowledge_title": knowledge.title,
                      "knowledge_folder_id": knowledge.knowledge_base_folder.id,
                      **knowledge.custom_metadata,
                  },
              }
          )

```
### Rest API

#### Request

POST: `manual_chunk/invoke`
```
{
    "input":{
        "enable_recursive_chunk_parse": false,
        "recursive_chunk_size": 128,
        "recursive_chunk_overlap": 0,
        "enable_semantic_chunck_parse": false,
        "semantic_embedding_address": "http://fast-embed-server.ops-pilot",
        "ocr_provider_address": "http://ocr-server.ops-pilot",
        "enable_ocr_parse": false,
        "excel_header_row_parse": false,
        "excel_full_content_parse": false,
        "custom_metadata": {
      
        },
        "content": ""
    }
}
```

| param                        | desc                         |
| ---------------------------- | ---------------------------- |
| enable_recursive_chunk_parse | Enable recursive chunk parse |
| recursive_chunk_size         | Recursive chunk size         |
| recursive_chunk_overlap      | Recursive chunk overlap      |
| enable_semantic_chunck_parse | Enable semantic chunk parse  |
| semantic_embedding_address   | Semantic embedding address   |
| ocr_provider_address         | OCR provider address         |
| enable_ocr_parse             | Enable OCR parse             |
| excel_header_row_parse       | Excel header row parse       |
| excel_full_content_parse     | Excel full content parse     |
| custom_metadata              | Custom metadata              |
| content                      | Content to parse             |

#### Response

```
{
  "output":[
    {
      "id":"",
      "metadata":{
        "format":"table", // image
      },
      "page_content":"",
      "type":"Document"
    }
  ]
}
```
