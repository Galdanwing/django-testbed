from django.test import TestCase
from weirdFilterOrder.models import ExampleModel


# Create your tests here.

class DatabaseTestCase(TestCase):
    def test_query_output_default_manager(self):
        query = ExampleModel.objects.filter(attribute_c=True, attribute_b=True, attribute_a = True).query
        expected_output = 'SELECT "weirdFilterOrder_examplemodel"."id",' \
                          ' "weirdFilterOrder_examplemodel"."attribute_a",' \
                          ' "weirdFilterOrder_examplemodel"."attribute_b",' \
                          ' "weirdFilterOrder_examplemodel"."attribute_c"' \
                          ' FROM "weirdFilterOrder_examplemodel"' \
                          ' WHERE ("weirdFilterOrder_examplemodel"."attribute_a"' \
                          ' AND "weirdFilterOrder_examplemodel"."attribute_b"' \
                          ' AND "weirdFilterOrder_examplemodel"."attribute_c")'
        self.assertEqual(str(query), expected_output)
    #
    def test_query_output_alphabetical_manager(self):
        query = ExampleModel.alphabetical_order_objects.all().query
        expected_output = 'SELECT "weirdFilterOrder_examplemodel"."id",' \
                          ' "weirdFilterOrder_examplemodel"."attribute_a",' \
                          ' "weirdFilterOrder_examplemodel"."attribute_b",' \
                          ' "weirdFilterOrder_examplemodel"."attribute_c"' \
                          ' FROM "weirdFilterOrder_examplemodel"' \
                          ' WHERE ("weirdFilterOrder_examplemodel"."attribute_a"' \
                          ' AND "weirdFilterOrder_examplemodel"."attribute_b"' \
                          ' AND "weirdFilterOrder_examplemodel"."attribute_c")'
        self.assertEqual(str(query),expected_output)

    def test_query_output_ordered_manager(self):
        query = ExampleModel.filter_order_objects.all().query
        expected_output = 'SELECT "weirdFilterOrder_examplemodel"."id",' \
                          ' "weirdFilterOrder_examplemodel"."attribute_a",' \
                          ' "weirdFilterOrder_examplemodel"."attribute_b",' \
                          ' "weirdFilterOrder_examplemodel"."attribute_c"' \
                          ' FROM "weirdFilterOrder_examplemodel"' \
                          ' WHERE ("weirdFilterOrder_examplemodel"."attribute_c"' \
                          ' AND "weirdFilterOrder_examplemodel"."attribute_b"' \
                          ' AND "weirdFilterOrder_examplemodel"."attribute_a")'
        self.assertEqual(str(query), expected_output)
