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


class ReportByStudent(APIView):

    def get(self, request):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT " 
                "st.name AS student_name, "
                "gp.name AS group_name, "
                "sb.name AS subject_name, " 
                "avg_mark_table.avg_mark AS average_mark "
                "from "
                "( "
                    "SELECT "
                        "student_id, "
                        "subject_id, "
                        "AVG(ball) AS avg_mark "
                    "FROM education_mark " 
                    "GROUP BY student_id, subject_id " 
                    "ORDER BY subject_id, student_id "
                ") avg_mark_table "
                "LEFT JOIN education_student st ON st.id = avg_mark_table.student_id "
                "LEFT JOIN education_subject sb ON sb.id = avg_mark_table.subject_id "
                "LEFT JOIN education_group gp ON gp.id = st.group_id ORDER BY st.name"
            )
            rows = cursor.fetchall()
        reportTable = {}
        i = 0
        for mark in rows:
            reportTable[i] = mark
            i = i + 1
        return Response({'marks': reportTable}, 200)


class ReportByGroup(APIView):

    def get(self, request):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT "
                  "group_name, "
                  "subject_name, "
                  "AVG(avg_mark_group_table.average_mark) "
                "FROM ( "
                  "SELECT  "
                  "st.group_id, "
                  "gp.name AS group_name, "
                  "sb.id AS subject_id, "
                  "sb.name AS subject_name, "
                  "avg_mark_table.avg_mark AS average_mark "
                  "FROM "
                  "(  "
                    "SELECT "
                      "student_id, "
                      "subject_id, "
                      "AVG(ball) AS avg_mark "
                    "FROM education_mark "
                    "GROUP BY student_id, subject_id "
                    "ORDER BY subject_id, student_id "
                  ") avg_mark_table "
                  "LEFT JOIN education_student st ON st.id = avg_mark_table.student_id "
                  "LEFT JOIN education_subject sb ON sb.id = avg_mark_table.subject_id "
                  "LEFT JOIN education_group gp ON gp.id = st.group_id "
                ") AS avg_mark_group_table "
                "GROUP BY group_name, subject_name "
                "ORDER BY group_name, subject_name"
            )
            rows = cursor.fetchall()
        reportTable = {}
        i = 0
        for mark in rows:
            reportTable[i] = mark
            i = i + 1
        return Response({'Report': reportTable}, 200)
