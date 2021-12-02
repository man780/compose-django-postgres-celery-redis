from django.urls import path, include

from .views import GroupViewSet, StudentViewSet, SubjectViewSet, MarkViewSet, ReportByStudentView, ReportByGroupView
from rest_framework import routers


app_name = 'education'

router = routers.DefaultRouter()
router.register(r'group', GroupViewSet)
router.register(r'student', StudentViewSet)
router.register(r'subject', SubjectViewSet)
router.register(r'mark', MarkViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('report-by-student/', ReportByStudentView.as_view()),
    path('report-by-group/', ReportByGroupView.as_view())
]
