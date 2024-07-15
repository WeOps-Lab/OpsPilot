import sys

from integrations.jenkins_integration import JenkinsIntegration
from loguru import logger


def test_list_jenkins_job():
    integration = JenkinsIntegration()
    result = integration.list_jenkins_job("test")
    logger.info(result)


def test_build_jenkins_job():
    integration = JenkinsIntegration()
    result = integration.build_jenkins_job("OpsPilot-doc-ci", "test")
    logger.info(result)


def test_get_build_log():
    integration = JenkinsIntegration()
    result = integration.get_build_log("OpsPilot-doc-ci", "test")
    logger.info(result)
