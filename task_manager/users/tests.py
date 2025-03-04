from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCRUDTest(TestCase):
    def setUp(self):
        # Создаем пользователя для теста
        self.user = User.objects.create_user(
            first_name='Ivanov',
            last_name='Ivan',
            username='testuser',
            password='testpassword123'
        )
        self.client.login(
            username='testuser',
            password='testpassword123'
        )

    def test_user_creation(self):
        # Данные для регистрации
        data = {
            'first_name': 'Ivanov',
            'last_name': 'Ivan',
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }

        # Отправляем POST-запрос на регистрацию
        response = self.client.post(reverse('register'), data)

        # Проверяем, что пользователь был создан
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.status_code, 302)

    def test_user_update(self):
        # Данные для обновления
        data = {
            'username': 'updateduser',
        }

        # Отправляем POST-запрос на обновление
        response = self.client.post(
            reverse('user_update',
                    args=[self.user.id]), data
        )

        # Проверяем, что данные пользователя были обновлены
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(response.status_code, 302)

    def test_user_deletion(self):
        # Отправляем POST-запрос на удаление
        response = self.client.post(
            reverse('user_delete',
                    args=[self.user.id])
        )

        # Проверяем, что пользователь был удален
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
        self.assertEqual(response.status_code, 302)
