import pytest
from model.services import CodeCategorizationService
import warnings
warnings.filterwarnings('ignore')
@pytest.fixture
def python_service():
    return CodeCategorizationService(
        model_path="model/models_ai/trained_model",
        csv_path="model/data/all_python_codes.csv"
    )


def test_predict_category(python_service):
    sample_code = "def test():\n    return 42"
    category = python_service.predict_category(sample_code)
    assert isinstance(category, str)


def test_search_codes_by_category(python_service):
    category = "example_category"
    results = python_service.search_codes_by_category(category)
    assert isinstance(results, list)
    if results:
        assert "code" in results[0]