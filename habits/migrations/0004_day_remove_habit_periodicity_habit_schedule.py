# Generated by Django 5.0.2 on 2024-03-11 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_alter_habit_reward'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.RemoveField(
            model_name='habit',
            name='periodicity',
        ),
        migrations.AddField(
            model_name='habit',
            name='schedule',
            field=models.ManyToManyField(blank=True, related_name='habits', to='habits.day'),
        ),
    ]