def test_get_users(api_request_context):

    response = api_request_context.get(
        "https://reqres.in/api/users?page=2"
    )

    print(response.status)
    print(response.json())

    assert response.status == 200


def test_create_user(api_request_context):

    payload = {
        "name": "Manoj",
        "job": "GET"
    }

    response = api_request_context.post(
        "https://reqres.in/api/users",
        data=payload
    )

    print(response.json())

    assert response.status == 201


def test_update_user(api_request_context):

    payload = {
        "name": "Manoj",
        "job": "Senior GET"
    }

    response = api_request_context.put(
        "https://reqres.in/api/users/2",
        data=payload
    )

    assert response.status == 200


def test_delete_user(api_request_context):

    response = api_request_context.delete(
        "https://reqres.in/api/users/2"
    )

    assert response.status == 204
 