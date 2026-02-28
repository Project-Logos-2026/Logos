import pathlib
import pytest

EXTERNAL_PATH_FRAGMENTS = [
    "External_Enhancements",
    "ML_Wrapper",
    "NLP_Wrapper",
    "Visualization_Wrapper",
    "Graph_Wrapper",
]

def pytest_collection_modifyitems(config, items):
    for item in items:
        path_str = str(item.fspath)
        if any(fragment in path_str for fragment in EXTERNAL_PATH_FRAGMENTS):
            item.add_marker(pytest.mark.external_wrapper)
