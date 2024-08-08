from typing import List

from langchain_core.documents import Document
from langserve import RemoteRunnable

from munchkin.components.remote_service import RAG_SERVER_URL


class KnowledgeSearchService:

    def search(self, knowledge_base_folders, query, metadata={}, score_threshold=0) -> List[Document]:
        docs = []
        remote_indexer = RemoteRunnable(RAG_SERVER_URL)

        for knowledge_base_folder in knowledge_base_folders:
            embed_model_address = ''
            if knowledge_base_folder.embed_model:
                embed_model_address = knowledge_base_folder.embed_model.embed_config["base_url"]
            rerank_model_address = ''

            if knowledge_base_folder.rerank_model:
                rerank_model_address = knowledge_base_folder.rerank_model.rerank_config["base_url"]
            result = remote_indexer.invoke({
                "embed_model_address": embed_model_address,
                "index_name": knowledge_base_folder.knowledge_index_name(),
                "search_query": query,
                "metadata_filter": metadata,
                "text_search_weight": knowledge_base_folder.text_search_weight,
                "rag_k": knowledge_base_folder.rag_k,
                "rag_num_candidates": knowledge_base_folder.rag_num_candidates,
                "vector_search_weight": knowledge_base_folder.vector_search_weight,
                "enable_rerank": knowledge_base_folder.enable_rerank,
                "rerank_model_address": rerank_model_address,
                "rerank_top_k": knowledge_base_folder.rerank_top_k,
            })
            for doc in result:
                score = doc.metadata['_score'] * 10
                if score > score_threshold:
                    doc_info = {
                        "content": doc.page_content,
                        "score": doc.metadata['_score'] * 10,
                        "knowledge_title": doc.metadata['_source']['metadata']['knowledge_title'],
                        "knowledge_id": doc.metadata['_source']['metadata']['knowledge_id'],
                        "knowledge_folder_id": doc.metadata['_source']['metadata']['knowledge_folder_id'],
                    }
                    if knowledge_base_folder.enable_rerank:
                        doc_info["rerank_score"] = doc.metadata["relevance_score"]
                    docs.append(doc_info)

        return docs
