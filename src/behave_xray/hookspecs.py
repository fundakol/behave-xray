import pluggy


hookspec = pluggy.HookspecMarker('xray')


@hookspec
def scenario_xray_result(result, scenario):
    """
    Update Xray result for the scenario.

    :param result: Xray result
    :param scenario: behave scenario
    """
