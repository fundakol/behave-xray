from collections import defaultdict, namedtuple
from dataclasses import dataclass, field
from os import environ

from behave.formatter.base import Formatter
from behave.model import Status as ScenarioStatus
from behave_xray.helper import (get_test_execution_key_from_tag,
                                get_test_plan_key_from_tag,
                                get_testcase_key_from_tag,
                                get_overall_status)
from behave_xray.model import XrayStatus, TestCase, TestExecution
from behave_xray.xray_publisher import XrayPublisher


@dataclass
class TCStatus:
    testcase_key: str = None
    statuses: list = field(default_factory=list)
    comment: str = ''
    is_outline: bool = False


class XrayFormatter(Formatter):
    name = 'xray'
    description = 'Jira XRAY formatter'

    def __init__(self, stream, config):
        super().__init__(stream, config)
        self.reset()
        jira_url = environ["XRAY_API_BASE_URL"]
        auth = (environ["XRAY_API_USER"], environ["XRAY_API_PASSWORD"])
        self.xray_publisher = XrayPublisher(base_url=jira_url, auth=auth)

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def reset(self):
        self.current_feature = None
        self.current_scenario = None
        self.current_test_key = None
        self.test_execution = TestExecution()
        self.testcases = defaultdict(lambda: TCStatus())

    def feature(self, feature):
        self.current_feature = feature
        if feature.tags:
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

        if scenario.tags:
            for tag in scenario.tags:
                testcase_key = get_testcase_key_from_tag(tag)
                if testcase_key:
                    self.current_test_key = testcase_key
                    self.testcases[testcase_key].is_outline = self.is_scenario_outline()

    def get_verdict(self, result):
        Verdict = namedtuple('Verdict', 'status message')
        if self.current_scenario.status == ScenarioStatus.passed:
            return Verdict(XrayStatus.PASS, '')
        if result.status == ScenarioStatus.failed:
            return Verdict(XrayStatus.FAIL, result.error_message)
        if result.status == ScenarioStatus.untested:
            return Verdict(XrayStatus.TODO, 'Untested')
        if result.status == ScenarioStatus.skipped:
            return Verdict(XrayStatus.ABORTED, self.current_scenario.skip_reason)

    def result(self, result):
        if self.current_scenario.status == ScenarioStatus.untested:
            return

        if self.current_test_key is None:
            return

        verdict = self.get_verdict(result)
        self.testcases[self.current_test_key].statuses.append(verdict.status)
        if not self.is_scenario_outline():
            self.testcases[self.current_test_key].comment = verdict.message

    def eof(self):
        """End of feature"""
        if self.config.dry_run:
            return

        for tc_id, tc_status in self.testcases.items():
            testcase = TestCase(test_key=tc_id)
            if tc_status.is_outline:
                testcase.status = get_overall_status(tc_status.statuses)
                testcase.examples = tc_status.statuses
            else:
                testcase.status = tc_status.statuses[0]
                testcase.comment = tc_status.comment
            self.test_execution.append(testcase)

        if self.test_execution.tests:
            self.xray_publisher.publish(self.test_execution)
        self.test_execution.flush()
        self.reset()
