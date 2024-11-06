from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import TypeOfGrades, DayOfWeek

@receiver(post_migrate)
def create_grade_types(sender, **kwargs):
    if sender.name == 'main':  
        grades = [
            ('ср.т1', True),
            ('ср.т2', True),
            ('рк1', True),
            ('Р1', True),
            ('рк2', True),
            ('Р2', True),
            ('Общий Рейтинг', True),
            ('Экзамен', True),
            ('итог оценка', True),
        ]

        for title, calculate in grades:
            TypeOfGrades.objects.get_or_create(title=title, calculate=calculate)



def create_weekdays(sender, **kwargs):
    weekdays = [
        {'name_en': 'Monday', 'name_kz': 'Дүйсенбі', 'name_ru': 'Понедельник'},
        {'name_en': 'Tuesday', 'name_kz': 'Сейсенбі', 'name_ru': 'Вторник'},
        {'name_en': 'Wednesday', 'name_kz': 'Сәрсенбі', 'name_ru': 'Среда'},
        {'name_en': 'Thursday', 'name_kz': 'Бейсенбі', 'name_ru': 'Четверг'},
        {'name_en': 'Friday', 'name_kz': 'Жұма', 'name_ru': 'Пятница'},
        {'name_en': 'Saturday', 'name_kz': 'Сенбі', 'name_ru': 'Суббота'},
        {'name_en': 'Sunday', 'name_kz': 'Жексенбі', 'name_ru': 'Воскресенье'},
    ]
    for weekday_data in weekdays:
        DayOfWeek.objects.get_or_create(
            name_en=weekday_data['name_en'],
            name_kz=weekday_data['name_kz'],
            name_ru=weekday_data['name_ru'],
        )
    # for weekday_data in weekdays:
    #     DayOfWeek.objects.get_or_create(
    #         name_en=weekday_data['name_en'],
    #         defaults={'name_kz': weekday_data['name_kz'], 'name_ru': weekday_data['name_ru']},
    #     )