#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nortegestion.settings')
os.environ['DEBUG'] = 'True'
os.environ['USE_POSTGRES'] = 'False'

# Initialize Django
django.setup()

try:
    from django.contrib.auth.models import User
    from core.models import Rubro, Marca

    print("[INFO] Creating user field migration...")

    # Get motocenter user to use as default
    motocenter_user = User.objects.get(email='motocenter@nortegestion.com')
    print(f"[INFO] Using default user: {motocenter_user.email} (ID: {motocenter_user.id})")

    # Create migration file content
    migration_content = f"""# Generated migration for adding user fields to Rubro and Marca
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_user_multitenant'),
    ]

    operations = [
        migrations.AddField(
            model_name='rubro',
            name='user',
            field=models.ForeignKey(default={motocenter_user.id}, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='marca',
            name='user',
            field=models.ForeignKey(default={motocenter_user.id}, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='rubro',
            unique_together={{('user', 'nombre')}},
        ),
        migrations.AlterUniqueTogether(
            name='marca',
            unique_together={{('user', 'nombre')}},
        ),
    ]
"""

    # Write migration file
    migration_dir = 'core/migrations'
    os.makedirs(migration_dir, exist_ok=True)

    migration_file = f'{migration_dir}/0004_add_user_to_rubro_marca.py'
    with open(migration_file, 'w') as f:
        f.write(migration_content)

    print(f"[SUCCESS] Migration file created: {migration_file}")
    print("[INFO] You can now run: python manage.py migrate")

except Exception as e:
    print(f"[ERROR] Error creating migration: {e}")
    import traceback
    traceback.print_exc()