RAG Server is a knowledge management module in OpsPilot, which is responsible for knowledge indexing and retrieval.

# API

## Elasticsearch Document Index

POST: `/elasticsearch_index/invoke`

```
{
  "input":{
    "elasticsearch_url":"",
    "elasticsearch_password":"",
    "embed_model_address":"",
    "index_name":"",
    "index_mode":"",
    "chunk_size":100,
    "max_chunk_bytes":1000000,
    "docs":[
      {
        "id":"",
        "metadata":{
          "knowledge_type":"",
          "knowledge_id":1,
          "knowledge_title":"",
          "knowledge_folder_id":1,
          #custom metadata
        },
        "page_content":""
      }
    ]
  }
}
```

| param                  | desc                                       |
| ---------------------- | ------------------------------------------ |
| elasticsearch_url      | ElasticSearch URL                          |
| elasticsearch_password | ElasticSearch password                     |
| embed_model_address    | Embedding model address ,for vector search |
| index_name             | ElasticSearch index name                   |
| index_mode             | Index mode,`overwrite` or `append`         |
| chunk_size             | Chunk size for indexing                    |
| max_chunk_bytes        | Max chunk bytes for indexing               |
| docs                   | Documents to index                         |

### Response

```
{
  "output": true
}
```

## Delete Elasticsearch Index
some times we need to delete hole index or some documents in the index

### Request

POST: `/elasticsearch_delete/invoke`
    
```
{
    "input":{
        "elasticsearch_url":"",
        "elasticsearch_password":"",
        "index_name":"",
        "mode":"delete_index"
        "metadata_filter":{}
    }
}
```

| param | desc |
| ----- | ---- |
| elasticsearch_url | ElasticSearch URL |
| elasticsearch_password | ElasticSearch password |
| index_name | ElasticSearch index name |
| mode | delete mode, `delete_index` or `delete_docs` |
| metadata_filter | Filter document for metadata |


## Elasticsearch RAG

this api is used to retrieve the knowledge from the Elastic Search

### Request

POST: `/elasticsearch_rag/invoke`

```
{
  "input":{
    "elasticsearch_url":"",
    "elasticsearch_password":"",
    "embed_model_address":"",
    "enable_term_search": true,
    "enable_vector_search": true,
    "index_name":"",
    "search_query":"",
    "text_search_weight": 0.9,
    "rag_k": 5,
    "size": 5,
    "rag_num_candidates": 1000,
    "rag_num_passages": 5,
    "vector_search_weight": 0.1,
    "metadata_filter":{

    },
    "enable_rerank": false,
    "rerank_model_address":"",
    "rerank_top_k": 5
  }
}
```

| param                  | desc                                       |
| ---------------------- | ------------------------------------------ |
| elasticsearch_url      | ElasticSearch URL                          |
| elasticsearch_password | ElasticSearch password                     |
| embed_model_address    | Embedding model address ,for vector search |
| enable_term_search     | Enable ElasticSearch full text search      |
| enable_vector_search   | Enable ElasticSearch vector search         |
| index_name             | RAG ElasticSearch index name               |
| search_query           | Search query                               |
| text_search_weight     | Weight for full text search                |
| rag_k                  | Number of top k documents to retrieve      |
| size                   | Number of documents to retrieve            |
| rag_num_candidates     | Number of candidates for elasticsearch knn |
| rag_num_passages       | Number of passages for knn                 |
| vector_search_weight   | Weight for vector search                   |
| metadata_filter        | Filter document for metadata               |
| enable_rerank          | Enable rerank                              |
| rerank_model_address   | Rerank model address                       |
| rerank_top_k           | Rerank top k                               |

### Response

```
{
  "output":[
    {
      "id":"",
      "metadata":{
        "_index":"",
        "_id":"",
        "_score":"",
        "_source":{
            "metadata":{
                "knowledge_type":"",
                "knowledge_id":1,
                "knowledge_title":"",
                "knowledge_folder_id":1,
                #custom metadata
            },
            "vector":[]
        },
        "relevance_score":0.0  # only rerank mode will have this field
      },
      "page_content":"",
      "type":"Document"
    }
  ]
}
```

## Network Retrieval

### Request

POST:  `/network_retrieval/invoke`

```
{
  "input":{
    "query":""
  }
}
```

| param | desc                                    |
| ----- | --------------------------------------- |
| query | Search statements for networked queries |

### Response

```
{
  "output":[
    {
      "id":"",
      "metadata":{

      },
      "page_content":"",
      "type":"Document"
    }
  ]
}
```
