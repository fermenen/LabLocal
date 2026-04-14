from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0003_ailicense_remove_userprofile_ai_api_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='smoker',
            field=models.BooleanField(blank=True, null=True, verbose_name='Fumador'),
        ),
    ]
