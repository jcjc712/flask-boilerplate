import src.config as config
import requests


def test_register():
    url = config.get_api_url()
    r = requests.post(
        f'{url}/auth/register',
        json={"username":"test", "password":"abc123", "created_at": "2022-12-07"}
    )
    assert r.status_code == 200
