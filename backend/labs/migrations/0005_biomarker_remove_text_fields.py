"""
Elimina los campos name, short_name y description del modelo Biomarker.
El texto pasa a vivir en labs/biomarker_i18n.py, indexado por loinc_code.
loinc_code pasa a ser unique y se amplía a max_length=30.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0004_userprofile_smoker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biomarker',
            name='name',
        ),
        migrations.RemoveField(
            model_name='biomarker',
            name='short_name',
        ),
        migrations.RemoveField(
            model_name='biomarker',
            name='description',
        ),
        migrations.AlterField(
            model_name='biomarker',
            name='loinc_code',
            field=models.CharField(
                max_length=30,
                unique=True,
                verbose_name='LOINC code',
            ),
        ),
    ]
