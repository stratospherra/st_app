from django.db import models, migrations
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from io import BytesIO
from django.core.files import File
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.conf.urls.static import static





def create_unknown_faculty(apps, schema_editor):
    Faculty = apps.get_model('main', 'Faculty')
    Faculty.objects.create(name='Unknown', is_active=True)

class Migration(migrations.Migration):

    dependencies = [
        # добавьте здесь зависимость вашей предыдущей миграции
        ('main', 'название_вашей_последней_миграции'),
    ]

    operations = [
        migrations.RunPython(create_unknown_faculty),
    ]


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id} {self.last_name} {self.first_name} {self.middle_name}"

    @property
    def formatted_id(self):
        return f"{self.id:06d}"



class Subject(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class StudentStatus(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Notification(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# ---------------

class ApplicationInformation(models.Model):
    title = models.CharField(max_length=2000)
    description = models.TextField()

    def __str__(self):
        return self.title
class ApplicationStatus(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Выполненные'),
        ('incomplete', 'Невыполненные'),
        ('done', 'Исполнено'),
        ('in_progress', 'В процессе'),
    ]
    
    name = models.CharField(max_length=100, choices=STATUS_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_name_display()

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Responsible(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Executor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Application(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Выполненные'),
        ('incomplete', 'Невыполненные'),
        ('done', 'Исполнено'),
        ('in_progress', 'В процессе'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    title = models.CharField(max_length=500)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    responsible = models.ForeignKey(Responsible, on_delete=models.SET_NULL, null=True)
    executor = models.ForeignKey(Executor, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # deadline = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_process')
    pdf_file = models.FileField(upload_to='', null=True, blank=True)

    def __str__(self):
        return f"{self.title} {self.description}"

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

        
        pdf_content = render_to_string('application_pdf_template.html', {'application': self})
        buffer = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(pdf_content.encode("UTF-8")), buffer)

        if pdf.err:
            print("Ошибка при создании PDF")
            return

        
        today_str = timezone.now().strftime('%Y-%m-%d')
        pdf_folder = os.path.join(settings.MEDIA_ROOT, 'applications', str(self.student.id), today_str, str(self.id))
        os.makedirs(pdf_folder, exist_ok=True)

        pdf_filename = f'application_{self.id}.pdf'
        pdf_path = os.path.join(pdf_folder, pdf_filename)

        
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(buffer.getvalue())

        buffer.close()


        self.pdf_file.name = pdf_path
        super().save(update_fields=["pdf_file"])

        

# -------------------------

class TypeOfGrades(models.Model):
    title = models.CharField(max_length=255)
    calculate = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey для связи с User
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    status = models.ForeignKey('StudentStatus', on_delete=models.CASCADE)
    faculties = models.ManyToManyField(Faculty, through='StudentOfFaculty')
    current_faculty = models.ForeignKey(Faculty, related_name='current_students', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name} - {self.current_faculty}, {self.speciality}, {self.status}"

    @property
    def formatted_id(self):
        return f"{self.id:06d}"
    
    def calculate_grades(self):
        grades = TypeOfGrades.objects.filter(student=self)
        grades_dict = {grade.grade_type.title: grade.value for grade in grades}

        P1 = (grades_dict.get('ср.т1', 0) + grades_dict.get('рк1', 0)) / 2
        P2 = (grades_dict.get('ср.т2', 0) + grades_dict.get('рк2', 0)) / 2
        OR = (P1 + P2) / 2
        IO = (OR + grades_dict.get('Экзамен', 0)) / 2

        return {
            'P1': P1,
            'P2': P2,
            'OR': OR,
            'IO': IO,
        }
    

class Grade(models.Model):
    id = models.IntegerField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, default=1)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    grade_type = models.ForeignKey(TypeOfGrades, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.student.last_name} - {self.grade_type.title}: {self.subject}"

    @property
    def is_pass(self):
        return self.value >= 50

    @property
    def max_value(self):
        return 100

    @property
    def min_value(self):
        return 0



class StudentOfFaculty(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Student {self.student} in Faculty {self.faculty}"
    

class StudentOfSpeciality(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Student {self.student} in Speciality {self.speciality}"
    

class StudentOfLanguage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Student {self.student} in Language {self.language}"
    


class DayOfWeek(models.Model):
    # language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name_en = models.CharField(max_length=20)
    # name_ru = models.CharField(max_length=20)
    # name_kz = models.CharField(max_length=20)
    def __str__(self):
        return f"{ self.name_en}"


class ScheduleVersion(models.Model):
    version_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.version_number


class Schedule(models.Model):
    date = models.DateField(default=datetime.date.today)
    day_of_week = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE)
    time_start = models.TimeField()
    time_end = models.TimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.CharField(max_length=20)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    version = models.ForeignKey(ScheduleVersion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.day_of_week} {self.time_start}-{self.time_end} {self.subject} ({self.teacher})"
    #help