# Generated by Django 3.2.8 on 2021-10-25 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("weirdFilterOrder", "0001_initial")]

    operations = [
        migrations.AddIndex(
            model_name="examplemodel",
            index=models.Index(
                fields=["attribute_a", "attribute_b", "attribute_c"], name="testApp_exa_attribu_bbbd02_idx"
            ),
        )
    ]
