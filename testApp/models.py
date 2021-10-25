from django.db import models

# Create your models here.
class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(attribute_c="I should be first", attribute_b="I should be second", attribute_a = "I should be third")

class ExampleModel(models.Model):
    attribute_a = models.CharField(max_length=32)
    attribute_b = models.CharField(max_length=32)
    attribute_c = models.CharField(max_length=32)

    class Meta:
        indexes = [
            models.Index(fields=['attribute_a', 'attribute_b', 'attribute_c']),
        ]
    objects = CustomManager()
    all_objects = models.Manager()