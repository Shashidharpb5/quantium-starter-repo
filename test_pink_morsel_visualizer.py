from pink_morsel_visualizer import dash_app

def test_header_present(dash_duo):
    dash_duo.start_server(dash_app)
    header = dash_duo.find_element("#header")
    assert "Quantium Pink Morsel Sales Analysis" in header.text

def test_graph_present(dash_duo):
    dash_duo.start_server(dash_app)
    graph = dash_duo.find_element("#visualization")
    assert graph is not None

def test_region_picker_present(dash_duo):
    dash_duo.start_server(dash_app)
    radio = dash_duo.find_element("#region_picker")
    assert radio is not None
