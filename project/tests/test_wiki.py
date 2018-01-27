import unittest

from project.tests.base import BaseTestCase

class TestWikiBlueprint(BaseTestCase):

    render_templates = False
    
    def test_index(self):
        response = self.client.get('/')
        self.assert_template_used('index.html')

if __name__ == '__main__':
    unittest.main()