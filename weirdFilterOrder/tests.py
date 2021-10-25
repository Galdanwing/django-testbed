from django.test import TestCase

# Create your tests here.

class DatabaseTestCase(TestCase):
    def test_query_output(self):
        from weirdFilterOrder.models import ExampleModel
        self.assertFalse(str(ExampleModel.objects.all().query).endswith("I should be third)"))
        self.assertTrue(str(ExampleModel.objects.all().query).endswith("I should be first)"))