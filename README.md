# behave-xray

### Installation


```commandline
pip install -U behave-xray
```

or 

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

Set system environments (Basic authentication):
```shell
export XRAY_API_BASE_URL=<jira URL>
export XRAY_API_USER=<jria username>
export XRAY_API_PASSWORD=<user password>
```

Run tests:

```commandline
behave . -f behave_xray.formatter:XrayFormatter
```

Example for Outline scenario:
```gherkin
# --FILE: tutorial.feature
Feature: showing off behave

    @jira.testcase(<jira>)
    Scenario Outline: Blenders
      Given I put <thing> in a blender,
      When I switch the blender on
      Then it should transform into <other thing>
    
      Examples:
        | thing        | other thing | jira   |
        | iPhone       | toxic waste | JIRA-1 |
        | Galaxy Nexus | toxic waste | JIRA-2 |
```
