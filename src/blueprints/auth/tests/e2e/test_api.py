import pytest
import src.config as config
import requests


@pytest.mark.usefixtures('in_memory_db')
def test_register():
    url = config.get_api_url()
    r = requests.post(
        f'{url}/auth/register',
        json={"username":"david7", "password":"abc123", "created_at": "2022-12-07"}
    )
    assert r.status_code == 200
