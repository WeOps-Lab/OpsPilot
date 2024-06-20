from langserve import RemoteRunnable

from apps.model_provider_mgmt.models import RerankModelChoices, RerankProvider


class RerankService:

    def execute(self, rerank_provider: RerankProvider, docs, query, rerank_top_k):
        reranker = None
        if rerank_provider.rerank_model == RerankModelChoices.BCE:
            decrypted_rerank_config_config = rerank_provider.decrypted_rerank_config_config
            reranker = RemoteRunnable(decrypted_rerank_config_config['base_url'])
            params = {
                "docs": docs,
                "query": query,
                "top_n": rerank_top_k
            }
            return reranker.invoke(params)
        return reranker


rerank_service = RerankService()
