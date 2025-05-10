from django.test import TestCase
from django.urls import reverse
from main.models import CV

class CVViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cv = CV.objects.create(firstname="Test", lastname="User", bio="Just a test user.")

    def test_cv_list_view_status_code(self):
        response = self.client.get(reverse('cv-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")

    def test_cv_detail_view_status_code(self):
        response = self.client.get(reverse('cv-detail', args=[self.cv.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")

    def test_cv_detail_404(self):
        response = self.client.get(reverse('cv-detail', args=[999]))
        self.assertEqual(response.status_code, 404)
