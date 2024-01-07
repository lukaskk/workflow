# Generated by Django 4.2.7 on 2024-01-06 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_order_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='tasks',
        ),
        migrations.RemoveField(
            model_name='client',
            name='user',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
        migrations.AddField(
            model_name='customuser',
            name='company',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='job_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Administrator',
        ),
        migrations.DeleteModel(
            name='Client',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]