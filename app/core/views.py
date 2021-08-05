from django.shortcuts import render
from .models import Account
from .serializers import AccountSerializer, ActionSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from .tasks import clear_hold


def task():
    clear_hold.delay()


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ChangeBalance(APIView):
    serializer_class = ActionSerializer

    def put(self, request):
        try:
            data = ActionSerializer(data=request.data)
            if data.is_valid():
                account = Account.objects.get(pk=data.data['uuid'])
                if data.data['action'] == 'plus':
                    account.add_balance(value=data.data['value'])
                    return Response('Balance added', 201)
                else:
                    account.dedicate_balance(value=data.data['value'])
                    return Response('Balance Substract', 202)
            else:
                return Response(False, status=ValueError)
        except Account.DoesNotExist:
            raise Http404


class AccountList(APIView):
    """
    List all accounts, or create a new account.
    """
    def get(self, request, format=None):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(APIView):
    """
    Retrieve, update or delete a account instance.
    """
    def get_object(self, uuid):
        try:
            return Account.objects.get(pk=uuid)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        account = self.get_object(uuid)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        account = self.get_object(pk)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        account = self.get_object(pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def load_data(request):
    Account.objects.create(
        uuid='26c940a1-7228-4ea2-a3bc-e6460b172040',
        fio='Петров Иван Сергеевич',
        balance=1700,
        hold=300,
        status=True
    )
    Account.objects.create(
        uuid='7badc8f8-65bc-449a-8cde-855234ac63e1',
        fio=' Kazitsky Jason',
        balance=200,
        hold=200,
        status=True
    )
    Account.objects.create(
        uuid='5597cc3d-c948-48a0-b711-393edf20d9c0',
        fio='Пархоменко Антон Александрович',
        balance=10,
        hold=300,
        status=True
    )
    Account.objects.create(
        uuid='867f0924-a917-4711-939b-90b179a96392',
        fio='Петечкин Петр Измаилович',
        balance=1000000,
        hold=1,
        status=False
    )

    return None