import pytest
import requests
import json


@pytest.fixture()
def base_url(request):
    url = request.config.getoption("--url")
    return url


@pytest.fixture()
def users_url():
    return "api/users"


@pytest.fixture()
def exist_user_url():
    return "api/users/2"


@pytest.fixture()
def get_users_code():
    return 200


@pytest.fixture()
def create_user_code():
    return 201


@pytest.fixture()
def update_users_code():
    return 200


@pytest.fixture()
def delete_users_code():
    return 204


@pytest.fixture()
def list_users_fields():
    return ["page",
            "per_page",
            "total",
            "data",
            "ad",
            ]


@pytest.fixture()
def user_name_field():
    return "name"


@pytest.fixture()
def user_job_field():
    return "job"


@pytest.fixture()
def create_user_fields(user_name_field, user_job_field):
    return [user_name_field,
            user_job_field,
            "id",
            "createdAt",
            ]


@pytest.fixture()
def update_user_fields(user_name_field, user_job_field):
    return [user_name_field,
            user_job_field,
            "updatedAt",
            ]


def headers_json_content_type():
    headers = {
        'Content-Type': 'application/json',
    }
    return headers


@pytest.fixture()
def create_user_headers():
    headers = headers_json_content_type()
    return headers


@pytest.fixture()
def update_user_headers():
    headers = headers_json_content_type()
    return headers


@pytest.fixture()
def page_field():
    return "page"


@pytest.fixture()
def per_page_field():
    return "per_page"


@pytest.fixture()
def total_field():
    return "total"


@pytest.fixture()
def total_pages_field():
    return "total_pages"


@pytest.fixture()
def data_field():
    return "data"


@pytest.fixture()
def page_option():
    return "page"


def test_list_users_fields(base_url, users_url, list_users_fields, get_users_code):
    r = requests.get(base_url + users_url)

    assert get_users_code == r.status_code

    data = r.json()
    for field in list_users_fields:
        assert field in data


def test_list_users_pagination(base_url, users_url, page_field, per_page_field, total_field, total_pages_field, data_field, page_option):
    r = requests.get(base_url + users_url)
    data = r.json()

    per_page = data[per_page_field]
    total = data[total_field]
    total_pages = data[total_pages_field]

    expected_pages = total // per_page
    if total % per_page:
        expected_pages = expected_pages + 1

    assert expected_pages == total_pages

    total_users = 0

    for i in range(1, total_pages + 1):
        r = requests.get(base_url + users_url, params={page_option: i})
        data = r.json()

        page = data[page_field]

        assert page == i

        users = data[data_field]
        users_count = len(users)
        assert users_count <= per_page
        total_users += users_count

    assert total_users <= total


def test_create_user(base_url, users_url, create_user_code, create_user_headers,
                     user_name_field, user_job_field,
                     create_user_fields):
    name = "test_name"
    job = "test_job"

    json_data = {user_name_field: name,
                 user_job_field: job
                 }

    json_data = json.dumps(json_data)

    r = requests.post(base_url + users_url, data=json_data, headers=create_user_headers)

    assert create_user_code == r.status_code

    data = r.json()
    for field in create_user_fields:
        assert field in data

    assert data[user_name_field] == name
    assert data[user_job_field] == job


def test_update_user(base_url, exist_user_url, update_users_code, update_user_headers,
                     user_name_field, user_job_field,
                     update_user_fields):
    name = "update_name"
    job = "update_job"

    json_data = {user_name_field: name,
                 user_job_field: job
                 }

    json_data = json.dumps(json_data)

    r = requests.put(base_url + exist_user_url, data=json_data, headers=update_user_headers)

    assert update_users_code == r.status_code

    data = r.json()
    for field in update_user_fields:
        assert field in data

    assert data[user_name_field] == name
    assert data[user_job_field] == job


def test_delete_user(base_url, exist_user_url, delete_users_code):
    r = requests.delete(base_url + exist_user_url)

    assert delete_users_code == r.status_code
