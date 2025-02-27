# Generated by Django 5.0.7 on 2024-08-20 20:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_assetgroup_sort'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otherasset',
            name='ghost',
        ),
        migrations.AlterField(
            model_name='security',
            name='account_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_accounts', to='portfolio.account'),
        ),
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('target_weighting', models.DecimalField(blank=True, decimal_places=4, max_digits=4, null=True)),
                ('color', models.CharField(blank=True, max_length=7, null=True)),
                ('sort', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('source', models.CharField(choices=[('MANUAL', 'Manual'), ('SNAPTRADE', 'SnapTrade'), ('PLAID', 'Plaid')], default='MANUAL', max_length=20)),
                ('ghost', models.BooleanField(default=False)),
                ('symbol', models.CharField(max_length=10)),
                ('shares_quantity', models.DecimalField(blank=True, decimal_places=6, max_digits=15, null=True)),
                ('equity', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('account_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_accounts', to='portfolio.account')),
                ('parent_group_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_assets', to='portfolio.assetgroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Crypto',
                'verbose_name_plural': 'Cryptos',
                'indexes': [models.Index(fields=['symbol'], name='portfolio_c_symbol_c8e660_idx')],
            },
        ),
    ]
