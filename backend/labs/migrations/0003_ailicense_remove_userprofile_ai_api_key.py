from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0002_userprofile_ai_api_key'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='ai_api_key',
        ),
        migrations.CreateModel(
            name='AILicense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=255, verbose_name='API key IA')),
                ('plan', models.CharField(default='premium', max_length=50, verbose_name='Plan')),
                ('activated_at', models.DateTimeField(auto_now_add=True, verbose_name='Activada el')),
                ('activated_by', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='ai_licenses',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Activada por',
                )),
            ],
            options={
                'verbose_name': 'Licencia IA',
                'verbose_name_plural': 'Licencias IA',
            },
        ),
    ]
