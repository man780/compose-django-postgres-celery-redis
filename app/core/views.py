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
