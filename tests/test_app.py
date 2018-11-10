import requests, pytest

from app import clientController, adminController

ENDPOINT = "http://127.0.0.1:5000"


def test_index_page():
	""" Query index page unit test"""
	r = requests.get(ENDPOINT)
	assert r.status_code == 200


def test_login_page():
	""" Query login page unit test """
	r = requests.get(ENDPOINT + "/login")
	assert r.status_code == 200


def test_client_login():
	""" Client login unit test """
	r = requests.post(ENDPOINT + "/login")
	assert r.status_code == 200
	client = clientController.get_client_by_password(
		username='antman', password='password1')
	assert client != []


def test_invalid_client_password():
	""" Client invalid login unit test """
	r = requests.post(ENDPOINT + "/login")
	assert r.status_code == 200
	client = clientController.get_client_by_password(
		username='antman', password='passsword1')
	assert client == []


# must work on this one
# def test_logout_client():
# 	""" Query logout page unit test """
# 	r = requests.get(ENDPOINT + "/logout")
# 	assert r.status_code == 200
# 	success = clientController.logout_client('antman')
# 	assert success == True


# valid admin username and password
def test_admin_login():
	""" Admin login unit test """
	r = requests.post(ENDPOINT + "/login")
	assert r.status_code == 200
	admin = adminController.get_admin_by_password(
		username='eagleman', password='password5')
	assert admin != []


# valid admin username invalid password
def test_invalid_admin_password():
	""" Admin invalid login unit test """
	r = requests.post(ENDPOINT + "/login")
	assert r.status_code == 200
	admin = adminController.get_admin_by_password(
		username='eagleman', password='passsword5')
	assert admin == []


def test_view_user_registry():
	""" View user registry unit test """
	r = requests.get(ENDPOINT + "/adminView/adminViewUserRegistry")
	assert r.status_code == 200
	list_of_clients = adminController.get_all_logged_admins() + clientController.get_all_logged_clients()
	assert list_of_clients != None
