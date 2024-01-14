from faker import Faker
fake = Faker()
import random
from .models import *
from django.db.models import Sum

def create_subject_marks(n):
    try:
        student_objs = Student.objects.all()
        for student in student_objs:
            subjects = Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject=subject,
                    student = student,
                    marks = random.randint(1,100)
                )
    
    except Exception as e:
        print(e)

def generate_report_card():
    current_rank = -1
    ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks','-student_age')
    i = 1
    for rank in ranks:
        ReportCard.objects.create(
            student = rank,
            student_rank = i
        )
        i = i+1