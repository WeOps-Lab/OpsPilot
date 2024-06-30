from apps.bot_mgmt.services.automation_service import AutomationService
from loguru import logger


def test_salt_runner():
    service = AutomationService()
    result = service.execute_salt_local('cmd.run', '*', 'pwd')
    logger.info(result)
