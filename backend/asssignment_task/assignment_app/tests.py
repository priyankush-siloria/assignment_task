from django.test import TestCase

# Create your tests here.

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


def user_login():
    client = APIClient()
    data = {
        "username": "admin@gmail.com",
        "password": "12345"
    }
    
    response = client.post(path=reverse("assignment_app:login_token"), data=data)
    access_token = response.json()['token']
    return access_token


class AcountsAPIViewTestCase(APITestCase):
    
    def setUp(self):
        self.username = "admin@gmail.com"
        self.first_name = "first_name"
        self.last_name = "last_name"
        self.password = "12345"

    def user_create(self):
        user = User.objects.create_user(
            username=self.username, password=self.password
        )
        
    def user_login(self):
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(path=reverse("assignment_app:login_token"), data=data)
        token = response.json()['token']
        user_id = response.json()['user']
        self.token = token
        self.user_id = user_id
        return token
    
    def create_post(self):
        data = {
            "title": "New Title",
            "body": "new Body",
            "user": self.user_id,
            "is_active": True
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(path=reverse("assignment_app:post"), data=data)
        return response.json()


    def test_Registration_success(self):
        """
        Test to verify registration
        """
        data = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password
        }
        response = self.client.post(path=reverse("assignment_app:Register"), data=data)
        self.assertEqual(201, response.status_code)
    
    def test_Registration_fail(self):
        """
        Test to verify registration with missing fields
        """
        data = {
            "username": self.username,
            "first_name": self.first_name,
        }
        response = self.client.post(path=reverse("assignment_app:Register"), data=data)
        self.assertEqual(400, response.status_code)


    def test_login_success(self):
        """
        Test to verify login success
        """
        self.user_create()

        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(path=reverse("assignment_app:login_token"), data=data)
        self.token = response.json()['token']
        self.assertEqual(200, response.status_code)

    
    def test_login_fail(self):
        """
        Test to verify login success
        """
        self.user_create()

        data = {
            "username": "unknown",
            "password": "password"
        }
        response = self.client.post(path=reverse("assignment_app:login_token"), data=data)
        self.assertEqual(401, response.status_code)
        
    
    def test_logout_success(self):
        """
        Test to verify login success
        """
        self.user_create()
        self.user_login()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(path=reverse("assignment_app:logout"))
        self.assertEqual(200, response.status_code)
    
    def test_logout_fail(self):
        """
        Test to verify login fail with expired token
        """
        self.user_create()
        self.user_login()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "expiredToken")
        response = self.client.get(path=reverse("assignment_app:logout"))
        self.assertEqual(401, response.status_code)


    def test_create_post_success(self):
        """
        Test for Create Post
        """
        self.user_create()
        self.user_login()
        data = {
            "title": "New Title",
            "body": "new Body",
            "user": self.user_id,
            "is_active": True
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(path=reverse("assignment_app:post"), data=data)
        self.assertEqual(201, response.status_code)

    def test_create_post_fail(self):
        """
        Test for Create Post without body(description)
        """
        self.user_create()
        self.user_login()
        data = {
            "title": "New Title",
            "user": self.user_id,
            "is_active": True
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(path=reverse("assignment_app:post"), data=data)
        self.assertEqual(400, response.status_code)


    def test_get_post_success(self):
        """
        Test for get all posts
        """
        self.user_create()
        self.user_login()
        self.create_post()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(path=reverse("assignment_app:post"))
        self.assertEqual(200, response.status_code)

    
    def test_get_post_fail(self):
        """
        Test for get all posts without token
        """
        self.user_create()
        self.user_login()
        self.create_post()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "expired token")
        response = self.client.get(path=reverse("assignment_app:post"))
        self.assertEqual(401, response.status_code)


    def test_get_post_by_id_success(self):
        """
        Test for get post with id
        """
        self.user_create()
        self.user_login()
        new_post = self.create_post()
        post_id  = new_post['data']['id']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(path=reverse("assignment_app:post", kwargs={'postid': post_id}))
        self.assertEqual(200, response.status_code)

    def test_get_post_by_id_fail(self):
        """
        Test for get post with id without register post 
        """
        self.user_create()
        self.user_login()
        post_id = 2323
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(path=reverse("assignment_app:post", kwargs={'postid': post_id}))
        self.assertEqual(404, response.status_code)

    
    def test_update_post_by_id_success(self):
        """
        Test for delete post with id
        """
        self.user_create()
        self.user_login()
        new_post = self.create_post()
        post_id  = new_post['data']['id']
        data = {
            "title": "updated_title"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(path=reverse("assignment_app:post", kwargs={'postid': post_id}), data=data)
        self.assertEqual(200, response.status_code)

    def test_update_post_by_id_fail(self):
        """
        Test for update post with wrong id
        """
        self.user_create()
        self.user_login()
        data = {
            "title": "updated_title"
        }
        post_id = 234234234
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(path=reverse("assignment_app:post", kwargs={'postid': post_id}), data=data)
        self.assertEqual(404, response.status_code)


    def test_delete_post_by_id_success(self):
        """
        Test for delete post with id
        """
        self.user_create()
        self.user_login()
        new_post = self.create_post()
        post_id  = new_post['data']['id']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(path=reverse("assignment_app:post", kwargs={'postid': post_id}))
        self.assertEqual(200, response.status_code)

    def test_delete_post_by_id_fail(self):
        """
        Test for delete post with wrong id
        """
        self.user_create()
        self.user_login()
        new_post = self.create_post()
        post_id  = 2342342
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(path=reverse("assignment_app:post", kwargs={'postid': post_id}))
        self.assertEqual(404, response.status_code)
