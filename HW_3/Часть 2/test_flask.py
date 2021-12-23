import pytest
from web_hello_world import (
    app as hello_world_app, 
    DEFAULT_GREETING_COUNT, 
    MAX_GREETING_COUNT, 
    REALY_TO_MANY_GREETING_COUNT,
)

@pytest.fixture
def client():
    with hello_world_app.test_client() as client:
        yield client

def test_service_reply_to_root_path(client):
    respoanse = client.get("/")
    assert "world" in respoanse.data.decode(respoanse.charset)


def test_service_reply_to_username(client):
    respoanse = client.get("/hello/Vasya")
    assert "Vasya" in respoanse.data.decode(respoanse.charset)

def test_service_reply_to_username_with_default_num(client):
    username = "Vasya"
    respoanse = client.get(f"/hello/{username}", follow_redirects=True)
    respoanse_text = respoanse.data.decode(respoanse.charset)
    vasya_count = respoanse_text.count(username)
    assert DEFAULT_GREETING_COUNT == vasya_count


def test_service_reply_to_username_serveral_times(client):
    username = "Petya"
    expected_greeting_count = 15
    respoanse = client.get(f"/hello/{username}/{expected_greeting_count}")
    respoanse_text = respoanse.data.decode(respoanse.charset)
    petya_count = respoanse_text.count(username)
    assert expected_greeting_count == petya_count


def test_service_reply_to_escaped_username(client):
    non_escaped_tag = "<br>"
    username = "Petya"
    expected_greeting_count = 12
    respoanse = client.get(f"/hello/{non_escaped_tag}{username}/{expected_greeting_count}")
    respoanse_text = respoanse.data.decode(respoanse.charset)
    petya_count = respoanse_text.count(username)
    assert expected_greeting_count == petya_count   
    assert 0 == respoanse_text.count(non_escaped_tag)


def test_service_hello_to_username_with_slash(client):
    username = "Vasya"
    respoanse = client.get(f"/hello/{username}/")
    assert 200 == respoanse.status_code


def test_service_reply_to_username_with_too_many_num(client):
    username = "Petya"
    supplied_greeting_count = MAX_GREETING_COUNT + 1
    expected_greeting_count = DEFAULT_GREETING_COUNT
    respoanse = client.get(f"/hello/{username}/{supplied_greeting_count}", follow_redirects=True)
    respoanse_text = respoanse.data.decode(respoanse.charset)
    petya_count = respoanse_text.count(username)
    assert expected_greeting_count == petya_count   


def test_service_reply_to_username_with_realy_too_many_num(client):
    username = "Petya"
    supplied_greeting_count = REALY_TO_MANY_GREETING_COUNT
    respoanse = client.get(f"/hello/{username}/{supplied_greeting_count}", follow_redirects=True)
    assert 404 == respoanse.status_code 
    
    respoanse_text = respoanse.data.decode(respoanse.charset)
    petya_count = respoanse_text.count(username)
    assert 0 == petya_count   
    



