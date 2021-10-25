from django.test import TestCase

# Create your tests here.

class DatabaseTestCase(TestCase):
    def test_query_output(self):
        from testApp.models import ExampleModel
        self.assertEqual(ExampleModel.objects.all().query, "koekoek")