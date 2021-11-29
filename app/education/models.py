from django.db import models
from django.urls import reverse


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Group'

    def get_absolute_url(self):
        return reverse('group', args=[self.name, str(self.id)])


class Student(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='student_group')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Student'

    def get_absolute_url(self):
        return reverse('student', args=[self.name, str(self.id)])


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Subject'

    def get_absolute_url(self):
        return reverse('subject', args=[self.name, str(self.id)])


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='mark_student')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='mark_subject')
    ball = models.PositiveIntegerField()

    def __str__(self):
        return self.student.name+' '+self.ball

    class Meta:
        verbose_name = 'Mark'

    def get_absolute_url(self):
        return reverse('mark', args=[self.name, str(self.id)])
