# Generated migration for adding user fields to Rubro and Marca
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_user_multitenant'),
    ]

    operations = [
        migrations.AddField(
            model_name='rubro',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='marca',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='rubro',
            unique_together={('user', 'nombre')},
        ),
        migrations.AlterUniqueTogether(
            name='marca',
            unique_together={('user', 'nombre')},
        ),
    ]
