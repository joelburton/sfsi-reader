# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='visible',
            field=models.BooleanField(default=False, help_text=b'Check to make your profile visible to your fellow students. Regardless, your email remains private to training staff.'),
            preserve_default=True,
        ),
    ]
