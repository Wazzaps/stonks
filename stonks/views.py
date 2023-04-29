import datetime
import json
from pytz import timezone
from django.db import IntegrityError
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import BaseParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets, permissions
from stonks.models import SwiftnessProduct, SwiftnessDeposit, SwiftnessInsurance, BankState, BankTransaction
from stonks.serializers import (
    SwiftnessProductSerializer,
    SwiftnessDepositSerializer,
    SwiftnessInsuranceSerializer,
    BankStateSerializer,
    BankTransactionSerializer,
)
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


class BankStateList(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = BankStateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BankState.objects.filter(user_id=self.request.user).order_by(
            "date",
            "account_num",
        )


class BankTransactionList(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = BankTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BankTransaction.objects.filter(user_id=self.request.user).order_by(
            "date",
            "account_num",
            "txn_id",
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


class ParseBankDumperJson(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [BinaryParser]

    # noinspection PyMethodMayBeStatic
    def put(self, request):
        dump = json.loads(request.read())
        assert dump["success"] is True, "israeli-bank-scrapers failed"

        israel_tz = timezone("Asia/Jerusalem")
        query_time = israel_tz.fromutc(datetime.datetime.fromisoformat(dump["queryTime"].rstrip("Z")))

        for account in dump["accounts"]:
            account_num = account["accountNumber"]
            balance = account["balance"]
            account_state = BankState(
                user_id=request.user,
                account_num=account_num,
                time=query_time,
                balance=balance,
            )
            try:
                account_state.save()
            except IntegrityError:
                # Entry already exists, ignore
                pass

            for transaction in account["txns"]:
                if transaction["type"] != "normal":
                    print(f"Skipping transaction of type '{transaction['type']}'")
                    continue
                if transaction["status"] != "completed":
                    print(f"Skipping transaction of status '{transaction['status']}'")
                    continue
                if transaction["chargedAmount"] != transaction["originalAmount"]:
                    print(
                        f"#{transaction['identifier']}: The charged amount ({transaction['chargedAmount']}) "
                        f"is different from the original amount ({transaction['originalAmount']})"
                    )
                    continue
                if transaction["originalCurrency"] != "ILS":
                    print(f"#{transaction['identifier']}: The original currency is {transaction['originalCurrency']}")
                    continue

                txn = BankTransaction(
                    user_id=request.user,
                    account_num=account_num,
                    txn_id=transaction["identifier"],
                    time=round_date(datetime.datetime.fromisoformat(transaction["date"].rstrip("Z"))).astimezone(
                        israel_tz
                    ),
                    amount=transaction["chargedAmount"],
                    description=transaction["description"],
                )
                try:
                    txn.save()
                except IntegrityError:
                    # Entry already exists, ignore
                    pass

        return Response({"status": "ok"}, status=201)


def round_date(date) -> datetime.datetime:
    return (date + datetime.timedelta(hours=12)).replace(hour=0, minute=0, second=0, microsecond=0)
