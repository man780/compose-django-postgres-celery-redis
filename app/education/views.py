from .models import (
    Group,
    Student,
    Subject,
    Mark,
    ReportByGroup,
    ReportByStudent
)
from .serializers import (
    GroupSerializer,
    StudentSerializer,
    SubjectSerializer,
    MarkSerializer,
    ReportByGroupSerializer,
    ReportByStudentSerializer
)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

import json


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


class ReportByStudentView(APIView):

    def get(self, request):
        rows = ReportByStudent.objects.raw(
            "SELECT "
                "1 as id, "
                "st.name AS fio, "
                "gp.name AS group, "
                "sb.name AS subject, "
                "avg_mark_table.avg_mark AS ball "
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
        sRows = ReportByStudentSerializer(rows, many=True)
        stRows = JSONRenderer().render(sRows.data)
        data = json.loads(stRows)

        return Response(data, 200)


class ReportByGroupView(APIView):

    def get(self, request):
        rows = ReportByGroup.objects.raw(
            "SELECT "
              "1 as id, "
              "group_name, "
              "subject_name, "
              "AVG(avg_mark_group_table.average_mark) as ball "
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
        print(rows)
        sRows = ReportByGroupSerializer(rows, many=True)
        stRows = JSONRenderer().render(sRows.data)
        data = json.loads(stRows)

        return Response(data, 200)
