from datetime import timedelta
from django.utils import timezone
from oauth2_provider.models import Application, AccessToken
from rest_framework.test import APITestCase
from user.models import *
from project.models import *


class TestProject(APITestCase):

    def setUp(self) -> None:
        # set up project manager user
        self.user_1 = User.objects.create_user(email='some_email@invalid.com', password='some_123_password')
        self.user_1.position = 'project manager'
        self.user_1.save()

        # set up developer user
        self.user_2 = User.objects.create_user(email='some__other_email@invalid.com', password='some_123_password')
        self.user_1.position = 'developer'
        self.user_2.save()

        # set up a project
        self.project = Project.objects.create(title='some project title', description='some project description',
                                              owner=self.user_1)

        # set up a task
        self.task = Task.objects.create(title='some task title', description='some task description',
                                        project=self.project)

        # assign task to a user
        self.assigned_task = AssignTask.objects.create(task=self.task, user=self.user_1)

        # set up oauth2 app
        self.app = Application.objects.create(
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.authorization_grant_type,
            redirect_uris='https://www.none.com/oauth2/callback',
            name='dummy',
            user=self.user_1
        )

        # set up token for user 1
        self.access_token_user_1 = AccessToken.objects.create(
            user=self.user_1,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=300),
            token='secret-access-token-key',
            application=self.app
        )

    def tearDown(self) -> None:
        pass

    def test_add_project(self):
        url = "/api/project/add_project/"
        data = {
            'title': "some_other_title",
            'description': 'some other description blah blah'
        }
        response = self.client.post(path=url, data=data, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 201)

    def test_add_task(self):
        url = "/api/project/add_task/"
        data = {
            'title': "some_other_title",
            'description': 'some other description blah blah',
            'project_id': self.project.id
        }
        response = self.client.post(path=url, data=data, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 201)

    def test_assign_task(self):
        url = "/api/project/assign_task/"
        data = {
            'task': self.task.id,
            'user': self.user_2.id
        }
        response = self.client.post(path=url, data=data, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 201)

    def test_list_of_all_project_by_project_manager(self):
        url = "/api/project/list_of_projects/"

        response = self.client.get(path=url, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 200)

    def test_list_of_all_project_by_developer(self):
        url = "/api/project/list_of_projects/"
        self.user_1.position = 'developer'
        self.user_1.save()
        response = self.client.get(path=url, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 403)
        self.user_1.position = 'project manager'
        self.user_1.save()

    def test_retrieve_project(self):
        url = f"/api/project/project/{self.project.id}/"
        response = self.client.get(path=url, **{'authorization': f'Bearer {self.access_token_user_1}'})

        self.assertEqual(response.status_code, 200)

    def test_retrieve_project_by_developer(self):
        url = f"/api/project/project/{self.project.id}/"
        self.user_1.position = 'developer'
        self.user_1.save()
        response = self.client.get(path=url, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 403)
        self.user_1.position = 'project manager'
        self.user_1.save()

    def test_retrieve_task_by_developer(self):
        url = f"/api/project/project_tasks/{self.project.id}/"
        self.user_1.position = 'developer'
        self.user_1.save()
        response = self.client.get(path=url, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 200)
        self.user_1.position = 'project manager'
        self.user_1.save()

    def test_retrieve_task_by_project_manager(self):
        url = f"/api/project/project_tasks/{self.project.id}/"
        response = self.client.get(path=url, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 200)

    def test_retrieve_project_users_by_project_manager(self):
        url = f"/api/project/project_users/{self.project.id}/"
        response = self.client.get(path=url, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 200)

    def test_retrieve_project_users_by_developer(self):
        url = f"/api/project/project_users/{self.project.id}/"
        self.user_1.position = 'developer'
        self.user_1.save()
        response = self.client.get(path=url, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 200)
        self.user_1.position = 'project manager'
        self.user_1.save()

    def test_retrieve_user_tasks(self):
        url = "/api/project/user_task/"
        self.user_1.position = 'developer'
        self.user_1.save()
        response = self.client.get(path=url, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 200)
        self.user_1.position = 'project manager'
        self.user_1.save()

    def test_sign_up(self):
        url = "/api/user/signup/"
        data = {
            'email': "john@doe.com",
            'password': 'some other description blah blah',
            'firstname': 'John',
            'lastname': "Doe"
        }
        response = self.client.post(path=url, data=data, **{'authorization': f'Bearer {self.access_token_user_1}'})
        self.assertEqual(response.status_code, 201)
