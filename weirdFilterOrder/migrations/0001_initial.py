# Generated by Django 3.2.8 on 2021-10-25 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExampleModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("attribute_a", models.CharField(max_length=32)),
                ("attribute_b", models.CharField(max_length=32)),
                ("attribute_c", models.CharField(max_length=32)),
            ],
        )
    ]
