import datetime as dt
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)


DATETIME_FORMAT: str = '%Y-%m-%dT%H:%M:%S%z'
DEFAULT_SUMMARY: str = 'Execution of automated tests'


class TestCase:
    """Class represents Test Case."""
    VALID_STATUSES = (
        'TODO',
        'ABORTED',
        'PASS',
        'FAIL',
        'EXECUTING',
        'PENDING',
        'BLOCKED'
    )

    def __init__(
            self,
            test_key: str = '',
            status: str = 'TODO',
            comment: str = '',
            examples: Optional[List[str]] = None,
            duration: float = 0.0,
    ):
        """
        :param test_key: Test Case ID
        :param status: Status
        :param comment: Comment
        :param examples: Outline tests results
        :param duration: Duration
        """
        self.test_key = test_key
        self.status = status
        self.comment = comment
        self.examples = examples or []
        self.duration = duration

    def __repr__(self):
        return f"{self.__class__.__name__}(test_key='{self.test_key}', status='{self.status}')"

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: str):
        self._validate_status(value)
        self._status = value

    def _validate_status(self, status: str):
        if status not in self.VALID_STATUSES:
            raise ValueError(f'Status must be one of {", ".join(self.VALID_STATUSES)}, but was {status}')

    def as_dict(self) -> Dict[str, str]:
        """Serialize Test Case."""
        return dict(
            testKey=self.test_key,
            status=self.status,
            comment=self.comment,
            examples=self.examples
        )


class TestCaseCloud(TestCase):
    """Class represents Test Case."""

    VALID_STATUSES = (
        'TODO',
        'ABORTED',
        'PASSED',
        'FAILED',
        'EXECUTING',
        'PENDING',
        'BLOCKED'
    )


class TestExecution:

    def __init__(
            self,
            test_execution_key: str = '',
            test_plan_key: str = '',
            user: str = '',
            revision: str = '',
            version: str = '',
            summary: str = '',
            description: str = '',
            tests: Optional[List[TestCase]] = None
    ):
        """
        :param test_execution_key: Test execution Xray ID
        :param test_plan_key: Test plan Xray ID
        :param user: Xray user
        :param revision: Revision
        :param version: Version
        :param summary: Summary
        :param description: Description
        :param tests: list of Test Cases
        """
        self.test_execution_key = test_execution_key
        self.test_plan_key = test_plan_key
        self.user = user
        self.revision = revision
        self.version = version
        self.summary = summary or DEFAULT_SUMMARY
        self.description = description
        self.start_date = dt.datetime.now(tz=dt.timezone.utc)
        self.tests = tests or []

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def append(self, test: Union[dict, TestCase]) -> None:
        """Add test case."""
        if not isinstance(test, TestCase):
            test = TestCase(**test)
        self.tests.append(test)

    def flush(self) -> None:
        """Remove all test cases."""
        self.tests = []

    def as_dict(self) -> Dict[str, Any]:
        """Serialize test execution."""
        tests: List[Dict[str, str]] = [test.as_dict() for test in self.tests]
        info: Dict[str, str] = dict(
            startDate=self.start_date.strftime(DATETIME_FORMAT),
            finishDate=dt.datetime.now(tz=dt.timezone.utc).strftime(DATETIME_FORMAT),
            summary=self.summary,
            description=self.description
        )
        if self.user:
            info['user'] = self.user
        if self.version:
            info['version'] = self.version
        if self.revision:
            info['revision'] = self.revision

        data: Dict[str, Any] = dict(info=info, tests=tests)
        if self.test_plan_key:
            info['testPlanKey'] = self.test_plan_key
        if self.test_execution_key:
            data['testExecutionKey'] = self.test_execution_key
        return data
