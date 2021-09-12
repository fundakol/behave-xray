from behave import *


@when("I add {a:g} and {b:g}")
def step_impl(context, a, b):
    context.result = a + b


@then("result is {result:g}")
def step_impl(context, result):
    assert context.result == result, 'Not equal'
