# Generated by Django 4.0.6 on 2022-07-13 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProtectedBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('strapline', models.TextField(blank=True, max_length=500)),
                ('is_encrypted', models.BooleanField()),
                ('private_key', models.TextField(blank=True, max_length=200)),
                ('blog_content', models.TextField()),
                ('author', models.CharField(max_length=100)),
            ],
        ),
    ]
