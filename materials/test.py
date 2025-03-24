from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Lesson, Course
from users.models import CustomUser
class LessonListCreateTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user("testuser@gmail.com", password="testpassword", username="testuser")
        self.course = Course.objects.create(title="Test course", description="test description", owner=self.user)
        self.lessons = Lesson.objects.create(course=self.course, title="Test Lessons", description="Testing views", video_link="https://www.youtube.com/watch", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get(self):
        # Testing GET-request API
        url = r'http://127.0.0.1:8000/api/lessons/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        # Testing POST-request API
        url = r'http://127.0.0.1:8000/api/lessons/'
        data = {
            'course': 1,
            'title': 'New test lesson',
            'description': 'test description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LessonRetrieveUpdateDestroyTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user("testuser@gmail.com", password="testpassword",
                                                   username="testuser")
        self.course = Course.objects.create(title="Test course", description="test description", owner=self.user)
        self.lessons = Lesson.objects.create(course=self.course, title="Test Lessons", description="Testing views",
                                             video_link="https://www.youtube.com/watch", owner=self.user)
        self.client.force_authenticate(user=self.user)


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