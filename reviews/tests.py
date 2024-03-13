from django.http import HttpResponseRedirect
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from reviews.models import Review, Comment
from profiles.models import UserProfile
from .forms import ReviewForm, CommentForm
from django.core.paginator import Paginator
from reviews.views import ReviewList
from django.utils import timezone


class ReviewListViewPaginationTest(TestCase):
    """
    Test to see if the reviews render correctly with pagination and the average rating.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.users = []

        # Create 10 test users with profiles
        for i in range(10):
            user = User.objects.create_user(
                first_name=f'User{i}',
                username=f'user_{i}',
                email=f'user_{i}@example.com',
                password='password'
            )
            profile, created = UserProfile.objects.get_or_create(user=user)
            self.users.append(profile)

        # Create 10 test reviews with authors set to user profiles
        for i in range(10):
            Review.objects.create(
                author=self.users[i],
                rating=(i % 5) + 1,
                content=f"Content of Test Review {i+1}",
                approved=True,
                created_on=timezone.now() - timezone.timedelta(days=i)
            )

    def test_pagination(self):
        """
        Test for pagination on reviews page.
        """
        url = reverse('reviews')
        request = self.factory.get(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        reviews = Review.objects.all().order_by('-created_on')
        page = request.GET.get('page')
        results_per_page = 6
        paginator = Paginator(reviews, results_per_page)
        self.assertEqual(paginator.num_pages, 2)

        if page == 1:
            self.assertEqual(len(paginator.page(page).object_list), 6)
        elif page == 2:
            self.assertEqual(len(paginator.page(page).object_list), 4)

    def test_average_rating(self):
        """
        Test for average review rating.
        """
        reviews = Review.objects.all()
        total_ratings = sum(review.rating for review in reviews)
        average_rating = total_ratings / len(reviews)
        expected_average_rating = 3
        self.assertAlmostEqual(average_rating, expected_average_rating, delta=0.01)


class ReviewDetailViewTest(TestCase):
    """
    Test to check the review details page for authenticated and non-authenticated users.
    """
    def setUp(self):
        self.testuser = User.objects.create_user(
            first_name='Fake',
            username='fakeuser',
            email='fakeuser@fakemail.com',
            password='password'
        )

        self.testuser.save()
        
        self.review = Review.objects.create(
            author=UserProfile.objects.get_or_create(user=self.testuser)[0],
            rating=4,
            content="Test Review Content",
            approved=True
        )

        self.review_id = self.review.id

    def test_non_authenticated_user(self):
        """
        Non authenticated user view checks to ensure that forms are inaccessible and information
        is read-only.
        """
        url = reverse('review_detail', kwargs={'review_id': self.review.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_detail.html') 
        self.assertNotContains(response, 'button type="submit"', html=True)
        self.assertNotContains(response, '<form id="commentForm" method="POST">')

    def test_authenticated_user(self):
        """
        Authenticated user view checks that comment form and like form is available.
        """
        self.client.login(username='fakeuser', password='password')
        url = reverse('review_detail', kwargs={'review_id': self.review.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_detail.html')
        # Checking if comment form exists
        self.assertRegex(response.content.decode('utf-8'), r'<form\s+id="commentForm"\s+method="POST"')
        # Checking if like form exists
        self.assertRegex(response.content.decode('utf-8'), r'<button[^>]*type="submit"[^>]*name="like_id"')


class EditCommentViewTest(TestCase):
    """
    Test case for editing a comment view.
    """
    def setUp(self):
        self.testuser = User.objects.create_user(
            first_name='Fake',
            username='fakeuser',
            email='fakeuser@fakemail.com',
            password='password'
        )

        self.testuser.save()

        self.review = Review.objects.create(
            author=UserProfile.objects.get_or_create(user=self.testuser)[0],
            rating=4,
            content="Test Review Content",
            approved=True
        )

        self.comment = Comment.objects.create(
            author=UserProfile.objects.get_or_create(user=self.testuser)[0],
            review=self.review,
            content="Test comment"
        )

        self.review_id = self.review.id
        self.comment_id = self.comment.id

    def test_edit_comment_authenticated_user(self):
        """
        Test editing a comment by an authenticated user.
        """
        self.client.login(username='fakeuser', password='password')
        url = reverse('edit_comment', kwargs={'review_id': self.review_id, 'comment_id': self.comment_id})
        response = self.client.get(url)
        form_data = {'content': 'Test comment content'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('review_detail', kwargs={'review_id': self.review.id}), data=form_data)
        self.assertEqual(response.status_code, 200)
        empty_form_data = {}
        empty_form = CommentForm(data=empty_form_data)
        self.assertFalse(empty_form.is_valid())
        empty_response = self.client.post(reverse('review_detail', kwargs={'review_id': self.review.id}), data=empty_form_data)
        self.assertEqual(empty_response.status_code, 200)

    def test_edit_comment_non_authenticated_user(self):
        """
        Test that non-authenticated users cannot access the edit comment view.
        """
        url = reverse('edit_comment', kwargs={'review_id': self.review_id, 'comment_id': self.comment_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class DeleteCommentViewTest(TestCase):
    """
    Test case for deleting a comment view.
    """
    def setUp(self):
        self.testuser = User.objects.create_user(
            first_name='Fake',
            username='fakeuser',
            email='fakeuser@fakemail.com',
            password='password'
        )

        self.testuser.save()

        self.review = Review.objects.create(
            author=UserProfile.objects.get_or_create(user=self.testuser)[0],
            rating=4,
            content="Test Review Content",
            approved=True
        )

        self.comment = Comment.objects.create(
            author=UserProfile.objects.get_or_create(user=self.testuser)[0],
            review=self.review,
            content="Test comment"
        )

        self.review_id = self.review.id
        self.comment_id = self.comment.id

    def test_delete_comment_authenticated_user(self):
        """
        Test deleting a comment by an authenticated user.
        """
        self.client.login(username='fakeuser', password='password')
        url = reverse('delete_comment', kwargs={'review_id': self.review_id, 'comment_id': self.comment_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_comment_non_authenticated_user(self):
        """
        Test that non-authenticated users cannot delete comments.
        """
        url = reverse('delete_comment', kwargs={'review_id': self.review_id, 'comment_id': self.comment_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class CreateReviewViewTest(TestCase):
    """
    Test cases for creating a review.
    """
    def setUp(self):
            self.testuser = User.objects.create_user(
                first_name='Fake',
                username='fakeuser',
                email='fakeuser@fakemail.com',
                password='password'
            )

            self.testuser.save()

    def test_authenticated_user_without_review(self):
        """
        Test the behavior of creating a review for an authenticated user without an existing review.
        """
        self.client.login(username='fakeuser', password='password')
        response = self.client.get(reverse('create_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_form.html')

    def test_authenticated_user_with_existing_review(self):
        """
        Test the behavior of creating a review for an authenticated user with an existing review.
        """
        if not UserProfile.objects.filter(user=self.testuser).exists():
            UserProfile.objects.create(user=self.testuser)
        review = Review.objects.create(author=self.testuser.profile, rating=4, content="Test Review Content", approved=True)
        self.client.login(username='fakeuser', password='password')
        response = self.client.get(reverse('create_review'))
        self.assertRedirects(response, reverse('profile_page'))
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_user(self):
        """
        Test the behavior of attempting to create a review for an authenticated user.
        """
        response = self.client.get(reverse('create_review'))
        self.assertRedirects(response, '/accounts/login/?next=/reviews/create-review/')
        self.assertEqual(response.status_code, 302)

    def test_valid_form_submission(self):
        """
        Test submitting a valid review form.
        """
        self.client.login(username='fakeuser', password='password')
        form_data = {'rating': 4, 'content': 'Valid review content'}
        response = self.client.post(reverse('create_review'), data=form_data)
        self.assertRedirects(response, reverse('profile_page'))
        self.assertEqual(response.status_code, 302)

    def test_invalid_form_submission(self):
        """
        Test submitting an invalid review form.
        """
        self.client.login(username='fakeuser', password='password')
        form_data = {'content': 'Invalid review content'}
        response = self.client.post(reverse('create_review'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_form.html')
        self.assertTrue('form' in response.context)


class UpdateReviewViewTest(TestCase):
    """
    Test cases for updating a review.
    """
    def setUp(self):
        self.testuser = User.objects.create_user(
            first_name='Fake',
            username='fakeuser',
            email='fakeuser@fakemail.com',
            password='password'
        )
        self.testuser.save()

    def test_authenticated_user_with_existing_review(self):
        """
        Test the behavior of the update_review view for an authenticated user with an existing review.
        """
        review = Review.objects.create(author=self.testuser.profile, rating=4, content="Test Review Content", approved=True)
        self.client.login(username='fakeuser', password='password')
        response = self.client.get(reverse('update_review', kwargs={'review_id': review.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_form.html')
    
    def test_authenticated_user_without_review(self):
        """
        Test the behavior of the update_review view for an authenticated user without an existing review.
        """
        self.client.login(username='fakeuser', password='password')
        response = self.client.get(reverse('update_review', kwargs={'review_id': 123}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile_page'))

    def test_unauthenticated_user(self):
        """
        Test the behavior of the update_review view for an unauthenticated user.
        """
        response = self.client.get(reverse('update_review', kwargs={'review_id': 123}))
        self.assertRedirects(response, '/accounts/login/?next=/reviews/update-review/123/')
        self.assertEqual(response.status_code, 302)

    def test_valid_form_submission(self):
        """
        Test submitting a valid review form.
        """
        self.client.login(username='fakeuser', password='password')
        form_data = {'rating': 4, 'content': 'Valid review content'}
        response = self.client.post(reverse('create_review'), data=form_data)
        self.assertRedirects(response, reverse('profile_page'))
        self.assertEqual(response.status_code, 302)

    def test_invalid_form_submission(self):
        """
        Test submitting an invalid review form.
        """
        self.client.login(username='fakeuser', password='password')
        form_data = {'content': 'Invalid review content'}
        response = self.client.post(reverse('create_review'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_form.html')
        self.assertTrue('form' in response.context)

    def test_valid_form_submission(self):
        # Validate form submission for an authenticated user with valid data
        self.client.login(username='fakeuser', password='password')
        form_data = {'rating': 4, 'content': 'Valid review content'}
        response = self.client.post(reverse('create_review'), data=form_data)
        self.assertRedirects(response, reverse('profile_page'))
        self.assertEqual(response.status_code, 302)

    def test_invalid_form_submission(self):
        # Assert that an invalid review form submission renders the review form page again
        self.client.login(username='fakeuser', password='password')
        form_data = {'content': 'Invalid review content'}
        response = self.client.post(reverse('create_review'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_form.html')
        self.assertTrue('form' in response.context)


class DeleteReviewViewTest(TestCase):
    """
    Test cases for deleting a review.
    """
    def setUp(self):
        self.testuser = User.objects.create_user(
            first_name='Fake',
            username='fakeuser',
            email='fakeuser@fakemail.com',
            password='password'
        )
        self.testuser.save()

        # Creating a test review
        self.review = Review.objects.create(
            author=self.testuser.profile,
            rating=4,
            content="Test Review Content",
            approved=True
        )

    def test_authenticated_user_delete_review(self):
        """
        Test deleting a review by an authenticated user.
        """
        self.client.login(username='fakeuser', password='password')
        response = self.client.post(reverse('delete_review', kwargs={'review_id': self.review.id}))
        self.assertRedirects(response, reverse('profile_page'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_unauthenticated_user_delete_review(self):
        """
        Test attempting to delete a review by an unauthenticated user.
        """
        response = self.client.post(reverse('delete_review', kwargs={'review_id': self.review.id}))
        self.assertRedirects(response, '/accounts/login/?next=/reviews/delete-review/1/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())


class LikeToggleViewTest(TestCase):
    """
    Test cases for toggling the like status for a review.
    """
    def setUp(self):
        self.testuser = User.objects.create_user(
            first_name='Fake',
            username='fakeuser',
            email='fakeuser@fakemail.com',
            password='password'
        )
        self.user_profile = UserProfile.objects.get_or_create(user=self.testuser)[0]

        self.review = Review.objects.create(
            author=self.user_profile,
            rating=4,
            content="Test Review Content",
            approved=True
        )
        
    def test_like_toggle(self):
        """
        Test toggling the like status for a review.
        """
        self.client.login(username='fakeuser', password='password')
        like_id = self.review.id
        response = self.client.post(reverse('like_review', args=[like_id]), {'like_id': like_id})
        self.assertIsInstance(response, HttpResponseRedirect)
        updated_review = Review.objects.get(id=like_id)
        self.assertTrue(updated_review.likes.filter(id=self.user_profile.id).exists())
        response = self.client.post(reverse('like_review', args=[like_id]), {'like_id': like_id})
        self.assertIsInstance(response, HttpResponseRedirect)
        updated_review = Review.objects.get(id=like_id)
        self.assertFalse(updated_review.likes.filter(id=self.user_profile.id).exists())
