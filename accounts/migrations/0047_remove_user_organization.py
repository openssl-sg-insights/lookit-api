# Generated by Django 3.0.5 on 2020-06-08 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("accounts", "0046_catch-up-migrations-to-current")]

    operations = [migrations.RemoveField(model_name="user", name="organization")]
