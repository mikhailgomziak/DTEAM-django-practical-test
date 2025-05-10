from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from main.models import CV


class CVViewSetTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up data for the tests."""
        cls.cv_data = {
            "firstname": "John",
            "lastname": "Doe",
            "bio": "A bio for John Doe"
        }
        cls.cv = CV.objects.create(**cls.cv_data)

    # Test for Create: POST
    def test_create_cv(self):
        url = '/api/cvs/'  # Direct URL to the list endpoint for creating CVs
        new_cv_data = {
            "firstname": "Jane",
            "lastname": "Doe",
            "bio": "A bio for Jane Doe"
        }
        response = self.client.post(url, new_cv_data, format='json')

        # Assert that the CV is created successfully with status 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['firstname'], new_cv_data['firstname'])
        self.assertEqual(response.data['lastname'], new_cv_data['lastname'])
        self.assertEqual(response.data['bio'], new_cv_data['bio'])

    # Test for Retrieve: GET
    def test_retrieve_cv(self):
        url = f'/api/cvs/{self.cv.pk}/'  # Direct URL to the detail endpoint for this CV
        response = self.client.get(url, format='json')

        # Assert status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the data returned is correct
        self.assertEqual(response.data['firstname'], self.cv.firstname)
        self.assertEqual(response.data['lastname'], self.cv.lastname)
        self.assertEqual(response.data['bio'], self.cv.bio)

    # Test for Update: PUT
    def test_update_cv(self):
        url = f'/api/cvs/{self.cv.pk}/'  # Direct URL to the detail endpoint for updating
        updated_cv_data = {
            "firstname": "Updated",
            "lastname": "User",
            "bio": "Updated bio"
        }
        response = self.client.put(url, updated_cv_data, format='json')

        # Assert that the update was successful with status 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Reload the cv instance and check if it was updated
        self.cv.refresh_from_db()
        self.assertEqual(self.cv.firstname, updated_cv_data['firstname'])
        self.assertEqual(self.cv.lastname, updated_cv_data['lastname'])
        self.assertEqual(self.cv.bio, updated_cv_data['bio'])

    # Test for Delete: DELETE
    def test_delete_cv(self):
        url = f'/api/cvs/{self.cv.pk}/'  # Direct URL to the detail endpoint for deleting
        response = self.client.delete(url, format='json')

        # Assert status code is 204 (No Content) for successful deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert that the CV is no longer in the database
        self.assertFalse(CV.objects.filter(pk=self.cv.pk).exists())
