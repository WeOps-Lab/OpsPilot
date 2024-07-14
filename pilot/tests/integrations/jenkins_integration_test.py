from integrations.jenkins_integration import JenkinsIntegration
from loguru import logger


def test_list_jenkins_job():
    integration = JenkinsIntegration()
    result = integration.list_jenkins_job("test")
    logger.info(result)
