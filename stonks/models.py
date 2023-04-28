import dataclasses
import datetime
from typing import Any, Optional

from django.db import models


# -- Base class and mixins for value parsers --


@dataclasses.dataclass
class BaseValueParser:
    heb_field_name: str

    def field(self, django_field: Optional[models.Field], nullable=False) -> models.Field:
        django_field.swiftness_value_parser = self
        return django_field

    @classmethod
    def parse(cls, value: str) -> Any:
        raise NotImplementedError()

    @classmethod
    def pretty_display(cls, value: Any) -> str:
        raise NotImplementedError()


class OptionalMixin(BaseValueParser):
    def field(self, django_field: Optional[models.Field] = None, nullable=False) -> models.Field:
        return super().field(django_field, nullable=True)

    @classmethod
    def parse(cls, value: str) -> Optional[float]:
        if value == "":
            return None
        return super().parse(value)

    @classmethod
    def pretty_display(cls, value: Optional[float]) -> str:
        if value is None:
            return "N/A"
        return super().pretty_display(value)


# -- Value parsers --


class String(BaseValueParser):
    def field(self, django_field: Optional[models.Field] = None, nullable=False) -> models.Field:
        if django_field is None:
            django_field = models.TextField(null=nullable, blank=True)
        return super().field(django_field, nullable=nullable)

    @classmethod
    def parse(cls, value: str) -> Optional[str]:
        return value

    @classmethod
    def pretty_display(cls, value: Optional[str]) -> str:
        return value


class Float(BaseValueParser):
    def field(self, django_field: Optional[models.Field] = None, nullable=False) -> models.Field:
        if django_field is None:
            django_field = models.FloatField(null=nullable)
        return super().field(django_field, nullable=nullable)

    @classmethod
    def parse(cls, value: str) -> Optional[float]:
        return float(value)

    @classmethod
    def pretty_display(cls, value: Optional[float]) -> str:
        return f"{value:.2f}"


class Percent(BaseValueParser):
    def field(self, django_field: Optional[models.Field] = None, nullable=False) -> models.Field:
        if django_field is None:
            django_field = models.FloatField(null=nullable)
        return super().field(django_field, nullable=nullable)

    @classmethod
    def parse(cls, value: str) -> Optional[float]:
        return float(value)

    @classmethod
    def pretty_display(cls, value: Optional[float]) -> str:
        return f"{value:.2f}%"


class IsraeliDate(BaseValueParser):
    def field(self, django_field: Optional[models.Field] = None, nullable=False) -> models.Field:
        if django_field is None:
            django_field = models.DateField(null=nullable)
        return super().field(django_field, nullable=nullable)

    @classmethod
    def parse(cls, value: str) -> Optional[datetime.date]:
        return datetime.datetime.strptime(value, "%d/%m/%Y").date()

    @classmethod
    def pretty_display(cls, value: Optional[datetime.date]) -> str:
        return value.strftime("%d/%m/%Y")


class OptString(OptionalMixin, String):
    pass


class OptFloat(OptionalMixin, Float):
    pass


class OptPercent(OptionalMixin, Percent):
    pass


class OptIsraeliDate(OptionalMixin, IsraeliDate):
    pass


# Create your models here.
class SwiftnessProduct(models.Model):
    user_id = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    date_of_validity = IsraeliDate("תאריך נכונות נתונים").field()
    managing_company = String("שם חברה מנהלת").field()
    product_name = String("שם מוצר").field()
    policy_id = String("מספר פוליסה").field()
    status = OptString("סטטוס").field()
    total_savings = OptFloat("סך הכל חיסכון").field()
    soonest_withdrawal = OptIsraeliDate("תחנת משיכה קרובה").field()
    expected_savings_at_retirement_not_including_premiums = OptFloat("חיסכון צפוי לגיל פרישה לא כולל פרמיות").field()
    monthly_allowance_at_retirement_not_including_premiums = OptFloat("קיצבה חודשית לגיל פרישה לא כולל פרמיות").field()
    expected_savings_at_retirement = OptFloat("חיסכון צפוי לגיל פרישה").field()
    monthly_allowance_at_retirement = OptFloat("קיצבה חודשית לגיל פרישה").field()
    estimated_zikna_pension = OptFloat("שיעור פנסיה זקנה צפויה").field()
    mgmt_fee_percent_from_deposits = OptPercent("שיעור דמי ניהול מהפקדות").field()
    yearly_mgmt_fee_percent_from_savings = OptPercent("שיעור דמי ניהול שנתי מחיסכון צבור").field()
    profit_this_year = OptPercent("תשואה מתחילת השנה").field()
    job_deposits = OptFloat("הפקדות מעסיק").field()
    personal_deposits = OptFloat("הפקדות חוסך").field()
    leftovers_partner = OptFloat("שארים - בן/בת זוג").field()
    leftovers_dependent_parent = OptFloat("שארים - הורה נתמך").field()
    leftovers_children = OptFloat("שארים - ילדים").field()
    pension_for_disablement = OptFloat("פנסיית נכות").field()
    monthly_insurance_loss_of_ability_to_work = OptFloat("סכום ביטוח אובדן כושר עבודה - חודשי").field()
    onetime_insurance_loss_of_ability_to_work = OptFloat("סכום ביטוח אובדן כושר עבודה - חד פעמי").field()
    initial_join_date = OptIsraeliDate("תאריך הצטרפות לראשונה").field()
    beneficiaries_partner = OptFloat("מוטבים - בן/בת זוג").field()
    beneficiaries_children = OptFloat("מוטבים - ילדים").field()
    monthly_insurance_death = OptFloat("סכום ביטוח למקרה מוות - חודשי").field()
    onetime_insurance_death = OptFloat("סכום ביטוח למקרה מוות – חד פעמי").field()
    product_type = OptString("סוג מוצר").field()
    plan_open_date = OptIsraeliDate("תאריך פתיחת תוכנית").field()

    def __str__(self):
        return f"U=({self.user_id}) ({self.product_name}) @ ({self.managing_company}) #({self.policy_id}) @ {self.date_of_validity}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product_name", "managing_company", "policy_id", "date_of_validity", "user_id"],
                name="swiftness_product_primary_key",
            )
        ]


class SwiftnessDeposit(models.Model):
    user_id = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    product_type = String("סוג מוצר").field()
    managing_company = String("שם חברה מנהלת").field()
    policy_id = String("מספר פוליסה").field()
    value_date = IsraeliDate("תאריך ערך").field()
    wage_month = OptIsraeliDate("חודש שכר").field()
    job_name = OptString("שם מעסיק").field()
    personal_deposits = OptFloat("הפקדות עובד").field()
    job_deposits = OptFloat("הפקדות מעסיק").field()
    job_deposits_for_compensation = OptFloat("הפקדות מעסיק לפיצויים").field()

    def __str__(self):
        return f"U=({self.user_id}) {self.personal_deposits}+{self.job_deposits}+{self.job_deposits_for_compensation} -> ({self.product_type}) @ ({self.managing_company}) #({self.policy_id}) @ VAL{self.value_date} @ WAGE{self.wage_month}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product_type", "managing_company", "policy_id", "value_date", "wage_month", "user_id"],
                name="swiftness_deposit_primary_key",
            )
        ]


class SwiftnessInsurance(models.Model):
    user_id = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    date_of_validity = models.DateField()
    insurance_type = String("סוג הכיסוי הביטוחי").field()
    name_of_policy = String("שם התוכנית").field()
    managing_company = String("שם חברה מנהלת/מבטחת").field()
    who_gets_the_money = String("מקבל התשלום").field()
    onetime_payment = OptFloat("סכום חד פעמי").field()
    monthly_payment = OptFloat("קצבה חודשית").field()
    policy_id = OptString("מס' פוליסה/חשבון").field()

    def __str__(self):
        return f"U=({self.user_id}) ({self.insurance_type} : {self.name_of_policy} : {self.who_gets_the_money}) @ ({self.managing_company}) @ {self.date_of_validity}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "insurance_type",
                    "name_of_policy",
                    "managing_company",
                    "policy_id",
                    "who_gets_the_money",
                    "date_of_validity",
                    "user_id",
                ],
                name="swiftness_insurance_primary_key",
            )
        ]
