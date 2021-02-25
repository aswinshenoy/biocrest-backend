# Generated by Django 3.1.4 on 2021-02-25 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0003_auto_20210217_1055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventcertificate',
            old_name='nameFontColor',
            new_name='fontColor',
        ),
        migrations.RenameField(
            model_name='eventcertificate',
            old_name='nameFontSize',
            new_name='fontSize',
        ),
        migrations.RenameField(
            model_name='eventcertificate',
            old_name='nameFontURL',
            new_name='fontURL',
        ),
        migrations.RemoveField(
            model_name='eventcertificate',
            name='nameFontName',
        ),
        migrations.AddField(
            model_name='eventcertificate',
            name='affiliationPositionX',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='eventcertificate',
            name='affiliationPositionY',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='eventcertificate',
            name='eventNamePositionX',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='eventcertificate',
            name='eventNamePositionY',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='eventcertificate',
            name='includeAffiliationBody',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eventcertificate',
            name='includeEventName',
            field=models.BooleanField(default=False),
        ),
    ]