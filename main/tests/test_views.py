from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from main.models import CV

class CVAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cv_data = {
            "firstname": "John",
            "lastname": "Doe",
            "bio": "Test bio for John Doe."
        }
        cls.cv = CV.objects.create(**cls.cv_data)

    # 1. Test Create
    def test_create_cv(self):
        url = reverse('cv-list')  # The list endpoint for creating CV
        response = self.client.post(url, self.cv_data, format='json')
        
        # Assert the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Assert the response data contains the fields we just sent
        self.assertEqual(response.data['firstname'], self.cv_data['firstname'])
        self.assertEqual(response.data['lastname'], self.cv_data['lastname'])
        self.assertEqual(response.data['bio'], self.cv_data['bio'])

    # 2. Test Retrieve (Get)
    def test_retrieve_cv(self):
        url = reverse('cv-detail', args=[self.cv.pk])  # The detail endpoint for this specific CV
        response = self.client.get(url, format='json')

        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert the response data matches the CV data
        self.assertEqual(response.data['firstname'], self.cv.firstname)
        self.assertEqual(response.data['lastname'], self.cv.lastname)
        self.assertEqual(response.data['bio'], self.cv.bio)

    # 3. Test Update (Put)
    def test_update_cv(self):
        url = reverse('cv-detail', args=[self.cv.pk])  # The detail endpoint for this specific CV
        updated_data = {
            "firstname": "Updated",
            "lastname": "User",
            "bio": "Updated bio."
        }
        response = self.client.put(url, updated_data, format='json')

        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the CV object from the database to check updated fields
        self.cv.refresh_from_db()

        # Assert the CV was updated in the database
        self.assertEqual(self.cv.firstname, updated_data['firstname'])
        self.assertEqual(self.cv.lastname, updated_data['lastname'])
        self.assertEqual(self.cv.bio, updated_data['bio'])

    # 4. Test Delete
    def test_delete_cv(self):
        url = reverse('cv-detail', args=[self.cv.pk])  # The detail endpoint for this specific CV
        response = self.client.delete(url, format='json')

        # Assert the response status code is 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert the CV object no longer exists in the database
        self.assertFalse(CV.objects.filter(pk=self.cv.pk).exists())
