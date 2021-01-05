# Generated by Django 3.1.4 on 2021-01-05 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210104_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, default='IN', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Admin'), (1, 'Student'), (2, 'Academician'), (3, 'Industry')], null=True),
        ),
    ]
