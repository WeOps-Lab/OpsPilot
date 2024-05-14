from actions.services.automation_service import AutomationService


def test_ping():
    r = AutomationService()
    rs = r.execute_salt_local('test.ping', '*', None)
    print(rs)
