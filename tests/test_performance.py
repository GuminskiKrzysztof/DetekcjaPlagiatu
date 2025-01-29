import pytest
import timeit
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.services import CodeCategorizationService

@pytest.fixture
def python_service():
    return CodeCategorizationService(
        model_path="model/models_ai/trained_model",
        csv_path="model/data/all_python_codes.csv"
    )


def test_predict_category_performance(python_service):
    sample_code = "def test_function():\n    return 42"
    execution_time = timeit.timeit(lambda: python_service.predict_category(sample_code), number=10)
    assert execution_time < 10.0


def test_search_codes_performance(python_service):
    category = "example_category"
    execution_time = timeit.timeit(lambda: python_service.search_codes_by_category(category), number=10)
    assert execution_time < 10.0
