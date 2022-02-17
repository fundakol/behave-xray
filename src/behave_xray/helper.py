import re
from typing import List, Optional

from behave.model import Status


def get_test_execution_key_from_tag(tag: str) -> Optional[str]:
    match = re.match(r"^jira\.test_execution\('(.+)'\)$", tag, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None


def get_test_plan_key_from_tag(tag: str) -> Optional[str]:
    match = re.match(r"^jira\.test_plan\('(.+)'\)$", tag, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None


def get_testcase_key_from_tag(tag: str) -> Optional[str]:
    match = re.match(r"^(allure|jira)\.testcase\(['\"](.+)['\"]\)$", tag, flags=re.IGNORECASE)
    if match:
        return match.group(2)
    # for outline scenario
    match = re.match(r'^(allure|jira)\.testcase(.+)$', tag, flags=re.IGNORECASE)
    if match:
        return match.group(2)
    else:
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
