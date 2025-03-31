from django.contrib.auth.models import Permission, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase, APIClient

from materials.models import Lesson, Course
from users.models import CustomUser
class LessonListCreateTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user("testuser@gmail.com", password="testpassword", username="testuser")
        self.course = Course.objects.create(title="Test course", description="test description", owner=self.user)
        self.lessons = Lesson.objects.create(course=self.course, title="Test Lessons", description="Testing views", video_link="https://www.youtube.com/watch", owner=self.user)
        self.client.force_authenticate(user=self.user)


    def get_moder_permissions(self):
        group = Group.objects.create(name="Moders")
        view_course = Permission.objects.get(codename="view_course")
        change_course = Permission.objects.get(codename="change_course")
        change_lesson = Permission.objects.get(codename="change_lesson")
        view_lesson = Permission.objects.get(codename="view_lesson")

        group.permissions.add(view_course, change_course, change_lesson, view_lesson)
        self.user.groups.add(group)

    def test_get(self):
        # Testing GET-request API
        url = r'http://127.0.0.1:8000/api/lessons/'
        response = self.client.get(url)  # -> it'll return a list of Lesson objects
        dict_data = response.json()
        print(dict_data)
        lessons = dict_data['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(lessons.get('title'), 'Test Lessons')
        self.assertEqual(lessons.get('description'), 'Testing views')
        self.assertEqual(lessons.get('video_link'), 'https://www.youtube.com/watch')
        self.assertEqual(lessons.get('owner'), self.user.id)

    def test_post(self):
        # Testing POST-request API
        url = r'http://127.0.0.1:8000/api/lessons/'
        data = {
            'course': 1,
            'title': 'New test lesson',
            'description': 'test description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_permission_denied(self):
        # Testing POST-request API
        url = r'http://127.0.0.1:8000/api/lessons/'
        self.get_moder_permissions()
        data = {
            'course': 1,
            'title': 'New test lesson',
            'description': 'test description'}
        response = self.client.post(url, data, format='json')
        self.assertTrue(response.status_code, status.HTTP_403_FORBIDDEN)


class LessonRetrieveUpdateDestroyTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user("testuser@gmail.com", password="testpassword",
                                                   username="testuser")
        self.course = Course.objects.create(title="Test course", description="test description", owner=self.user)
        self.lessons = Lesson.objects.create(course=self.course, title="Test Lessons", description="Testing views",
                                             video_link="https://www.youtube.com/watch", owner=self.user)
        self.client.force_authenticate(user=self.user)


    def get_moder_permissions(self):
        group = Group.objects.create(name="Moders")
        view_course = Permission.objects.get(codename="view_course")
        change_course = Permission.objects.get(codename="change_course")
        change_lesson = Permission.objects.get(codename="change_lesson")
        view_lesson = Permission.objects.get(codename="view_lesson")

        group.permissions.add(view_course, change_course, change_lesson, view_lesson)
        self.user.groups.add(group)

    def test_update(self):
        url = f'http://127.0.0.1:8000/api/lessons/{self.lessons.id}/'
        data = {
            'title': 'Not a new New test lesson',
            'description': '1test description'}
        response = self.client.patch(url, data, format='json')
        dict_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict_data.get('title'), 'Not a new New test lesson')
        self.assertEqual(dict_data.get('description'), '1test description')


    def test_delete(self):
        url = f'http://127.0.0.1:8000/api/lessons/{self.lessons.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_get_permission_denied(self):
        url = f'http://127.0.0.1:8000/api/lessons/{self.lessons.id}/'
        self.get_moder_permissions()
        response = self.client.get(url)
        self.assertTrue(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get(self):
        url = f'http://127.0.0.1:8000/api/lessons/{self.lessons.id}/'
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Test Lessons')
        self.assertEqual(data.get('description'), 'Testing views')
        self.assertEqual(data.get('video_link'), 'https://www.youtube.com/watch')
        self.assertEqual(data.get('owner'), self.user.id)

class CourseViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user("testuser@gmail.com", password="testpassword", username="testuser")
        self.course = Course.objects.create(title="Test course", description="test description", owner=self.user)
        self.lessons = Lesson.objects.create(course=self.course, title="Test Lessons", description="Testing views", video_link="https://www.youtube.com/watch", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def get_moder_permissions(self):
        group = Group.objects.create(name="Moders")
        view_course = Permission.objects.get(codename="view_course")
        change_course = Permission.objects.get(codename="change_course")
        change_lesson = Permission.objects.get(codename="change_lesson")
        view_lesson = Permission.objects.get(codename="view_lesson")

        group.permissions.add(view_course, change_course, change_lesson, view_lesson)
        self.user.groups.add(group)

    def test_get(self):
        # Testing GET-request API
        url = r'http://127.0.0.1:8000/api/courses/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_object(self):
        # Testing GET-request API
        url = f'http://127.0.0.1:8000/api/courses/{self.course.id}/'
        self.get_moder_permissions()
        response = self.client.get(url)
        dict_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict_data.get('title'), 'Test course')
        self.assertEqual(dict_data.get('description'), 'test description')


    def test_get_object_permission_denied(self):
        # Testing GET-request API
        url = f'http://127.0.0.1:8000/api/courses/{self.course.id}/'
        response = self.client.get(url)
        dict_data = response.json()
        self.assertTrue(response.status_code, HTTP_403_FORBIDDEN)


    def test_post(self):
        # Testing POST-request API
        url = f'http://127.0.0.1:8000/api/courses/'
        data = {
            'title': 'New test course',
            'description': 'test course description'}
        response = self.client.post(url, data, format='json')
        dict_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(dict_data.get('title'), 'New test course')
        self.assertEqual(dict_data.get('description'), 'test course description')

    def test_update(self):
        url = f'http://127.0.0.1:8000/api/courses/{self.course.id}/'
        self.get_moder_permissions()
        data = {
            'title': 'Not a new New test course',
            'description': '1test description'}
        response = self.client.patch(url, data, format='json')
        dict_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict_data.get('title'), 'Not a new New test course')
        self.assertEqual(dict_data.get('description'), '1test description')


    def test_update_permission_denied(self):
        url = f'http://127.0.0.1:8000/api/courses/{self.course.id}/'
        data = {
            'title': 'Not a new New test course',
            'description': '1test description'}
        response = self.client.patch(url, data, format='json')
        self.assertTrue(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_dpermission_denied(self):
        user = CustomUser.objects.create_user("testerror@gmail.com", password="errortestpassword", username="testerroruser")
        course = Course.objects.create(title="Test error course", description="test error description", owner=user)
        url = f'http://127.0.0.1:8000/api/courses/{course.id}/'
        self.get_moder_permissions()
        response = self.client.delete(url)
        self.assertTrue(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        url = f'http://127.0.0.1:8000/api/courses/{self.course.id}/'
        response = self.client.delete(url)
        self.assertTrue(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionCreateDestroyAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user("testuser@gmail.com", password="testpassword", username="testuser")
        self.course = Course.objects.create(title="Test course", description="test description", owner=self.user)
        self.client.force_authenticate(user=self.user)


    def test_post(self):
        # Testing POST-request API
        url = f'http://127.0.0.1:8000/api/subscriptions/create/'
        data = {
            'user': self.user.id,
            'course': self.course.id
        }
        response = self.client.post(url, data, format='json')
        dict_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(dict_data.get('user'), self.user.id)
        self.assertEqual(dict_data.get('course'), self.course.id)

    def test_delete(self):
        url = f'http://127.0.0.1:8000/api/subscriptions/delete/{self.course.id}/'
        response = self.client.delete(url)
        self.assertTrue(response.status_code, status.HTTP_204_NO_CONTENT)