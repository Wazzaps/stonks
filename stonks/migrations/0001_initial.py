# Generated by Django 4.1.7 on 2023-03-24 23:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SwiftnessProduct",
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
                ("date_of_validity", models.DateField()),
                ("managing_company", models.TextField(blank=True)),
                ("product_name", models.TextField(blank=True)),
                ("policy_id", models.TextField(blank=True)),
                ("status", models.TextField(blank=True, null=True)),
                ("total_savings", models.FloatField(null=True)),
                ("soonest_withdrawal", models.DateField(null=True)),
                (
                    "expected_savings_at_retirement_not_including_premiums",
                    models.FloatField(null=True),
                ),
                (
                    "monthly_allowance_at_retirement_not_including_premiums",
                    models.FloatField(null=True),
                ),
                ("expected_savings_at_retirement", models.FloatField(null=True)),
                ("monthly_allowance_at_retirement", models.FloatField(null=True)),
                ("estimated_zikna_pension", models.FloatField(null=True)),
                ("mgmt_fee_percent_from_deposits", models.FloatField(null=True)),
                ("yearly_mgmt_fee_percent_from_savings", models.FloatField(null=True)),
                ("profit_this_year", models.FloatField(null=True)),
                ("job_deposits", models.FloatField(null=True)),
                ("personal_deposits", models.FloatField(null=True)),
                ("leftovers_partner", models.FloatField(null=True)),
                ("leftovers_dependent_parent", models.FloatField(null=True)),
                ("leftovers_children", models.FloatField(null=True)),
                ("pension_for_disablement", models.FloatField(null=True)),
                (
                    "monthly_insurance_loss_of_ability_to_work",
                    models.FloatField(null=True),
                ),
                (
                    "onetime_insurance_loss_of_ability_to_work",
                    models.FloatField(null=True),
                ),
                ("initial_join_date", models.DateField(null=True)),
                ("beneficiaries_partner", models.FloatField(null=True)),
                ("beneficiaries_children", models.FloatField(null=True)),
                ("monthly_insurance_death", models.FloatField(null=True)),
                ("onetime_insurance_death", models.FloatField(null=True)),
                ("product_type", models.TextField(blank=True, null=True)),
                ("plan_open_date", models.DateField(null=True)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SwiftnessInsurance",
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
                ("date_of_validity", models.DateField()),
                ("insurance_type", models.TextField(blank=True)),
                ("name_of_policy", models.TextField(blank=True)),
                ("managing_company", models.TextField(blank=True)),
                ("who_gets_the_money", models.TextField(blank=True)),
                ("onetime_payment", models.FloatField(null=True)),
                ("monthly_payment", models.FloatField(null=True)),
                ("policy_id", models.TextField(blank=True, null=True)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SwiftnessDeposit",
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
                ("product_type", models.TextField(blank=True)),
                ("managing_company", models.TextField(blank=True)),
                ("policy_id", models.TextField(blank=True)),
                ("value_date", models.DateField()),
                ("wage_month", models.DateField(null=True)),
                ("job_name", models.TextField(blank=True, null=True)),
                ("personal_deposits", models.FloatField(null=True)),
                ("job_deposits", models.FloatField(null=True)),
                ("job_deposits_for_compensation", models.FloatField(null=True)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="swiftnessproduct",
            constraint=models.UniqueConstraint(
                fields=(
                    "product_name",
                    "managing_company",
                    "policy_id",
                    "date_of_validity",
                    "user_id",
                ),
                name="swiftness_product_primary_key",
            ),
        ),
        migrations.AddConstraint(
            model_name="swiftnessinsurance",
            constraint=models.UniqueConstraint(
                fields=(
                    "insurance_type",
                    "name_of_policy",
                    "managing_company",
                    "policy_id",
                    "who_gets_the_money",
                    "date_of_validity",
                    "user_id",
                ),
                name="swiftness_insurance_primary_key",
            ),
        ),
        migrations.AddConstraint(
            model_name="swiftnessdeposit",
            constraint=models.UniqueConstraint(
                fields=(
                    "product_type",
                    "managing_company",
                    "policy_id",
                    "value_date",
                    "user_id",
                ),
                name="swiftness_deposit_primary_key",
            ),
        ),
    ]
