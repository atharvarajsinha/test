from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CompilationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_code', models.TextField()),
                ('source_language', models.CharField(max_length=16)),
                ('target_language', models.CharField(max_length=16)),
                ('tokens_file_path', models.CharField(max_length=512)),
                ('ast_file_path', models.CharField(max_length=512)),
                ('ir_file_path', models.CharField(max_length=512)),
                ('converted_code', models.TextField()),
                ('original_output', models.TextField(blank=True)),
                ('converted_output', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
