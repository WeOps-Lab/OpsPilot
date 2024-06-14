from typing import List

from apps.model_provider_mgmt.models import RerankModelChoices, RerankProvider
from BCEmbedding.tools.langchain import BCERerank
from langchain_core.documents import Document


class RerankService:
    def __init__(self):
        self.cache = {}

    def predict(self, rerank_provider: RerankProvider, rerank_top_k, sentences: List[str], query):
        reranker = self.get_reranker(rerank_provider, rerank_top_k)
        docs = []
        for sentence in sentences:
            docs.append(Document(page_content=sentence))
        compressed_data = reranker.compress_documents(docs, query)
        results = []
        for doc in compressed_data:
            results.append(
                {
                    "score": doc.metadata.get("relevance_score"),
                    "page_content": doc.page_content,
                }
            )
        return results

    def clean_cache(self, rerank_provider_id):
        if rerank_provider_id in self.cache:
            del self.cache[rerank_provider_id]

    def get_reranker(self, rerank_provider: RerankProvider, rerank_top_k):
        cache_key = f"{rerank_provider.id}_{rerank_top_k}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        rerank_model_config = rerank_provider.decrypted_rerank_config_config
        reranker = None

        if rerank_provider.rerank_model == RerankModelChoices.BCE:
            reranker_args = {
                "model": rerank_model_config["model"],
                "top_n": rerank_top_k,
            }
            reranker = BCERerank(**reranker_args)

        self.cache[cache_key] = reranker
        return reranker


rerank_service = RerankService()
