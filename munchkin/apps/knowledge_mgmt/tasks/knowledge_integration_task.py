from dotenv.main import load_dotenv
from celery import shared_task
from loguru import logger

load_dotenv()


@shared_task
def execute_knowledge_integration():
    logger.info("开始执行知识库集成任务....")

    # 获取所有知识库，查看是否配置了知识集成

    # 假如有，那么遍历集成，并且执行集成任务

