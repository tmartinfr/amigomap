from django.apps import apps
from django.test import TestCase

from app.apps import AppConfig


class AppConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(AppConfig.name, 'app')
        self.assertEqual(apps.get_app_config('app').name, 'app')
