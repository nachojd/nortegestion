#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Set environment variables for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nortegestion.settings')
os.environ['DEBUG'] = 'True'
os.environ['USE_POSTGRES'] = 'False'

# Initialize Django
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

try:
    print("[MIGRATE] Creating migrations for multi-tenant models...")

    # Get the motocenter user ID for default value
    motocenter_user = User.objects.get(username='motocenter@nortegestion.com')
    print(f"[OK] Motocenter user ID: {motocenter_user.id}")

    # Create migration file content manually since we need to provide defaults
    migration_content = f'''# Generated migration for multi-tenant models
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
            field=models.ForeignKey(default={motocenter_user.id}, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(default={motocenter_user.id}, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='user',
            field=models.ForeignKey(default={motocenter_user.id}, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
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
            unique_together={{('user', 'codigo')}},
        ),
        migrations.AlterUniqueTogether(
            name='quote',
            unique_together={{('user', 'numero')}},
        ),
    ]
'''

    # Write migration file
    migration_file = f"D:/Dev/nortegestion/core/migrations/0003_add_user_multitenant.py"
    with open(migration_file, 'w', encoding='utf-8') as f:
        f.write(migration_content)

    print(f"[OK] Migration file created: {migration_file}")

    # Apply the migration
    print("\n[MIGRATE] Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

    print("\n[SUCCESS] MULTI-TENANT MIGRATION COMPLETED!")

except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()