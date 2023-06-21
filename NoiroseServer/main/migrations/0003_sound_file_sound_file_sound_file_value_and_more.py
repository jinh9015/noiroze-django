# Generated by Django 4.1.7 on 2023-06-21 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_sound_level_verified_sound_file_dong_sound_file_ho_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sound_file",
            name="sound_file",
            field=models.FileField(null=True, upload_to="sound_file/%Y_%m_%d"),
        ),
        migrations.AddField(
            model_name="sound_file",
            name="value",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="sound_level_verified",
            name="file_name",
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name="sound_file",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="sound_level_verified",
            name="created_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="sound_level_verified",
            name="sound_type",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="sound_level_verified",
            name="value",
            field=models.FloatField(null=True),
        ),
    ]
