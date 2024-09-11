from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.core.pagination import (
    PageNumberPaginationWithCount,
)  # Adjust the import as needed

CustomUser = get_user_model()


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
        )
        self.client.force_authenticate(user=self.user)
        self.user_list_url = reverse('user-list')
        self.user_detail_url = reverse('user-detail', kwargs={'pk': self.user.pk})

    def test_list_users(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_user(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User',
        }
        response = self.client.post(self.user_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_retrieve_user(self):
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user(self):
        data = {
            'email': 'testuser@example.com',  # Include email to avoid validation error
            'first_name': 'Updated',
            'last_name': 'User',
        }
        response = self.client.put(self.user_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_delete_user(self):
        response = self.client.delete(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 0)


class CustomUserPaginationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User',
        )
        self.client.force_authenticate(user=self.user)
        # Create test users
        for i in range(10):
            CustomUser.objects.create_user(
                email=f'user{i}@example.com',
                password='password123',
                first_name=f'First{i}',
                last_name=f'Last{i}',
                date_joined=timezone.now() - timezone.timedelta(days=i + 1),
            )
        self.url = reverse('user-list')  # Adjust the URL name as per your setup
        self.page_size = PageNumberPaginationWithCount.page_size

    def test_default_pagination(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']), self.page_size
        )  # Default page size
        self.assertEqual(
            response.data['total_objects'], 11
        )  # Including the admin user
        self.assertEqual(
            response.data['total_pages'], (11 + self.page_size - 1) // self.page_size
        )

    def test_custom_page_size(self):
        custom_page_size = 5
        response = self.client.get(self.url, {'page_size': custom_page_size})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), custom_page_size)
        self.assertEqual(
            response.data['total_objects'], 11
        )  # Including the admin user
        self.assertEqual(
            response.data['total_pages'],
            (11 + custom_page_size - 1) // custom_page_size,
        )

    def test_default_sorting(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['email'], 'admin@example.com'
        )  # Default ordering is '-date_joined'

    def test_custom_sorting(self):
        response = self.client.get(self.url, {'ordering': 'first_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['first_name'], 'Admin'
        )  # Custom ordering by 'first_name'
