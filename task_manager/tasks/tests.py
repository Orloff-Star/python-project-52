from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Status

class TaskViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.status = Status.objects.create(name='To Do')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user
        )

    def test_task_list_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.id,
            'assigned_to': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_update', args=[self.task.pk]), {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'assigned_to': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
    
    def test_task_list_view_authenticated(self):
        """
        Проверяет, что авторизованный пользователь может просматривать список задач.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_list_view_unauthenticated(self):
        """
        Проверяет, что неавторизованный пользователь перенаправляется на страницу входа.
        """
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.assertRedirects(response, '/login/')
        

class TaskDeleteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.status = Status.objects.create(name='To Do')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user1
        )

    def test_delete_task_by_author(self):
        """
        Проверяет, что автор может удалить задачу.
        """
        self.client.login(username='user1', password='testpass')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_task_by_non_author(self):
        """
        Проверяет, что другой пользователь не может удалить задачу.
        """
        self.client.login(username='user2', password='testpass')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())  # Задача не удалена
        # Проверяем, что пользователь был перенаправлен на список задач
        self.assertRedirects(response, reverse('task_list'))