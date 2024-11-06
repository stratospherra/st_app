from rest_framework import serializers
from .models import (Student, Faculty, StudentOfFaculty, Speciality, Teacher, Subject, Language, 
                     StudentStatus, News, Notification, Application, ApplicationStatus, 
                     StudentOfLanguage, StudentOfSpeciality, TypeOfGrades, Grade, 
                     DayOfWeek, ScheduleVersion, Schedule, ApplicationInformation, Category, Executor, Responsible)

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class StudentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStatus
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class ApplicationInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationInformation
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = '__all__'

class ResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsible
        fields = '__all__'

class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = '__all__'

class TypeOfGradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfGrades
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class StudentOfFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOfFaculty
        fields = '__all__'

class StudentOfSpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOfSpeciality
        fields = '__all__'

class StudentOfLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOfLanguage
        fields = '__all__'

class DayOfWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfWeek
        fields = '__all__'

class ScheduleVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleVersion
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
