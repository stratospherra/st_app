from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import register, user_login, api_register
from .views import (FacultyViewSet, SpecialityViewSet, TeacherViewSet, SubjectViewSet, LanguageViewSet, 
                    StudentStatusViewSet, NewsViewSet, NotificationViewSet, ApplicationViewSet, 
                    ApplicationStatusViewSet, TypeOfGradesViewSet, StudentViewSet, GradeViewSet, 
                    StudentOfFacultyViewSet, StudentOfSpecialityViewSet, StudentOfLanguageViewSet, 
                    DayOfWeekViewSet, ScheduleVersionViewSet, ScheduleViewSet,
                    ApplicationInformationViewSet, CategoryViewSet, ExecutorViewSet, ResponsibleViewSet)
from . import views
from django.conf import settings
from django.conf.urls.static import static


# Создаем роутер для автоматического определения URL.
router = DefaultRouter()
router.register(r'faculties', FacultyViewSet)
router.register(r'specialities', SpecialityViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'student-statuses', StudentStatusViewSet)
router.register(r'news', NewsViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'application-informations', ApplicationInformationViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'executor', ExecutorViewSet)
router.register(r'responsible', ResponsibleViewSet)
router.register(r'application-statuses', ApplicationStatusViewSet)
router.register(r'type-of-grades', TypeOfGradesViewSet)
router.register(r'students', StudentViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'student-of-faculties', StudentOfFacultyViewSet)
router.register(r'student-of-specialities', StudentOfSpecialityViewSet)
router.register(r'student-of-languages', StudentOfLanguageViewSet)
router.register(r'day-of-weeks', DayOfWeekViewSet)
router.register(r'schedule-versions', ScheduleVersionViewSet)
router.register(r'schedules', ScheduleViewSet)

# URL-паттерны Django, включающие все роутеры для автоматической маршрутизации.
urlpatterns = [
    path('api/', include(router.urls)),
    path('index/', views.index, name='index'),
    path('personal_cabinet/', views.personal_cabinet, name='personal_cabinet'),
    path('', register, name='register'),
    path('login/', user_login, name='login'),
    path('api/register/', api_register, name='api_register'),
    path('view_schedule/', views.view_schedule, name='view_schedule'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)