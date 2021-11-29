from .models import (
    Group,
    Student,
    Subject,
    Mark
)
from .serializers import (
    GroupSerializer,
    StudentSerializer,
    SubjectSerializer,
    MarkSerializer
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import Http404


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows student to be viewed or edited.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subjects to be viewed or edited.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class MarkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mark to be viewed or edited.
    """
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
