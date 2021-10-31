from django.db import models


# Create your models here.
class AlphabeticalOrderObjects(models.Manager):
    def get_queryset(self):
        # This order does not matter, it will become alphabetical
        return super().get_queryset().filter(attribute_c=True, attribute_b=True, attribute_a=True)


class FilteredOrderObjects(models.Manager):
    def get_queryset(self):
        # Because we filter separately here, order does matter
        return super().get_queryset().filter(attribute_c=True).filter(attribute_b=True).filter(attribute_a=True)


class ExampleModel(models.Model):
    attribute_a = models.BooleanField()
    attribute_b = models.BooleanField()
    attribute_c = models.BooleanField()

    class Meta:
        indexes = [models.Index(fields=["attribute_a", "attribute_b", "attribute_c"])]

    alphabetical_order_objects = AlphabeticalOrderObjects()
    filter_order_objects = FilteredOrderObjects()
    objects = models.Manager()
