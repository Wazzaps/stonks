from django.contrib import admin

# Register your models here.
from stonks.models import SwiftnessProduct, SwiftnessDeposit, SwiftnessInsurance, BankState, BankTransaction


class SwiftnessProductAdmin(admin.ModelAdmin):
    pass


class SwiftnessDepositAdmin(admin.ModelAdmin):
    pass


class SwiftnessInsuranceAdmin(admin.ModelAdmin):
    pass


class BankStateAdmin(admin.ModelAdmin):
    pass


class BankTransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(SwiftnessProduct, SwiftnessProductAdmin)
admin.site.register(SwiftnessDeposit, SwiftnessDepositAdmin)
admin.site.register(SwiftnessInsurance, SwiftnessInsuranceAdmin)
admin.site.register(BankState, BankStateAdmin)
admin.site.register(BankTransaction, BankTransactionAdmin)
