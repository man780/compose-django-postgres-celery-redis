from .models import (Group, Student, Subject, Mark, ReportByStudent, ReportByGroup)
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'group', 'name']


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['id', 'student', 'subject', 'ball']


class ReportByStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportByStudent
        fields = ['fio', 'group', 'subject', 'ball']


class ReportByGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportByGroup
        fields = ['group_name', 'subject_name', 'ball']
