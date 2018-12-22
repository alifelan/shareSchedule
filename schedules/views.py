from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from schedules.models import Class, Group, Teacher, Student, Date
from os import listdir
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta

# Create your views here.

def handler500(request):
    return render(request, 'schedules/500.html')

def index(request):
    return render(request, 'schedules/index.html')

def students(request):
    students = Student.objects.all()
    return render(request, 'schedules/students.html', {'students':students})

def classes(request):
    return render(request, 'schedules/classes.html', {'classes': Class.objects.all()})

def class_detail(request, class_id):
    current_class = Class.objects.get(class_id=class_id)
    groups = Group.objects.filter(class_id=current_class)
    students_enrolled= {}
    for group in groups:
        students_enrolled[group.group_number] = []
        for student_enrolled in Student.objects.filter(enrolled_in=group):
            students_enrolled[group.group_number].append(student_enrolled)
    return render(request, 'schedules/class_detail.html', {'class_': current_class, 'groups':groups, 'students_enrolled':students_enrolled})

def group_detail(request, class_id, group_number):
    current_class = Class.objects.get(class_id=class_id)
    group = Group.objects.get(class_id=current_class, group_number=group_number)
    students_enrolled = Student.objects.filter(enrolled_in=group)
    return render(request, 'schedules/group_detail.html', {'class_':current_class, 'group':group, 'students_enrolled':students_enrolled})

def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    groups = student.enrolled_in.all()
    students_enrolled = {}
    for group in groups:
        students_enrolled[group.class_id.class_id] = []
        for student_enrolled in Student.objects.filter(enrolled_in=group):
            students_enrolled[group.class_id.class_id].append(student_enrolled)
        students_enrolled[group.class_id.class_id].remove(student)
    return render(request, 'schedules/student_detail.html', {'student':student, 'groups':groups, 'students_enrolled':students_enrolled})

def register(request):
    try:
        rawSchedule = request.FILES['rawSchedule.html'].read()
        name = request.POST['name']
    except KeyError:
        return render(request, 'schedules/register.html')
    else:
        soup = bs(rawSchedule, features="html.parser")
        table = soup.find('div', alink='#0000ff', vlink='#0000ff', style='background-color:#FFFFFF')
        if not table:
            table = soup.find('div', alink='#0000ff', vlink='#0000ff', style='background-color:white;')
        if not table:
            table = soup.find('div', alink='#0000FF', vlink='#0000FF', style='background-color:white;')
        if not table:
            table = soup.find('div', alink='#0000ff', vlink='#0000ff', style='background-color:#ffffff')
        if not table:
            table = soup.find('div', alink='#0000FF', vlink='#0000FF', style='background-color:#FFFFFF')
        if not table:
            table = soup.find('div', alink='#0000FF', vlink='#0000FF', style='background-color:ffffff')
        if not table:
            table = soup.find('div', alink='#0000ff', vlink='#0000ff', bgcolor="#FFFFFF")
        if not table:
            table = soup.find('div', id='contentDiv', class_='col-md-10 topPadding')
        table = table.find_all('center')[2].find('table').find('table')
        try:
            student = Student.objects.get(student_name=name)
            student.enrolled_in.clear()
        except ObjectDoesNotExist:
            student = Student(student_name=name)
            student.save()
        cl = []
        classes = []
        for row in table.find_all('tr'):
            if row['bgcolor'] == '#9bbad6' or row['bgcolor'] == '#9BBAD6':
                classes.append(cl)
                cl = []
                cl.append(row)
            else:
                cl.append(row)
        classes.append(cl)
        classes = classes[1:]
        for cl in classes:
            class_text = cl[0].find('code').text
            class_id = class_text[:class_text.find('.')]
            try:
                current_class = Class.objects.get(class_id=class_id)
            except ObjectDoesNotExist:
                class_name = class_text[class_text.find(' ') + 1:]
                current_class = Class(class_id=class_id, class_name=class_name)
                current_class.save()
            class_group = class_text[class_text.find('.') + 1:class_text.find(' ')]
            try:
                group = Group.objects.get(class_id=current_class, group_number=class_group, semester='EM2019')
            except ObjectDoesNotExist:
                group = Group(class_id=current_class, group_number=class_group, semester='EM2019')
                group.save()
            student.enrolled_in.add(group)
            for l in cl[1:]:
                if l['align'] == 'left' and 'Atributo' not in l.find('code').string:
                    teacher_name = l.find_all('code')[1].contents[0]
                    try:
                        teacher = Teacher.objects.get(teacher_name=teacher_name)
                    except ObjectDoesNotExist:
                        teacher = Teacher(teacher_name=teacher_name)
                        teacher.save()
                    group.teachers.add(teacher)
                elif l['align'] == 'center' and (l['bgcolor'] == '#EEEEEE' or l['bgcolor'] == '#eeeeee'):
                    data = l.find_all('code')
                    days = []
                    for i, c in enumerate(data[1].string.replace('\xa0', ' ')):
                        if c != ' ':
                            days.append(i)
                    time = data[2].string.split(' a ')
                    if time[0][0] == ' ':
                        time[0] = time[0][1:]
                    if time[1][0] == ' ':
                        time[1] = time[1][1:]
                    fmt = '%H:%M'
                    split_time = time[0].split(':')
                    time_dec = int(split_time[0]) * 60 + int(split_time[1]) - 7 * 60
                    time_id = time_dec // 90 if time_dec % 90 == 0 else 8
                    date_ids = []
                    for day in days:
                        date_ids.append(1 + time_id + day * 10)
                        group.dates.add(Date.objects.get(id=date_ids[-1]))
                    if (datetime.strptime(time[1], fmt) - datetime.strptime(time[0], fmt)).seconds // 60 > 90:
                        for date_id in date_ids:
                            group.dates.add(Date.objects.get(id=date_id + 1))
        return HttpResponseRedirect(reverse('schedules:student_detail', kwargs={'student_id': student.id}))


def free(request):
    return render(request, 'schedules/base.html')


def free_day(request, day_name):
    day_names = ['domingo', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado']
    try:
        day_id = day_names.index(day_name.lower())
    except ValueError:
        return render(request, 'schedules/error.html', {'error_message':'Ese dia no existe prro'})
    dates = Date.objects.all()[day_id * 10:(day_id + 1) * 10]
    students = Student.objects.all()
    students_free = []
    for date in dates:
        students_in_class = []
        for group in date.groups.all():
            students_in_class.extend(list(group.students.all()))
        students_free.append(list(set(students) - set(students_in_class)))
    students_free_at_date = zip(dates, students_free)
    return render(request, 'schedules/free_day.html', {'day_name':day_name, 'students_free_at_date':students_free_at_date})


def addDates():
    Date.objects.all().delete()
    days = [0, 1, 2, 3, 4, 5]
    x = datetime(1,1,1,7)
    for day in days:
        for i in range(8):
            time = (x + timedelta(hours=1, minutes=30) * i).time()
            Date(day=day, time=time).save()
        Date(day=day, time=datetime(1,1,1,18).time()).save()
        Date(day=day, time=datetime(1,1,1,19,30).time()).save()


#def add_groups(request):
#    for file_name in listdir('./groups/'):
#        with open(file_name, encoding='ISO-8859-1') as file:
#            soup = bs(file)
#        groups = []
#        group = []
#        table = soup.find('table').find_all('table')[2]
