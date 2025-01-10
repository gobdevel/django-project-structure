# -----------------------------------------------------------------------------
# Copyright (c) 2025 Tekyonix
# All rights reserved.
#
#
# Licensed under the MIT License.
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
#
# -----------------------------------------------------------------------------

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.core.pagination import (
    PageNumberPaginationWithCount,
)  # Adjust the import as needed
from apps.users.tests.factories.custom_user import CustomUserFactory

CustomUser = get_user_model()


class UserAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUserFactory(is_staff=True)
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
            'is_staff': False,  # Set is_staff to False for the new user
        }
        response = self.client.post(self.user_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        new_user = CustomUser.objects.get(email='newuser@example.com')
        self.assertFalse(new_user.is_staff)  # Check if is_staff is correctly set

    def test_retrieve_user(self):
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertTrue(
            response.data['is_staff']
        )  # Check if is_staff is correctly retrieved

    def test_update_user(self):
        data = {
            'email': 'testuser@example.com',  # Include email to avoid validation error
            'first_name': 'Updated',
            'last_name': 'User',
            'is_staff': False,  # Update is_staff to False
        }
        response = self.client.put(self.user_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertFalse(
            self.user.is_staff
        )  # Check if is_staff is correctly updated

    def test_delete_user(self):
        response = self.client.delete(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 0)


class CustomUserPaginationTests(APITestCase):
    def setUp(self):
        self.user = CustomUserFactory(
            email='admin@example.com', first_name='Admin', is_staff=True
        )
        self.client.force_authenticate(user=self.user)
        # Create test users
        for i in range(10):
            CustomUserFactory()

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
        )  # Default ordering is '-created_at'

    def test_custom_sorting(self):
        response = self.client.get(self.url, {'ordering': 'first_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['first_name'], 'Admin'
        )  # Custom ordering by 'first_name'

    def test_is_staff_attribute(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        admin_user = response.data['results'][0]
        self.assertTrue(
            admin_user['is_staff']
        )  # Check if is_staff is True for admin user
        for user in response.data['results'][1:]:
            self.assertFalse(
                user['is_staff']
            )  # Check if is_staff is False for other users
