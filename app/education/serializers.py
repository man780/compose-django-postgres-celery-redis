from .models import (Group, Student, Subject, Mark)
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        # url: {'view_name': 'api:user-detail'}

        # Added this line:
        # groups: {'view_name': 'education:group-detail'}
        model = Student
        # lookup_field = 'id'
        fields = ['id', 'group', 'name']


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['id', 'student', 'subject', 'ball']
