"""Models."""
from django.db import models

# Create your models here.


class Teacher(models.Model):
    """Teacher model."""

    teacher_name = models.CharField(max_length=40)

    def __str__(self):
        """Return string."""
        return self.teacher_name


class Class(models.Model):
    """Class model."""

    class_id = models.CharField(max_length=6, primary_key=True)
    class_name = models.CharField(max_length=50)

    def __str__(self):
        """Return string."""
        return "%s %s" % (self.class_id, self.class_name)


class Date(models.Model):
    """Date model."""

    day = models.PositiveSmallIntegerField()
    time = models.TimeField()

    def __str__(self):
        """Return string."""
        day_names = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves',
                     'Viernes', 'Sabado']
        return "%s a las %s" % (day_names[self.day],
                                self.time.strftime("%H:%M"))

    class Meta:
        """Meta."""

        unique_together = (("day", "time"),)


class Group(models.Model):
    """Group model."""

    class_id = models.ForeignKey(Class, related_name='groups',
                                 on_delete=models.CASCADE)
    group_number = models.IntegerField()
    teachers = models.ManyToManyField(Teacher, related_name='groups')
    # classroom = models.CharField(max_length=10)
    semester = models.CharField(max_length=6)
    dates = models.ManyToManyField(Date, related_name='groups')

    def __str__(self):
        """Return string."""
        return "%s %s grupo %s" % (self.class_id.class_id,
                                   self.class_id.class_name, self.group_number)

    class Meta:
        """Meta."""

        unique_together = (("group_number", "class_id", "semester"),)


class Homework(models.Model):
    """Homework model."""

    text = models.TextField()
    group_id = models.ForeignKey(Group, related_name='Homework',
                                 on_delete=models.CASCADE)

    def __str__(self):
        """Return string."""
        return "%s" % (self.text)


class Student(models.Model):
    """Student model."""

    student_name = models.CharField(max_length=40)
    enrolled_in = models.ManyToManyField(Group, related_name='students')

    def __str__(self):
        """Return string."""
        return self.student_name
