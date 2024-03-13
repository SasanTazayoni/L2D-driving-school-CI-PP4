from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from profiles.models import UserProfile


class HomeViewTest(TestCase):
    """
    Test to see if home page renders correctly.
    """
    def test_home_view(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')


class AppointmentsViewTest(TestCase):
    """
    Tests to see is appointments page works properly.
    """
    def setUp(self):
        self.client = Client()
        self.testuser = User.objects.create_user(
            first_name='Fake',
            username='fakeuser',
            email='fakeuser@fakemail.com',
            password='password'
        )

    def test_unauthenticated_user(self):
        """
        Testing unauthenticated user.
        """
        response = self.client.get(reverse('appointments'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/appointments/')

    def test_authenticated_user_with_unapproved_profile(self):
        """
        Testing authenticated, unapproved user.
        """
        self.client.login(username='fakeuser', password='password')
        if not UserProfile.objects.filter(user=self.testuser).exists():
            UserProfile.objects.create(user=self.testuser, approved=False)

        response = self.client.get(reverse('appointments'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contact'))

    def test_authenticated_user_with_approved_profile(self):
        """
        Testing authenticated, approved user.
        """
        self.client.login(username='fakeuser', password='password')

        if hasattr(self.testuser, 'profile'):
            self.testuser.profile.approved = True
            self.testuser.profile.save()
        else:
            UserProfile.objects.create(user=self.testuser, approved=True)

        response = self.client.get(reverse('appointments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/appointments.html')
       

class ContactViewTest(TestCase):
    """
    Test to see if contact page renders correctly.
    """
    def test_contact_view(self):
        client = Client()
        response = client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')


class UserProfileSearchViewTest(TestCase):
    """
    Test user search on user profiles page.
    """
    def setUp(self):
        self.factory = RequestFactory()

        self.user1 = User.objects.create_user(
            first_name='John',
            username='johnsmith',
            email='john@example.com',
            password='password'
        )

        self.user2 = User.objects.create_user(
            first_name='Jane',
            username='janedoe',
            email='jane@example.com',
            password='password'
        )

    def test_search_bar_with_empty_query(self):
        url = reverse('user_profiles')
        request = self.factory.get(url, {'search_query': ''})
        response = self.client.get(url, {'search_query': ''})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'No results found')

    def test_search_bar_with_results(self):
        url = reverse('user_profiles')
        request = self.factory.get(url, {'search_query': 'John'})
        response = self.client.get(url, {'search_query': 'John'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')


class UserProfilePaginationViewTest(TestCase):
    """
    Test pagination on user profiles page.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.users = []

        for i in range(15):
            user = User.objects.create_user(
                first_name=f'User{i}',
                username=f'user_{i}',
                email=f'user_{i}@example.com',
                password='password'
            )

            profile, created = UserProfile.objects.get_or_create(user=user)
            self.users.append((user, profile))
    
    def test_pagination(self):
        url = reverse('user_profiles')
        request = self.factory.get(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        user_profiles = (
            UserProfile.objects
            .all()
            .order_by('user__first_name')
        )

        page = request.GET.get('page')
        results = 12
        paginator = Paginator(user_profiles, results)

        self.assertEqual(paginator.num_pages, 2)

        if page == 1:
            self.assertEqual(len(user_profiles_page.object_list), 12)
        elif page == 2:
            self.assertEqual(len(user_profiles_page.object_list), 3)


class ProfileDetailViewTest(TestCase):
    """
    Test to see if user profile page renders correctly with a given id.
    """
    def setUp(self):
        self.testuser = User.objects.create_user(
            first_name='Fake',
            username='fakeuser',
            email='fakeuser@fakemail.com',
            password='password'
        )
        
        if not UserProfile.objects.filter(user=self.testuser).exists():
            self.testuser_profile = UserProfile.objects.create(user=self.testuser)

        self.testuser_id = self.testuser.id

    def test_profile_detail_view(self):
        url = reverse('profile_detail', kwargs={'user_id': self.testuser.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/profile_detail.html')