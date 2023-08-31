from .models import Account
from .serializers import AccountSerializer, ActionSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.response import Response


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @action(detail=True)
    def status(self, request, *args, **kwargs):
        account = self.get_object()
        return Response({'balance': account.balance, 'status': account.status})


class ChangeBalance(APIView):
    serializer_class = ActionSerializer

    def put(self, request):
        try:
            data = ActionSerializer(data=request.data)
            if data.is_valid():
                account = Account.objects.get(pk=data.data['uuid'])
                if data.data['action'] == 'plus':
                    account.increase_balance(value=data.data['value'])
                    return Response('Balance added', 201)
                else:
                    account.decrease_balance(value=data.data['value'])
                    return Response('Balance Substract', 202)
            else:
                return Response(False, status=ValueError)
        except Account.DoesNotExist:
            raise Http404
