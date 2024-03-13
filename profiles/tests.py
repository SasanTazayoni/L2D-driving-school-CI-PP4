from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client


class ProfilePageViewTest(TestCase):
    """
    Test cases for the profile_page view.
    """
    def setUp(self):
        self.client = Client()
        self.testuser = User.objects.create_user(
            first_name='Fake',
            username='fakeuser',
            email='fakeuser@fakemail.com',
            password='password'
        )

    def test_authenticated_user_profile_page(self):
        """
        Test the profile page for an authenticated user.
        """
        self.client.login(username='fakeuser', password='password')
        response = self.client.get(reverse('profile_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertEqual(response.context['profile'], self.testuser.profile)

    def test_unauthenticated_user_profile_page(self):
        """
        Test that an unauthenticated user is redirected to the login page.
        """
        response = self.client.get(reverse('profile_page'))
        self.assertRedirects(response, '/accounts/login/?next=/profile/')
        self.assertEqual(response.status_code, 302)


class EditProfileViewTest(TestCase):
    """
    Test cases for editing user profile.
    """
    def setUp(self):
        self.testuser = User.objects.create_user(
            first_name='Fake',
            username='fakeuser',
            email='fakeuser@fakemail.com',
            password='password'
        )
        self.testuser.save()

    def test_authenticated_user_edit_profile(self):
        """
        Test editing profile for an authenticated user.
        """
        self.client.login(username='fakeuser', password='password')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit_profile.html')

        self._test_form_submission()

    def test_unauthenticated_user_edit_profile(self):
        """
        Test accessing edit profile page for an unauthenticated user.
        """
        response = self.client.get(reverse('edit_profile'))
        self.assertRedirects(response, '/accounts/login/?next=/profile/edit/')
        self.assertEqual(response.status_code, 302)

    def _test_form_submission(self):
        """
        Test form submission.
        """
        form_data = {}
        response = self.client.post(reverse('edit_profile'), form_data)
        self.assertEqual(response.status_code, 200)


class DeleteProfileViewTest(TestCase):
    """
    Test cases for deleting user profile.
    """
    def setUp(self):
        self.testuser = User.objects.create_user(
            first_name='Fake',
            username='fakeuser',
            email='fakeuser@fakemail.com',
            password='password'
        )
        self.testuser.save()

    def test_authenticated_user_delete_profile(self):
        """
        Test deleting profile for an authenticated user.
        """
        self.client.login(username='fakeuser', password='password')
        response = self.client.post(reverse('delete_profile'))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(User.objects.count(), 0)

    def test_unauthenticated_user_delete_profile(self):
        """
        Test accessing delete profile view for an unauthenticated user.
        """
        response = self.client.post(reverse('delete_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/profile/delete/')
