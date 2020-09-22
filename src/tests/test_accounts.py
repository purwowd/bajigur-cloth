from django.urls import reverse, resolve
from django.test import TestCase

from accounts.views import auth
from accounts.forms import UserCreationForm


class AccountTests(TestCase):

    def setUp(self):
        url = reverse('auth')
        self.res = self.client.get(url)

    def test_account_auth_status_code(self):
        url = reverse('auth')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_auth_url_resolve_auth_view(self):
        view = resolve('/accounts/auth/')

        self.assertEqual(view.func, auth)

    def test_csrf(self):
        self.assertContains(self.res, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.res.context.get('form')

        self.assertNotIsInstance(form, UserCreationForm)
