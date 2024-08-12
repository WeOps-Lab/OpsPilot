Chunk-Server is responsible for knowledge partitioning, supports semantic and length partitioning of files, and has a variety of knowledge partitioning options

# API

## File Partitioning

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

### Response

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

### Response

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

### Response

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
