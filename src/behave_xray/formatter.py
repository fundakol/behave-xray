from collections import defaultdict
from dataclasses import dataclass, field
from os import environ, getenv
from typing import Dict, List, Optional

from behave.formatter.base import Formatter
from behave.model import Status

from behave_xray.authentication import BearerAuth, PersonalAccessTokenAuth
from behave_xray.exceptions import XrayError
from behave_xray.helper import (
    get_test_execution_key_from_tag,
    get_test_plan_key_from_tag,
    get_testcase_key_from_tag,
    get_overall_status
)
from behave_xray.model import TestExecution, TestCase, TestCaseCloud
from behave_xray.xray_publisher import (
    XrayPublisher,
    TEST_EXECUTION_ENDPOINT,
    TEST_EXECUTION_ENDPOINT_CLOUD
)


@dataclass
class ScenarioOutline:
    """Class store Scenario Outline information."""

    testcase_key: Optional[str] = None
    statuses: List[Status] = field(default_factory=list)
    comment: str = ''
    is_outline: bool = False


@dataclass
class Verdict:
    status: Status
    message: str


class _XrayFormatterBase(Formatter):
    name = 'xray'
    description = 'Jira XRAY formatter'

    STATUS_MAPS: Dict[str, str] = {}

    def __init__(self, stream, config, publisher: XrayPublisher):
        super().__init__(stream, config)
        self.xray_publisher = publisher
        self.current_feature = None
        self.current_scenario = None
        self.current_test_key = None
        self.test_execution: TestExecution = TestExecution(
            summary=self._get_summary(),
            user=self._get_user(),
            revision=self._get_revision(),
            version=self._get_version()
        )
        self.testcases: dict = defaultdict(lambda: ScenarioOutline())

    @staticmethod
    def _get_auth(jira_config):
        if jira_config.auth_method == 'bearer':
            auth = BearerAuth(
                base_url=jira_config.jira_url,
                client_id=jira_config.client_id,
                client_secret=jira_config.client_secret
            )
        elif jira_config.auth_method == 'token':
            auth = PersonalAccessTokenAuth(token=jira_config.token)
        else:
            auth = (jira_config.user_name, jira_config.user_password)
        return auth

    def _get_summary(self) -> str:
        return self.config.userdata.get('xray.summary', '')

    def _get_user(self) -> str:
        return self.config.userdata.get('xray.user', '')

    def _get_revision(self) -> str:
        return self.config.userdata.get('xray.revision', '')

    def _get_version(self) -> str:
        return self.config.userdata.get('xray.version', '')

    def reset(self):
        self.current_feature = None
        self.current_scenario = None
        self.current_test_key = None
        self.test_execution = TestExecution()
        self.testcases = defaultdict(lambda: ScenarioOutline())

    def feature(self, feature):
        self.current_feature = feature

        # description is a mandatory Xray field, use feature name if it doesn't have a description
        description_text = '\n'.join(feature.description) if feature.description else feature.name
        self.test_execution.description = description_text
        for tag in feature.tags:
            test_exec_key = get_test_execution_key_from_tag(tag)
            if test_exec_key:
                self.test_execution.test_execution_key = test_exec_key
            test_plan_key = get_test_plan_key_from_tag(tag)
            if test_plan_key:
                self.test_execution.test_plan_key = test_plan_key

    def is_scenario_outline(self):
        return True if 'Scenario Outline' in self.current_scenario.keyword else False

    def scenario(self, scenario):
        self.current_scenario = scenario
        if not scenario.tags:
            return

        for tag in scenario.tags:
            testcase_key = get_testcase_key_from_tag(tag)
            if testcase_key:
                self.current_test_key = testcase_key
                self.testcases[testcase_key].is_outline = self.is_scenario_outline()

    def _get_xray_status(self, status: str) -> str:
        try:
            return self.STATUS_MAPS[status]
        except KeyError:
            return 'TODO'

    def get_verdict(self, step) -> Verdict:
        verdict = Verdict(self.current_scenario.status, '')
        if step.status == Status.failed:
            verdict.message = step.error_message
        if step.status == Status.untested:
            verdict.message = 'Untested'
        if step.status == Status.skipped:
            verdict.message = self.current_scenario.skip_reason
        return verdict

    def result(self, step):
        if self.current_scenario.status == Status.untested:
            return

        if self.current_test_key is None:
            return

        verdict = self.get_verdict(step)
        self.testcases[self.current_test_key].statuses.append(verdict.status)
        if not self.is_scenario_outline():
            self.testcases[self.current_test_key].comment = verdict.message

    @staticmethod
    def _get_test_case(test_key) -> TestCase:
        return TestCase(test_key=test_key)

    def eof(self) -> None:
        if self.config.dry_run:
            return

        self.collect_tests()
        if self.test_execution.tests:
            self.xray_publisher.publish(self.test_execution.as_dict())
        self.test_execution.flush()
        self.reset()

    def collect_tests(self) -> None:
        for tc_id, tc_status in self.testcases.items():
            testcase = self._get_test_case(test_key=tc_id)
            if tc_status.is_outline:
                testcase.status = self._get_xray_status(get_overall_status(tc_status.statuses).name)
                testcase.examples = [self._get_xray_status(s.name) for s in tc_status.statuses]
            else:
                testcase.status = self._get_xray_status(tc_status.statuses[0].name)
                testcase.comment = tc_status.comment
            self.test_execution.append(testcase)


class XrayFormatter(_XrayFormatterBase):
    """Formatter publish test results to Jira Xray."""
    endpoint: str = TEST_EXECUTION_ENDPOINT

    STATUS_MAPS: Dict[str, str] = {
        'untested': 'TODO',
        'skipped': 'ABORTED',
        'passed': 'PASS',
        'failed': 'FAIL',
        'undefined': 'FAIL',  # a step is not implemented
        'executing': 'EXECUTING'
    }

    def __init__(self, stream, config):
        jira_config = _get_jira_config()
        auth = self._get_auth(jira_config=jira_config)
        publisher = XrayPublisher(base_url=jira_config.jira_url, endpoint=self.endpoint, auth=auth)
        super().__init__(stream, config, publisher)


class XrayCloudFormatter(_XrayFormatterBase):
    """Formatter publish test results to Jira Xray Cloud."""
    endpoint: str = TEST_EXECUTION_ENDPOINT_CLOUD
    name = 'xray-cloud'
    STATUS_MAPS = {
        'untested': 'TODO',
        'skipped': 'ABORTED',
        'passed': 'PASSED',
        'failed': 'FAILED',
        'undefined': 'FAILED',  # a step is not implemented
        'executing': 'EXECUTING'
    }

    def __init__(self, stream, config):
        jira_config = _get_jira_config()
        auth = self._get_auth(jira_config=jira_config)
        publisher = XrayPublisher(base_url=jira_config.jira_url, endpoint=self.endpoint, auth=auth)
        super().__init__(stream, config, publisher)

    @staticmethod
    def _get_test_case(test_key):
        return TestCaseCloud(test_key=test_key)


@dataclass
class JiraConfig:
    jira_url: str
    user_name: str = ''
    user_password: str = ''
    client_id: str = ''
    client_secret: str = ''
    token: str = ''

    @property
    def auth_method(self) -> str:
        if self.client_id and self.client_id:
            return 'bearer'  # client id & client secret
        if self.token:
            return 'token'
        else:
            return 'basic'


def _get_jira_config() -> JiraConfig:
    try:
        jira_url = environ['XRAY_API_BASE_URL']
    except KeyError:
        raise XrayError('Environment variable `XRAY_API_BASE_URL` must be set')
    user_name = getenv('XRAY_API_USER', '')
    user_password = getenv('XRAY_API_PASSWORD', '')
    client_id = getenv('XRAY_CLIENT_ID', '')
    client_secret = getenv('XRAY_CLIENT_SECRET', '')
    token = getenv('XRAY_TOKEN', '')
    return JiraConfig(
        user_name=user_name,
        user_password=user_password,
        jira_url=jira_url,
        client_id=client_id,
        client_secret=client_secret,
        token=token
    )
