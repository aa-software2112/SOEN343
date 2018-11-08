import requests


def test_sum():
	assert 1 == 1


def test_index_page():
	r = requests.get("http://127.0.0.1:5000")
	assert r.status_code == 200


def test_login_page():
	r = requests.get("http://127.0.0.1:5000/login")
	assert r.status_code == 200
