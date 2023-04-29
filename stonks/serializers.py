from rest_framework import serializers
from stonks.models import SwiftnessProduct, SwiftnessDeposit, SwiftnessInsurance, BankState, BankTransaction


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


class BankStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankState
        fields = "__all__"


class BankTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransaction
        fields = "__all__"
