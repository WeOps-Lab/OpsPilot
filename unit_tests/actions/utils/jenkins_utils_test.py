from actions.utils.jenkins_utils import trigger_jenkins_pipeline, find_jenkins_job, get_jenkins_build_info, \
    analyze_jenkins_build_console


def test_trigger_jenkins_pipeline():
    trigger_jenkins_pipeline('Rasa-Sample')


def test_find_jenkins_job():
    assert find_jenkins_job('Rasa-Sample') is True


def test_get_jenkins_build_info():
    get_jenkins_build_info('Rasa-Sample', '12')


def test_get_jenkins_build_console():
    analyze_jenkins_build_console('Rasa-Sample', '21')
