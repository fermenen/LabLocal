from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ai_api_key',
            field=models.CharField(
                blank=True,
                default='',
                max_length=255,
                verbose_name='API key IA premium',
            ),
        ),
    ]
