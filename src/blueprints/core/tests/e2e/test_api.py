import pytest
import src.config as config
import requests


@pytest.mark.usefixtures('in_memory_db')
def test_register():
    url = config.get_api_url()

    # Register user
    requests.post(
        f'{url}/auth/register',
        json={"username": "test", "password": "test", "created_at": "2022-12-07"}
    )

    # Login
    r = requests.post(
        f'{url}/auth/login',
        json={"username":"test", "password":"test"}
    )
    token = r.json()['access_token']

    headers = {"Authorization": f"Bearer {token}"}
    # Create todo
    r = requests.post(
        f'{url}/add_todo',
        headers=headers,
        json={"name":"agua", "user_id": 1, "created_at": "2022-12-07"}
    )
    assert r.status_code == 201
