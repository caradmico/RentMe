from unittest.mock import MagicMock, patch

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase, override_settings

from houseme_project.settings import require_production_secret


class ProductionSecretTests(SimpleTestCase):
    def test_placeholder_rejected_when_debug_false(self):
        for placeholder in ('', 'change-me', 'your-secret-key-here'):
            with self.subTest(secret=placeholder):
                with self.assertRaises(ImproperlyConfigured):
                    require_production_secret(placeholder, debug=False)

    def test_placeholder_allowed_when_debug_true(self):
        require_production_secret('change-me', debug=True)

    def test_real_key_ok_when_debug_false(self):
        require_production_secret('a-real-non-placeholder-secret', debug=False)


class WhiteNoiseMiddlewareTests(SimpleTestCase):
    def test_whitenoise_follows_security_middleware(self):
        from django.conf import settings

        middleware = settings.MIDDLEWARE
        security = 'django.middleware.security.SecurityMiddleware'
        whitenoise = 'whitenoise.middleware.WhiteNoiseMiddleware'
        self.assertIn(security, middleware)
        self.assertIn(whitenoise, middleware)
        self.assertLess(middleware.index(security), middleware.index(whitenoise))


@override_settings(SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies')
class IndexViewTests(SimpleTestCase):
    @patch('houseme_app.views.Application.objects.filter')
    def test_home_ok_with_no_listings(self, mock_filter):
        qs = MagicMock()
        qs.select_related.return_value.order_by.return_value = []
        mock_filter.return_value = qs
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'HouseMe')
        self.assertContains(response, 'Gonna Git Housed')
