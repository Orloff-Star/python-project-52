from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Status, Label

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


class TaskFilterTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.status1 = Status.objects.create(name='To Do')
        self.status2 = Status.objects.create(name='In Progress')
        self.label1 = Label.objects.create(name='Bug')
        self.label2 = Label.objects.create(name='Feature')
        self.executor1 = User.objects.create_user(username='executor1', password='testpass')
        self.executor2 = User.objects.create_user(username='executor2', password='testpass')

        # Создаем задачи для тестов
        self.task1 = Task.objects.create(
            name='Task 1',
            description='Description 1',
            status=self.status1,
            author=self.user,
            executor=self.executor1
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Task 2',
            description='Description 2',
            status=self.status2,
            author=self.user,
            executor=self.executor2
        )
        self.task2.labels.add(self.label2)

        self.task3 = Task.objects.create(
            name='Task 3',
            description='Description 3',
            status=self.status1,
            author=self.user,
            executor=self.executor1
        )
        self.task3.labels.add(self.label1, self.label2)
        self.client.force_login(self.user)

    def test_filter_by_status(self):
        response = self.client.get(reverse('task_list'), {'status': self.status1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')  # Должна отображаться Task 1
        self.assertContains(response, 'Task 3')  # Должна отображаться Task 3
        self.assertNotContains(response, 'Task 2')  # Task 2 не должна отображаться

    def test_filter_by_executor(self):
        response = self.client.get(reverse('task_list'), {'executor': self.executor1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')  # Должна отображаться Task 1
        self.assertContains(response, 'Task 3')  # Должна отображаться Task 3
        self.assertNotContains(response, 'Task 2')  # Task 2 не должна отображаться

    def test_filter_by_label(self):
        response = self.client.get(reverse('task_list'), {'label': self.label1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')  # Должна отображаться Task 1
        self.assertContains(response, 'Task 3')  # Должна отображаться Task 3
        self.assertNotContains(response, 'Task 2')  # Task 2 не должна отображаться

    def test_filter_by_self_tasks(self):
        # Создаем задачу для другого пользователя
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        Task.objects.create(
            name='Task 4',
            description='Description 4',
            status=self.status1,
            author=other_user,
            executor=self.executor1
        )

        # Фильтруем задачи текущего пользователя
        self.client.force_login(self.user)
        response = self.client.get(reverse('task_list'), {'self_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')  # Должна отображаться Task 1
        self.assertContains(response, 'Task 2')  # Должна отображаться Task 2
        self.assertContains(response, 'Task 3')  # Должна отображаться Task 3
        self.assertNotContains(response, 'Task 4')  # Task 4 не должна отображаться