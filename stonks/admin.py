from django.contrib import admin

# Register your models here.
from stonks.models import SwiftnessProduct, SwiftnessDeposit, SwiftnessInsurance


class SwiftnessProductAdmin(admin.ModelAdmin):
    pass


class SwiftnessDepositAdmin(admin.ModelAdmin):
    pass


class SwiftnessInsuranceAdmin(admin.ModelAdmin):
    pass


admin.site.register(SwiftnessProduct, SwiftnessProductAdmin)
admin.site.register(SwiftnessDeposit, SwiftnessDepositAdmin)
admin.site.register(SwiftnessInsurance, SwiftnessInsuranceAdmin)
