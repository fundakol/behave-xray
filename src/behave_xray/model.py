import datetime as dt
from typing import Dict, List, Union, Any

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


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
            test_key: str = None,
            status: str = 'TODO',
            comment: str = '',
            examples: List[str] = None,
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
            test_execution_key: str = None,
            test_plan_key: str = None,
            user: str = None,
            revision: str = None,
            tests: List[TestCase] = None
    ):
        """
        :param test_execution_key: Test execution Xray ID
        :param test_plan_key: Test plan Xray ID
        :param user: Xray user
        :param revision: Revision
        :param tests: list of Test Cases
        """
        self.test_execution_key = test_execution_key
        self.test_plan_key = test_plan_key or ''
        self.user = user or ''
        self.revision = revision or ''
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
        tests = [test.as_dict() for test in self.tests]
        info = dict(
            startDate=self.start_date.strftime(DATETIME_FORMAT),
            finishDate=dt.datetime.now(tz=dt.timezone.utc).strftime(DATETIME_FORMAT)
        )
        data = dict(info=info, tests=tests)
        if self.test_plan_key:
            info['testPlanKey'] = self.test_plan_key
        if self.test_execution_key:
            data['testExecutionKey'] = self.test_execution_key
        return data
