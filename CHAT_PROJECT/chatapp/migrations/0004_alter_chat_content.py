# Generated by Django 4.1.3 on 2022-12-13 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_alter_chat_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='content',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
