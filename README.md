# behave-xray

### Installation

```commandline
python setup.py install
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
```

Set system environments:
```commandline
export XRAY_API_BASE_URL=<jira URL>
export XRAY_API_USER=<jria username>
export XRAY_API_PASSWORD=<user password>
```

Run tests:

```commandline
behave . -f behave_xray.formatter:XrayFormatter
```
