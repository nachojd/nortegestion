# Generated migration for multi-tenant models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0002_remove_quoteitem_servicio_delete_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='codigo',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='quote',
            name='numero',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('user', 'codigo')},
        ),
        migrations.AlterUniqueTogether(
            name='quote',
            unique_together={('user', 'numero')},
        ),
    ]
