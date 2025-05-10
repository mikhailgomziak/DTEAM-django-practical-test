from django.test import TestCase, Client
from audit.models import RequestLog
from django.contrib.auth.models import User
from django.urls import reverse


class RequestLogMiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='testuser', password='password123')

    def test_request_log_created_for_anonymous_user(self):
        self.client.get('/logs/')
        self.assertEqual(RequestLog.objects.count(), 1)
        log = RequestLog.objects.first()
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.path, '/logs/')
        self.assertIsNone(log.user)

    def test_request_log_created_for_authenticated_user(self):
        self.client.login(username='testuser', password='password123')
        self.client.get('/logs/')
        log = RequestLog.objects.latest('timestamp')
        self.assertEqual(log.user.username, 'testuser')

    def test_static_and_admin_requests_not_logged(self):
        self.client.get('/admin/login/')
        self.assertEqual(RequestLog.objects.count(), 0)
