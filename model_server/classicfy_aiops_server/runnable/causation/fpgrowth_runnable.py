import base64
import csv
from io import StringIO
from typing import List

import networkx as nx
from langchain_core.runnables import RunnableLambda

from libs.fp_growth_py3 import find_frequent_itemsets
from user_types.causation.fpgrowth_request import FPGrowthRequest


class FPGrowthRunnable:
    def execute(self, request: FPGrowthRequest) -> List[str]:
        response: List[str] = []

        content = base64.b64decode(request.file.encode("utf-8")).decode("utf-8")

        dataset = []

        reader = csv.reader(StringIO(content))
        headers = next(reader)[1:]
        for row in reader:
            indicators = [header for header, value in zip(headers, row[1:]) if value == '1']
            if len(indicators) > 1:
                dataset.append(indicators)

        min_support = 2
        frequent_itemsets = find_frequent_itemsets(dataset, min_support)

        # 将频繁项集中的元素根据原始顺序进行排序
        headers_index = {item: index for index, item in enumerate(headers)}

        def custom_sort(itemset):
            dic = {}
            for item in itemset:
                dic[headers_index[item]] = item
            dic = sorted(dic.items(), key=lambda k: k[0])
            sorted_itemset = []
            for item in dic:
                sorted_itemset.append(item[1])
            return sorted_itemset

        # 对结果进行进一步处理，仅保留包含两个及以上元素的频繁项，且按顺序
        filter_itemsets = []
        for itemset in frequent_itemsets:
            if len(itemset) > 1:
                itemset = custom_sort(itemset)
                filter_itemsets.append(itemset)

        # 构建边集合
        edges = []
        for itemset in filter_itemsets:
            for i in range(len(itemset) - 1):
                edges.append((itemset[i], itemset[i + 1], {}))

        # 构建有向图
        graph = nx.DiGraph(edges)

        # 找到根因点
        roots = [node for node in graph.nodes() if graph.in_degree(node) == 0]
        return roots

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=FPGrowthRequest, output_type=List[str])
