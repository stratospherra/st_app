from django.shortcuts import render, redirect
from main.models import DayOfWeek, Language
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from .forms import StudentRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.db.models import Count
from .models import (Student, Faculty, StudentOfFaculty, Speciality, Teacher, Subject, 
                     Language, StudentStatus, News, Notification, Application, 
                     ApplicationStatus, StudentOfLanguage, StudentOfSpeciality, 
                     TypeOfGrades, Grade, DayOfWeek, ScheduleVersion, Schedule, User, ApplicationInformation, Category, Executor, Responsible)
from .serializers import (FacultySerializer, SpecialitySerializer, TeacherSerializer, 
                          SubjectSerializer, LanguageSerializer, StudentStatusSerializer, 
                          NewsSerializer, NotificationSerializer, ApplicationSerializer, 
                          ApplicationStatusSerializer, TypeOfGradesSerializer, 
                          StudentSerializer, GradeSerializer, StudentOfFacultySerializer, 
                          StudentOfSpecialitySerializer, StudentOfLanguageSerializer, 
                          DayOfWeekSerializer, ScheduleVersionSerializer, ScheduleSerializer,
                          ApplicationInformationSerializer, ExecutorSerializer, ResponsibleSerializer, CategorySerializer)



def application_status_count():
    counts = Application.objects.values('status').annotate(count=Count('id'))
    return {item['status']: item['count'] for item in counts}



def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация успешна! Пожалуйста, войдите.")
            return redirect('login')  
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже.")
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def personal_cabinet(request):
    student = None
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
    return render(request, 'personal_cabinet.html', {'student': student})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')  # Редирект на главную страницу после успешного входа
                else:
                    messages.error(request, 'Неверный email или пароль.')
            except User.DoesNotExist:
                messages.error(request, 'Неверный email или пароль.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@api_view(['POST'])
def api_register(request):
    form = StudentRegistrationForm(request.data)
    if form.is_valid():
        user = form.save(commit=True)
        return Response({'message': 'Регистрация успешна.'}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'index.html')

@login_required
def user_settings(request):
    student = request.user.student 

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your settings have been updated successfully.')
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=student)

    return render(request, 'user_settings.html', {'form': form})
    



@login_required
def view_schedule(request):
    if request.method == 'POST':
        speciality_name = request.POST.get('speciality')
        sheet_name = SPECIALITY_SHEET_MAP.get(speciality_name)

        if sheet_name:
            try:
                scraper = ScheduleScraper(
                    file="timetable.xlsx", sheet_name=sheet_name)
                schedule = scraper.__post_init__()  # Get the schedule JSON
                return render(request, 'schedule.html', {'schedule': schedule, 'speciality': sheet_name})
            except Exception as e:
                print(e)
                messages.error(request, str(e))
        else:
            print(f'Sheet name for speciality "{speciality_name}" not found')
            messages.error(request, 'Speciality not found.')

    # Render the selection form if not a POST request
    specialties = Speciality.objects.filter(is_active=True)  # Fetch active specialties
    return render(request, 'select_speciality.html', {'specialities': specialties})


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

class SpecialityViewSet(viewsets.ModelViewSet):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class StudentStatusViewSet(viewsets.ModelViewSet):
    queryset = StudentStatus.objects.all()
    serializer_class = StudentStatusSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationInformationViewSet(viewsets.ModelViewSet):
    queryset = ApplicationInformation.objects.all()
    serializer_class = ApplicationInformationSerializer
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class ExecutorViewSet(viewsets.ModelViewSet):
    queryset = Executor.objects.all()
    serializer_class = ExecutorSerializer
    

class ResponsibleViewSet(viewsets.ModelViewSet):
    queryset = Responsible.objects.all()
    serializer_class = ResponsibleSerializer
    

class ApplicationStatusViewSet(viewsets.ModelViewSet):
    queryset = ApplicationStatus.objects.all()
    serializer_class = ApplicationStatusSerializer

class TypeOfGradesViewSet(viewsets.ModelViewSet):
    queryset = TypeOfGrades.objects.all()
    serializer_class = TypeOfGradesSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class StudentOfFacultyViewSet(viewsets.ModelViewSet):
    queryset = StudentOfFaculty.objects.all()
    serializer_class = StudentOfFacultySerializer

class StudentOfSpecialityViewSet(viewsets.ModelViewSet):
    queryset = StudentOfSpeciality.objects.all()
    serializer_class = StudentOfSpecialitySerializer

class StudentOfLanguageViewSet(viewsets.ModelViewSet):
    queryset = StudentOfLanguage.objects.all()
    serializer_class = StudentOfLanguageSerializer

class DayOfWeekViewSet(viewsets.ModelViewSet):
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer

class ScheduleVersionViewSet(viewsets.ModelViewSet):
    queryset = ScheduleVersion.objects.all()
    serializer_class = ScheduleVersionSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
