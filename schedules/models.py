from django.db import models
import calendar

# Create your models here.


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=40)

    def __str__(self):
        return self.teacher_name


class Class(models.Model):
    class_id = models.CharField(max_length=6, primary_key=True)
    class_name = models.CharField(max_length=50)

    def __str__(self):
        return self.class_name



class Date(models.Model):
    day = models.PositiveSmallIntegerField()
    time = models.TimeField()

    def __str__(self):
        return list(calendar.day_name)[self.day] + ' at ' + str(self.time)

    class Meta:
        unique_together = (("day", "time"),)


class Group(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    group_number = models.IntegerField()
    teachers = models.ManyToManyField(Teacher)
    #classroom = models.CharField(max_length=10)
    semester = models.CharField(max_length=6)
    dates = models.ManyToManyField(Date)

    def __str__(self):
        return self.class_id.class_name + ' group ' + str(self.group_number)

    class Meta:
        unique_together = (("group_number", "class_id", "semester"),)


class Student(models.Model):
    student_name = models.CharField(max_length=40)
    enrolled_in = models.ManyToManyField(Group)

    def __str__(self):
        return self.student_name
