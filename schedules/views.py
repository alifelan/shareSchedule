from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from schedules.models import Class, Group, Teacher, Student, Date
from bs4 import BeautifulSoup as bs4
from datetime import datetime, timedelta

# Create your views here.

def index(request):
    return HttpResponse('index')

def classes(request):
    return render(request, 'schedules/classes.html', {'classes': Class.objects.all()})

def class_detail(request, class_id):
    current_class = Class.objects.get(class_id=class_id)
    groups = Group.objects.filter(class_id=current_class)
    return render(request, 'schedules/class_detail.html', {'class_details': current_class, 'groups':groups})

def group_detail(request, class_id, group_number):
    current_class = Class.objects.get(class_id=class_id)
    group = Group.objects.get(class_id=current_class, group_number=group_number)
    students_enrolled = Student.objects.filter(enrolled_in=group)
    return render(request, 'schedules/group_detail.html', {'class_details':current_class, 'group_details':group, 'students_enrolled':students_enrolled})

def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    groups = student.enrolled_in.all()
    return render(request, 'schedules/student_detail.html', {'student':student, 'groups':groups})

def register(request):
    try:
        rawSchedule = request.POST['rawSchedule']
        name = request.POST['name']
    except KeyError:
        return render(request, 'schedules/register.html')
    else:
        if not Student.objects.filter(student_name=name):
            Student(student_name=name).save()
        student = Student.objects.get(student_name=name)
        table = bs4(rawSchedule).find('div', alink='#0000ff', vlink='#0000ff', leftmargin='0', topmargin='0', style='background-color:#FFFFFF').find_all('center')[2].find('table').find('table')
        cl = []
        classes = []
        for row in table.find_all('tr'):
            if row['bgcolor'] == '#9bbad6':
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
            if not Class.objects.filter(class_id=class_id):
                class_name = class_text[class_text.find(' ') + 1:]
                Class(class_id=class_id, class_name=class_name).save()
            current_class = Class.objects.get(class_id=class_id)
            class_group = class_text[class_text.find('.') + 1:class_text.find(' ')]
            if not Group.objects.filter(class_id=current_class, group_number=class_group, semester='EM2019'):
                Group(class_id=current_class, group_number=class_group, semester='EM2019').save()
            group = Group.objects.get(class_id=current_class, group_number=class_group, semester='EM2019')
            student.enrolled_in.add(group)
            for l in cl[1:]:
                if l['align'] == 'left' and 'Atributo' not in l.find('code').string:
                    teacher_name = l.find_all('code')[1].contents[0]
                    if not Teacher.objects.filter(teacher_name=teacher_name):
                        Teacher(teacher_name=teacher_name).save()
                    group.teachers.add(Teacher.objects.get(teacher_name=teacher_name))
                elif l['align'] == 'center' and l['bgcolor'] == '#EEEEEE':
                    data = l.find_all('code')
                    days = []
                    for i, c in enumerate(data[1].string[1:].replace('\xa0', ' ')):
                        if c != ' ':
                            days.append(i)
                    time = data[2].string.split(' a ')
                    fmt = '%H:%M'
                    split_time = time[0].split(':')
                    time_dec = int(split_time[0]) * 60 + int(split_time[1]) - 7 * 60
                    time_id = time_dec // 90 if time_dec % 90 == 0 else 9
                    date_ids = []
                    for day in days:
                        date_ids.append(11 + time_id + day * 10)
                        group.dates.add(Date.objects.get(id=date_ids[-1]))
                    if (datetime.strptime(time[1], fmt) - datetime.strptime(time[0], fmt)).seconds // 60 > 90:
                        for date_id in date_ids:
                            group.dates.add(Date.objects.get(id=date_id + 1))
        return HttpResponseRedirect(reverse('index'))
