from actions.utils.jenkins_utils import JenkinsUtils


def test_list_jenkins_job():
    results = JenkinsUtils().list_jenkins_job()
    print(results)


def test_list_jenkins_job():
    results = JenkinsUtils().find_jenkins_job('ops-pilot')
    print(results)


def test_search_jenkins_job():
    results = JenkinsUtils().search_jenkins_job('rasa')
    print(results)


def test_search_jenkins_job():
    results = JenkinsUtils().trigger_jenkins_pipeline('ops-pilot')
    print(results)


def test_get_jenkins_build_info():
    results = JenkinsUtils().get_jenkins_build_info('ops-pilot', 8)
    print(results)

