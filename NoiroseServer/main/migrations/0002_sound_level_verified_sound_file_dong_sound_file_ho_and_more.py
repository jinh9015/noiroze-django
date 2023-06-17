# Generated by Django 4.1.7 on 2023-06-17 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
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
                            ("A", "A동"),
                            ("B", "B동"),
                            ("C", "C동"),
                            ("D", "D동"),
                            ("E", "E동"),
                        ],
                        default="A",
                        max_length=10,
                    ),
                ),
                ("ho", models.CharField(default=0, max_length=4)),
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
                ("sound_type", models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name="sound_file",
            name="dong",
            field=models.CharField(
                choices=[
                    ("A", "A동"),
                    ("B", "B동"),
                    ("C", "C동"),
                    ("D", "D동"),
                    ("E", "E동"),
                ],
                default="A",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="sound_file",
            name="ho",
            field=models.CharField(default=0, max_length=4),
        ),
        migrations.AddField(
            model_name="sound_level",
            name="dong",
            field=models.CharField(
                choices=[
                    ("A", "A동"),
                    ("B", "B동"),
                    ("C", "C동"),
                    ("D", "D동"),
                    ("E", "E동"),
                ],
                default="A",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="sound_level",
            name="ho",
            field=models.CharField(default=0, max_length=4),
        ),
        migrations.AlterField(
            model_name="sound_file",
            name="place",
            field=models.CharField(
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
        migrations.AlterField(
            model_name="sound_level",
            name="place",
            field=models.CharField(
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
    ]