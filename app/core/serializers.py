from .models import Account
from rest_framework import serializers


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    # uuid = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Account
        fields = ['uuid', 'fio', 'balance', 'hold', 'status']


class ActionSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    value = serializers.IntegerField()
    action = serializers.ChoiceField({'plus': 'plus', 'minus': 'minus'})

    class Meta:
        model = Account
        fields = ['uuid', 'value']
