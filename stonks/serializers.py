from rest_framework import serializers
from stonks.models import SwiftnessProduct, SwiftnessDeposit, SwiftnessInsurance


class SwiftnessProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwiftnessProduct
        fields = "__all__"


class SwiftnessDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwiftnessDeposit
        fields = "__all__"


class SwiftnessInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwiftnessInsurance
        fields = "__all__"
