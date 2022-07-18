# from django.test import TestCase, Client
# from django.contrib.auth import get_user_model
# from http import HTTPStatus
# from django.core.cache import cache

# from posts.models import Group, Post


# User = get_user_model()


# class PostURLTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.guest_client = Client()
#         cls.user = User.objects.create_user(username='test_user')
#         cls.author = User.objects.create_user(username='author')
#         cls.group = Group.objects.create(
#             title='Тестовая группа',
#             slug='test_slug',
#             description='группа для тестов',
#         )
#         cls.post = Post.objects.create(
#             author=cls.author,
#             text='Тестовый пост',
#             id=1,
#         )

#         cls.template_url_names = {
#             '/': 'posts/index.html',
#             f'/group/{cls.group.slug}/': 'posts/group_list.html',
#             f'/profile/{cls.user.username}/': 'posts/profile.html',
#             f'/posts/{cls.post.id}/': 'posts/post_detail.html',
#             '/create/': 'posts/create_post.html',
#             f'/posts/{cls.post.id}/edit/': 'posts/create_post.html',
#             '/unexisting_page/': 'core/404.html'
#         }
#     def setUp(self):
#         self.authorized_client = Client()
#         self.authorized_client.force_login(self.user)
#         self.author_client = Client()
#         self.author_client.force_login(self.author)
#         cache.clear()

#     def test_homepage(self):
#         response = self.guest_client.get('/')
#         self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_group_added_url_exists_at_desired_location(self):
#         """Страница /group/ доступна любому пользователю."""
#         response = self.guest_client.get(f'/group/{self.group.slug}/')
#         self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_profile_added_url_exists_at_desired_location(self):
#         """Страница /profile/ доступна любому пользователю."""
#         response = self.guest_client.get(f'/profile/{self.user.username}/')
#         self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_posts_added_url_exists_at_desired_location(self):
#         """Страница /posts/ доступна любому пользователю."""
#         response = self.guest_client.get(f'/posts/{self.post.id}/')
#         self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_unexisting_page_added_url_exists_at_desired_location(self):
#         """Страница /unexisting_page/ доступна любому пользователю."""
#         response = self.guest_client.get('/unexisting_page/')
#         self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

#     def test_create_new_post(self):
#         """Страница /create/ доступна автору поста."""
#         response = self.guest_client.get('/create/', follow=True)
#         self.assertRedirects(response, '/auth/login/?next=/create/')
#         response = self.authorized_client.get('/create/', follow=True)
#         self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_edit_post(self):
#         """Страница /edit/ доступна автору поста."""
#         response = self.guest_client.get(f'/posts/{self.post.id}/edit/')
#         self.assertEqual(response.status_code, HTTPStatus.FOUND)
#         response = self.author_client.get(f'/posts/{self.post.id}/edit/')
#         self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_urls_uses_correct_template(self):
#         """URL-адрес использует соответствующий шаблон."""
#         for address, template in self.template_url_names.items():
#             with self.subTest(address=address):
#                 response = self.author_client.get(address)
#                 self.assertTemplateUsed(response, template)
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from http import HTTPStatus


from posts.models import Group, Post


User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='test_user')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.author = User.objects.create_user(username='author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='группа для тестов',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый пост',
            id=1,
        )

        cls.template_url_names = {
            '/': 'posts/index.html',
            f'/group/{cls.group.slug}/': 'posts/group_list.html',
            f'/profile/{cls.user.username}/': 'posts/profile.html',
            f'/posts/{cls.post.id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{cls.post.id}/edit/': 'posts/create_post.html',
        }

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_added_url_exists_at_desired_location(self):
        """Страница /group/ доступна любому пользователю."""
        response = self.guest_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_added_url_exists_at_desired_location(self):
        """Страница /profile/ доступна любому пользователю."""
        response = self.guest_client.get(f'/profile/{self.user.username}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_added_url_exists_at_desired_location(self):
        """Страница /posts/ доступна любому пользователю."""
        response = self.guest_client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting_page_added_url_exists_at_desired_location(self):
        """Страница /unexisting_page/ доступна любому пользователю."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_new_post(self):
        """Страница /create/ доступна автору поста."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')
        response = self.authorized_client.get('/create/', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_post(self):
        """Страница /edit/ доступна автору поста."""
        response = self.guest_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.author_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for url, template in self.template_url_names.items():
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertTemplateUsed(response, template)
