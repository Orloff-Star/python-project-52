from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Status

User = get_user_model()

class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.status = Status.objects.create(name="Test Status")

    def test_status_list_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Status")

    def test_status_create_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('status_create'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('status_update', args=[self.status.pk]), {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    '''def test_unauthorized_access(self):
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 302)'''
