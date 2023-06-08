from logzero import logger

from actions.utils.jenkins_utils import trigger_jenkins_pipeline, find_jenkins_job, get_jenkins_build_info, \
    analyze_jenkins_build_console, list_jenkins_job, search_jenkins_job


def test_trigger_jenkins_pipeline():
    trigger_jenkins_pipeline('Rasa-Sample')


def test_find_jenkins_job():
    assert find_jenkins_job('Rasa-Sample') is True


def test_get_jenkins_build_info():
    get_jenkins_build_info('Rasa-Sample', '12')


def test_get_jenkins_build_console():
    analyze_jenkins_build_console('Rasa-Sample', '21')


def test_search_jenkins_job():
    print(search_jenkins_job('rasa'))


def test_list_jenkins_job():
    result = list_jenkins_job()
    logger.info(result)
    assert result is not None
