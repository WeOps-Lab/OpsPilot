from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.knowledge_mgmt.models import KnowledgeBaseFolder, ManualKnowledge
from apps.knowledge_mgmt.serializers.manual_knowledge_serializer import ManualKnowledgeSerializer
from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from django.db.models import Case, IntegerField, Value, When
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action


class ManualKnowledgeViewSet(GuardianModelViewSet):
    serializer_class = ManualKnowledgeSerializer
    queryset = ManualKnowledge.objects.all()
    search_fields = [
        "title",
        "content",
        "custom_metadata",
    ]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "knowledgebase_folder_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                ),
                "query": openapi.Schema(type=openapi.TYPE_STRING),
                "metadata": openapi.Schema(type=openapi.TYPE_OBJECT),
                "score_threshold": openapi.Schema(type=openapi.TYPE_NUMBER),
                "page": openapi.Schema(type=openapi.TYPE_NUMBER),
                "size": openapi.Schema(type=openapi.TYPE_NUMBER),
            },
        ),
    )
    @action(methods=["post"], detail=False, url_path="search")
    def search(self, request):
        data = request.data
        knowledgebase_folder_ids = data.get("knowledgebase_folder_ids")
        query = data.get("query")
        metadata = data.get("metadata", {})
        score_threshold = data.get("score_threshold", 0)
        page = data.get("page", 1)
        size = data.get("size", 10)
        start = (page - 1) * size  # 计算开始的记录
        ordering = data.get("ordering", "-created_at")
        if query:
            service = KnowledgeSearchService()
            knowledgebase_folders = KnowledgeBaseFolder.objects.filter(id__in=knowledgebase_folder_ids)
            docs = service.search(knowledgebase_folders, query, metadata, score_threshold)
            doc_ids = [doc["knowledge_id"] for doc in docs]
            manual_knowledge = ManualKnowledge.objects.filter(id__in=set(doc_ids))

            # 处理特殊排序score
            if "score" in ordering:
                # 去重同时保持顺序
                seen = set()
                ordered_unique_docs_ids = [x for x in doc_ids if not (x in seen or seen.add(x))]
                if "-" not in ordering:  # doc_ids默认是按分数从高到底返回, 如果要按score正序则需要逆向ordered_unique_docs_ids顺序
                    ordered_unique_docs_ids.reverse()

                # 构建排序条件
                preserved_order = Case(
                    *[When(pk=pk, then=Value(i)) for i, pk in enumerate(ordered_unique_docs_ids)],
                    output_field=IntegerField()
                )
                ordering = preserved_order
        else:
            manual_knowledge = ManualKnowledge.objects.all()

        manual_knowledge = manual_knowledge.order_by(ordering)
        total = manual_knowledge.count()  # 获取总记录数
        manual_knowledge = manual_knowledge[start : start + size]  # 应用分页

        serializer = ManualKnowledgeSerializer(manual_knowledge, many=True)
        results = {
            "result": True,
            "data": {
                "count": total,  # 返回总记录数
                "items": serializer.data,
                "page": page,
                "size": size,
                "total_pages": (total + size - 1) // size,  # 计算总页数
            },
        }
        return JsonResponse(results)
