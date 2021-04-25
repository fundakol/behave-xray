import re

from behave_xray.model import XrayStatus


def get_test_execution_key_from_tag(tag):
    match = re.match(r"^jira\.test_execution\('(.+)'\)$", tag, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None


def get_test_plan_key_from_tag(tag):
    match = re.match(r"^jira\.test_plan\('(.+)'\)$", tag, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None


def get_testcase_key_from_tag(tag):
    match = re.match(r"^(allure|jira)\.testcase\(['\"](.+)['\"]\)$", tag, flags=re.IGNORECASE)
    if match:
        return match.group(2)
    # for outline scenario
    match = re.match(r"^(allure|jira)\.testcase(.+)$", tag, flags=re.IGNORECASE)
    if match:
        return match.group(2)
    else:
        return None


def get_overall_status(statuses):
    if XrayStatus.FAIL in statuses:
        return XrayStatus.FAIL
    if set(statuses) == set([XrayStatus.TODO]):
        return XrayStatus.TODO
    if set(statuses) == set([XrayStatus.EXECUTING]):
        return XrayStatus.EXECUTING
    if XrayStatus.EXECUTING in statuses or XrayStatus.TODO in statuses:
        return XrayStatus.EXECUTING
    if set(statuses) == set([XrayStatus.PASS]):
        return XrayStatus.PASS
    return XrayStatus.TODO
