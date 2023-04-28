from django.db import IntegrityError
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import BaseParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets, permissions
from stonks.models import SwiftnessProduct, SwiftnessDeposit, SwiftnessInsurance
from stonks.serializers import SwiftnessProductSerializer, SwiftnessDepositSerializer, SwiftnessInsuranceSerializer
from stonks.swiftness_parsing.extractor import extract_swiftness_zip


class BinaryParser(BaseParser):
    """Parser for raw binary data."""

    media_type = "application/octet-stream"

    def parse(self, stream, media_type=None, parser_context=None):
        """Returns the incoming bytestream as-is."""
        return stream.read()


class SwiftnessProductList(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = SwiftnessProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SwiftnessProduct.objects.filter(user_id=self.request.user).order_by(
            "date_of_validity", "managing_company", "product_name", "policy_id"
        )


class SwiftnessDepositList(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = SwiftnessDepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SwiftnessDeposit.objects.filter(user_id=self.request.user).order_by(
            "value_date", "managing_company", "product_type", "policy_id"
        )


class SwiftnessInsuranceList(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = SwiftnessInsuranceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SwiftnessInsurance.objects.filter(user_id=self.request.user).order_by(
            "date_of_validity",
            "managing_company",
            "insurance_type",
            "name_of_policy",
            "who_gets_the_money",
            "policy_id",
        )


class ParseSwiftnessZip(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [BinaryParser]

    # noinspection PyMethodMayBeStatic
    def put(self, request):
        zip_data = request.read()
        zip_pass = request.query_params.get("zip_pass", None).encode("utf-8")
        normalized = extract_swiftness_zip(zip_data, zip_pass)

        for category, serializer_type in zip(
            ["products", "deposits", "insurances"],
            [SwiftnessProductSerializer, SwiftnessDepositSerializer, SwiftnessInsuranceSerializer],
        ):
            for item in normalized[category]:
                item["user_id"] = request.user.id
                serializer = serializer_type(data=item)
                if serializer.is_valid():
                    try:
                        serializer.save()
                    except IntegrityError:
                        # Entry already exists, ignore
                        pass
                else:
                    return Response(serializer.errors, status=400)

        return Response({"status": "ok"}, status=201)
