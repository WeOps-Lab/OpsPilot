from typing import List

from BCEmbedding.tools.langchain import BCERerank
from django.core.cache import cache
from langchain_core.documents import Document

from apps.model_provider_mgmt.models import RerankProvider, RerankModelChoices


class RerankService:
    def predict(self, rerank_provider: RerankProvider, rerank_top_k, sentences: List[str], query):
        reranker = self.get_reranker(rerank_provider, rerank_top_k)
        docs = []
        for sentence in sentences:
            docs.append(Document(page_content=sentence))
        compressed_data = reranker.compress_documents(docs, query)
        results = []
        for doc in compressed_data:
            results.append({
                'score': doc.metadata.get('relevance_score'),
                'page_content': doc.page_content
            })
        return results

    def get_reranker(self, rerank_provider: RerankProvider, rerank_top_k):
        reranker = cache.get(f'{rerank_provider.id}_{rerank_top_k}')

        if reranker is None:
            rerank_model_config = rerank_provider.decrypted_rerank_config_config
            if rerank_provider.rerank_model == RerankModelChoices.BCE:
                reranker_args = {
                    'model': rerank_model_config['model'],
                    'top_n': rerank_top_k
                }
                reranker = BCERerank(**reranker_args)

            cache.set(f'{rerank_provider.id}_{rerank_top_k}', reranker, 3600)

        return reranker
