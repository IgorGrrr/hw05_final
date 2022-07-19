from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Comment, Group, Post
from ..forms import CommentForm

User = get_user_model()


class PostCommentsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.group = Group.objects.create(
            title='Test',
            slug='test_slug',
            description='Test group'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )
        cls.form = CommentForm()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_comment_guest_client(self):
        comment_count = Comment.objects.count()

        form_data = {
            'text': 'Test comment',
        }
        response = self.guest_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        comment_create_redirect = (reverse('users:login') + '?next='
                                   + reverse('posts:add_comment',
                                             kwargs={'post_id': self.post.id}))
        self.assertRedirects(response, comment_create_redirect)
        self.assertEqual(Comment.objects.count(), comment_count)

    def test_create_comment_authorized_client(self):
        comment_count = Comment.objects.count()

        form_data = {
            'text': 'Test comment',
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        last_object = Comment.objects.latest('id')
        self.assertEqual(form_data['text'], last_object.text)

