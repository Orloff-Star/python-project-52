from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Label


User = get_user_model()

class LabelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.label = Label.objects.create(name='Bug')

    def test_label_list_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bug')

    def test_status_update_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('label_update', args=[self.label.pk]), {'name': 'Updated label'})
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated label')

    def test_label_create_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('label_create'), {'name': 'Feature'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Feature').exists())

    def test_label_delete_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('label_delete', args=[self.label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
    
    def test_unauthorized_access(self):
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 302)