import re
from typing import List, Optional

from behave.model import Status

TEST_CASE_PATTERNS: list[re.Pattern] = [
    re.compile(r'^(TEST_|JIRA\.TESTCASE)(?P<jira_id>[a-zA-Z0-9-_]+)$', flags=re.IGNORECASE),
    re.compile(r"^(allure|jira)\.testcase[\(]*[\"']*(?P<jira_id>[a-zA-Z0-9-_]+)['\"]*[\)]*$", flags=re.IGNORECASE),
]


def get_test_execution_key_from_tag(tag: str) -> Optional[str]:
    """Return Jira Xray test execution ID or None if not defined."""
    match = re.match(r"^jira\.test_execution\('(.+)'\)$", tag, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None


def get_test_plan_key_from_tag(tag: str) -> Optional[str]:
    """Return Jira Xray test plan ID or None if not defined."""
    match = re.match(r"^jira\.test_plan\('(.+)'\)$", tag, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None


def get_testcase_key_from_tag(tag: str) -> Optional[str]:
    """Return Jira Xray test ID or None if not defined."""
    for pattern in TEST_CASE_PATTERNS:
        match = pattern.match(tag)
        if match:
            return match.group('jira_id')
    return None


def get_overall_status(statuses: List[Status]) -> Status:
    """Return overall status for list of statuses."""
    if not len(statuses):
        return Status.untested
    statuses_list = [s.value for s in statuses]
    if len(set(statuses_list)) == 1:
        return statuses[0]
    if Status.failed in statuses:
        return Status.failed
    if Status.executing in statuses:
        return Status.executing
    if Status.undefined in statuses:
        return Status.undefined  # Error
    else:
        statuses = [s for s in statuses if s != Status.untested]
        return get_overall_status(statuses)
