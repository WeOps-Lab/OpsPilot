import base64
from io import StringIO
from typing import List

import pandas as pd
from langchain_core.runnables import RunnableLambda
from causality.inference.search import IC
from causality.inference.independence_tests import RobustRegressionTest
from user_types.causation.causality_request import CausalityRequest
import networkx as nx


class CausalityRunnable:
    def execute(self, request: CausalityRequest) -> List[str]:
        response: List[str] = []

        content = base64.b64decode(request.file.encode("utf-8")).decode("utf-8")
        # read csv content to pandas dataframe
        data = pd.read_csv(StringIO(content))
        variable_types = {col: 'd' for col in data.columns}

        # 进行因果推断
        ic_algorithm = IC(RobustRegressionTest)
        graph = ic_algorithm.search(data, variable_types)

        # 获取不满足条件的边
        edges_to_remove = []
        for node1, node2, data in graph.edges(data=True):
            if not (data.get('marked', False) and data.get('arrows', [])):
                edges_to_remove.append((node1, node2))
        # 从图中剔除不满足条件的边
        graph.remove_edges_from(edges_to_remove)

        # 使用DiGraph类型
        graph = nx.DiGraph(graph)
        # 获取前一半的边
        edges_to_keep = list(graph.edges())[:len(graph.edges()) // 2]
        # 创建新的有向图，只包含前一半的边
        graph = nx.DiGraph(edges_to_keep)

        roots = [node for node in graph.nodes() if graph.in_degree(node) == 0]
        return roots

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=CausalityRequest, output_type=List[str])
