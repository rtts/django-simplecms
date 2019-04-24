from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='title',
            field=models.CharField(blank=True, max_length=255, verbose_name='title'),
        ),
    ]
