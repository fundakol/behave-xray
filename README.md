# behave-xray

[![PyPi](https://img.shields.io/pypi/v/behave-xray.png)](https://pypi.python.org/pypi/behave-xray)
[![Build Status](https://github.com/fundakol/behave-xray/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/fundakol/behave-xray/actions?query=workflow?master)
[![codecov](https://codecov.io/gh/fundakol/behave-xray/branch/master/graph/badge.svg?token=VV1DMT3605)](https://codecov.io/gh/fundakol/behave-xray)

### Installation


```shell
$ pip install -U behave-xray
```

or from the source:

```shell
$ python setup.py install
```
### Usage

Add JIRA tags to Gherkin scenario:

```gherkin
# --FILE: tutorial.feature
@jira.test_plan('JIRA-3')
Feature: showing off behave

  @jira.testcase('JIRA-1')
  Scenario: run a simple test
     Given we have behave installed
      When we implement a test
      Then behave will test it for us!

  @jira.testcase('JIRA-2')
  Scenario Outline: Add two numbers in Calc
    Given Calculator is open
    When I add <a> and <b>
    Then result is <result>

  Examples: Sum
      | a | b  | result |
      | 3 | 4  | 7      |
      | 6 | 10 | 18     |
```

Set system environments (Basic authentication) for [Xray Server+DC](https://docs.getxray.app/display/XRAY/REST+API):
```commandline
export XRAY_API_BASE_URL=<jira URL>
export XRAY_API_USER=<jria username>
export XRAY_API_PASSWORD=<user password>
```

Run tests:

```commandline
behave -f behave_xray:XrayFormatter
```

Set system environments (Bearer authentication) for [Xray Cloud](https://docs.getxray.app/display/XRAYCLOUD/REST+API):
```commandline
export XRAY_API_BASE_URL=<jira URL>
export XRAY_CLIENT_ID=<Xray client id>
export XRAY_CLIENT_SECRET=<Xray client secret>
```

Run tests:

```commandline
behave -f behave_xray:XrayCloudFormatter
```

You can register formatter in behave.ini:

```ini
# -- FILE: behave.ini
[behave.formatters]
xray = behave_xray:XrayCloudFormatter
```

and use with shorter name:

```shell
$ behave --f xray
```
