from behave import then, when


@when('I add {a:g} and {b:g}')
def step_impl(context, a, b):  # noqa: F811
    context.result = a + b


@then('result is {result:g}')
def step_impl(context, result):  # noqa: F811
    assert context.result == result, 'Not equal'
