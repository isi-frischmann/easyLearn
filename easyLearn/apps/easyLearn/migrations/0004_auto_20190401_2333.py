# Generated by Django 2.1.7 on 2019-04-01 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('easyLearn', '0003_auto_20190401_2333'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('completion', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StatusSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('completion', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StatusTraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('completion', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(default='no Name yet', max_length=60),
        ),
        migrations.AlterField(
            model_name='activityprogress',
            name='status',
            field=models.CharField(default='not started', max_length=12),
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(default='no Name yet', max_length=60),
        ),
        migrations.AlterField(
            model_name='sectionprogress',
            name='status',
            field=models.CharField(default='not started', max_length=12),
        ),
        migrations.AlterField(
            model_name='training',
            name='name',
            field=models.CharField(default='no Name yet', max_length=60),
        ),
        migrations.AlterField(
            model_name='trainingprogress',
            name='status',
            field=models.CharField(default='not started', max_length=12),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='user',
            name='fname',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='user',
            name='lname',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255),
        ),
        migrations.AddField(
            model_name='statustraining',
            name='training',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modernHealth.Training'),
        ),
        migrations.AddField(
            model_name='statussection',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modernHealth.Section'),
        ),
        migrations.AddField(
            model_name='statusactivity',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modernHealth.Activity'),
        ),
    ]