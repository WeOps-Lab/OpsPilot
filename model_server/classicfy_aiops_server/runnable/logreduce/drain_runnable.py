import base64
from typing import List

from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from langchain_core.runnables import RunnableLambda
from tqdm import tqdm

from user_types.logreduce.drain_request import DrainRequest
from user_types.logreduce.drain_entity import DrainEntity


class DrainRunnable:
    def execute(self, request: DrainRequest) -> List[DrainEntity]:
        response: List[DrainEntity] = []

        content = base64.b64decode(request.file.encode("utf-8")).decode("utf-8")

        # split content to lines
        lines = content.split("\n")

        config = TemplateMinerConfig()
        config.load('conf/drain/drain3.ini')
        config.profiling_enabled = False
        template_miner = TemplateMiner(config=config)

        results = {}
        for log in tqdm(lines):
            log = log.rstrip()
            log = log.partition(': ')[2]
            result = template_miner.add_log_message(log)
            cluster_id = result['cluster_id']
            results[cluster_id] = {
                'template': result['template_mined'],
                'size': result['cluster_size']
            }

        for cluster_id, result in results.items():
            response.append(DrainEntity(cluster_id=cluster_id, template=result['template'], size=result['size']))

        return response

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=DrainRequest, output_type=DrainEntity)
