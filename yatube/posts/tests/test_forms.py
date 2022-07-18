from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.models import Group, Post
from posts.forms import PostForm

User = get_user_model()


class PostCreateForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
            id='1',
        )

        cls.form = PostForm()
        cls.form_data = {
            'text': 'Тестовый пост',
            'group': cls.group.id,
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        post_count = Post.objects.count()
        post = Post.objects.all()[0]
        response = self.authorized_client.post(
            reverse('posts:create_post'),
            data=self.form_data,
            follow=True
        )

        self.assertRedirects(
            response,
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username}
            )
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(post.text, self.form_data['text'])

    def test_post_edit(self):
        post_count = Post.objects.count()
        form_data = {
            'text': 'Другой тестовый текст',
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )

        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            )
        )
        self.assertEqual(Post.objects.count(), post_count)

        response1 = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),)
        self.assertContains(response1, form_data['text'])
