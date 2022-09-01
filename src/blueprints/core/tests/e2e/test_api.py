import src.config as config
import requests


def test_register():
    url = config.get_api_url()

    # Register user
    requests.post(
        f'{url}/auth/register',
        json={"username": "test", "password": "abc123", "created_at": "2022-12-07"}
    )

    # Login
    r = requests.post(
        f'{url}/auth/login',
        json={"username":"test", "password":"abc123"}
    )
    token = r.json()['access_token']

    headers = {"Authorization": f"Bearer {token}"}
    # Create todo
    r = requests.get(
        f'{url}/',
        headers=headers
    )
    assert r.status_code == 200
