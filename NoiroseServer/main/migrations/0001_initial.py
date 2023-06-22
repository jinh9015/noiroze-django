# Generated by Django 4.1.7 on 2023-06-22 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Sound_File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dong",
                    models.CharField(
                        choices=[
                            ("101", "101동"),
                            ("102", "102동"),
                            ("103", "103동"),
                            ("104", "104동"),
                            ("105", "105동"),
                        ],
                        default="101",
                        max_length=10,
                    ),
                ),
                (
                    "ho",
                    models.CharField(
                        choices=[
                            ("101", "101호"),
                            ("102", "102호"),
                            ("201", "201호"),
                            ("202", "202호"),
                            ("301", "301호"),
                            ("302", "302호"),
                            ("401", "401호"),
                            ("402", "402호"),
                            ("501", "501호"),
                            ("502", "502호"),
                            ("601", "601호"),
                            ("602", "602호"),
                            ("701", "701호"),
                            ("702", "702호"),
                            ("801", "801호"),
                            ("802", "802호"),
                            ("901", "901호"),
                            ("902", "902호"),
                            ("1001", "1001호"),
                            ("1002", "1002호"),
                        ],
                        default="101",
                        max_length=5,
                    ),
                ),
                (
                    "place",
                    models.CharField(
                        choices=[
                            ("거실", "거실"),
                            ("안방", "안방"),
                            ("주방", "주방"),
                            ("방1", "방1"),
                            ("방2", "방2"),
                        ],
                        default="거실",
                        max_length=10,
                    ),
                ),
                ("value", models.FloatField(null=True)),
                ("file_name", models.CharField(max_length=40)),
                (
                    "sound_file",
                    models.FileField(null=True, upload_to="sound_file/%Y_%m_%d"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Sound_Level",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dong",
                    models.CharField(
                        choices=[
                            ("101", "101동"),
                            ("102", "102동"),
                            ("103", "103동"),
                            ("104", "104동"),
                            ("105", "105동"),
                        ],
                        default="101",
                        max_length=10,
                    ),
                ),
                (
                    "ho",
                    models.CharField(
                        choices=[
                            ("101", "101호"),
                            ("102", "102호"),
                            ("201", "201호"),
                            ("202", "202호"),
                            ("301", "301호"),
                            ("302", "302호"),
                            ("401", "401호"),
                            ("402", "402호"),
                            ("501", "501호"),
                            ("502", "502호"),
                            ("601", "601호"),
                            ("602", "602호"),
                            ("701", "701호"),
                            ("702", "702호"),
                            ("801", "801호"),
                            ("802", "802호"),
                            ("901", "901호"),
                            ("902", "902호"),
                            ("1001", "1001호"),
                            ("1002", "1002호"),
                        ],
                        default="101",
                        max_length=5,
                    ),
                ),
                (
                    "place",
                    models.CharField(
                        choices=[
                            ("거실", "거실"),
                            ("안방", "안방"),
                            ("주방", "주방"),
                            ("방1", "방1"),
                            ("방2", "방2"),
                        ],
                        default="거실",
                        max_length=10,
                    ),
                ),
                ("value", models.FloatField()),
                ("created_at", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Sound_Level_Verified",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dong",
                    models.CharField(
                        choices=[
                            ("101", "101동"),
                            ("102", "102동"),
                            ("103", "103동"),
                            ("104", "104동"),
                            ("105", "105동"),
                        ],
                        default="101",
                        max_length=10,
                    ),
                ),
                (
                    "ho",
                    models.CharField(
                        choices=[
                            ("101", "101호"),
                            ("102", "102호"),
                            ("201", "201호"),
                            ("202", "202호"),
                            ("301", "301호"),
                            ("302", "302호"),
                            ("401", "401호"),
                            ("402", "402호"),
                            ("501", "501호"),
                            ("502", "502호"),
                            ("601", "601호"),
                            ("602", "602호"),
                            ("701", "701호"),
                            ("702", "702호"),
                            ("801", "801호"),
                            ("802", "802호"),
                            ("901", "901호"),
                            ("902", "902호"),
                            ("1001", "1001호"),
                            ("1002", "1002호"),
                        ],
                        default="101",
                        max_length=5,
                    ),
                ),
                (
                    "place",
                    models.CharField(
                        choices=[
                            ("거실", "거실"),
                            ("안방", "안방"),
                            ("주방", "주방"),
                            ("방1", "방1"),
                            ("방2", "방2"),
                        ],
                        default="거실",
                        max_length=10,
                    ),
                ),
                ("value", models.FloatField(null=True)),
                ("created_at", models.DateTimeField(null=True)),
                ("sound_type", models.CharField(max_length=100, null=True)),
                ("file_name", models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ComplainBoard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CommunityBoard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("정보공유", "정보공유"),
                            ("소통해요", "소통해요"),
                            ("붙어봐요", "붙어봐요"),
                            ("칭찬해요", "칭찬해요"),
                            ("나눔해요", "나눔해요"),
                        ],
                        default="정보공유",
                        max_length=10,
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
