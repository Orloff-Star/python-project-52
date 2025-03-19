# Generated by Django 5.1.6 on 2025-03-04 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0002_alter_label_name'),
        ('tasks', '0002_task_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True,
                                         related_name='tasks',
                                         to='labels.label'
                                         ),
        ),
    ]
