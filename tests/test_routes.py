import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200


def test_dodaj_projekt_route(client):
    response = client.get('/dodaj-projekt')
    assert response.status_code == 200


def test_edytor_route(client):
    response = client.get('/edytor')
    assert response.status_code == 200



def test_python_information(client):
    sample_code = "def sample_function():\n    return 'hello'"
    response = client.post('/python_information', json={"code": sample_code})
    assert response.status_code == 200
    data = response.get_json()
    assert "Information: " in data


def test_cpp_information(client):
    sample_code = "#include <iostream>\nusing namespace std;\nint main() { cout << 'Hello'; return 0; }"
    response = client.post('/cpp_information', json={"code": sample_code})
    assert response.status_code == 200
    data = response.get_json()
    assert "Information: " in data
