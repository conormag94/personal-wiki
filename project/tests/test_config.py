import os
import unittest

from flask import current_app
from flask_testing import TestCase

from project import create_app

app = create_app()

class TestDevelopmentConfig(TestCase):

    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(app.config['VERIFY_WEBHOOKS'])
        self.assertFalse(current_app is None)

if __name__ == '__main__':
    unittest.main()