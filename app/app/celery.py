import os
from celery import Celery
import random
from celery.utils.log import get_task_logger


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# from core.models import Account

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls every 10 sec.
    sender.add_periodic_task(1000.0, clear_holds, name='every 10')
    # sender.add_periodic_task(1.0, add_subject.s(), name='add every 10')
    # sender.add_periodic_task(5.0, add_group.s(), name='add every 10')
    # sender.add_periodic_task(1000.0, add_student.s())

    # You can put 1 instead of 100
    # This will randomly add one "ball" per second.
    sender.add_periodic_task(100.0, add_mark.s(), name='add mark every 1')


logger = get_task_logger(__name__)


@app.task
def clear_holds():
    from core.models import Account
    accounts = Account.objects.all()
    isAllCleared = True
    for account in accounts:
        if account.hold == 0:
            continue
        result = account.balance - account.hold
        if result>=0:
            account.balance = result
            account.hold = 0
            account.save()
            logger.info("Account hold cleared. - " + account.fio)
        else:
            isAllCleared = False
            logger.warning("Account hold not cleared - " + account.fio)
    if isAllCleared:
        logger.info("+++All account holds cleared.+++")
    else:
        logger.info("---Not all account holds cleared.---")
    return 1


@app.task
def add_group():
    from education.models import Group
    groupCount = Group.objects.count()
    groupName = str(groupCount+1) + "-Group"
    group = Group(name=groupName)
    group.save()

    logger.info("Created group name is: " + str(group))

    return 1


@app.task
def add_subject():
    from education.models import Subject
    subjectCount = Subject.objects.count()
    subjectName = str(subjectCount+1) + "-Subject"
    subject = Subject(name=subjectName)
    subject.save()

    logger.info("Created subject name is: " + str(subject))

    return 1


@app.task
def add_student():
    from education.models import Student
    from education.models import Group
    groupCount = Group.objects.count()
    count = Student.objects.count()

    group_id = random.randint(1, groupCount)
    studentName = str(count + 1) + "-Student-"+str(group_id)
    student = Student(name=studentName, group_id=group_id)
    student.save()

    logger.info("Created Student name is: " + str(student))

    return 1


@app.task
def add_mark():
    from education.models import Mark
    from education.models import Student
    from education.models import Subject
    subjectCount = Subject.objects.count()
    studentCount = Student.objects.count()
    subject_id = random.randint(1, subjectCount)
    student_id = random.randint(1, studentCount)
    ball = random.randint(56, 100)
    mark = Mark(student_id=student_id, subject_id=subject_id, ball=ball)
    mark.save()

    logger.info("Created Student mark: " + str(mark))

    return 1


app.autodiscover_tasks()
