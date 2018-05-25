from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=200)
    LEVEL1 = '1'
    LEVEL2 = '2'
    LEVEL3 = '3'
    PRIVILEGE = (
        (LEVEL1, '低'),
        (LEVEL2, '中'),
        (LEVEL3, '高'),
    )
    privilege = models.CharField(
        max_length=1,
        choices=PRIVILEGE,
        default=LEVEL1,
    )

class Door(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    LEVEL1 = '1'
    LEVEL2 = '2'
    LEVEL3 = '3'
    LEVEL = (
        (LEVEL1, '低'),
        (LEVEL2, '中'),
        (LEVEL3, '高'),
    )
    level = models.CharField(
        max_length=1,
        choices=LEVEL,
        default=LEVEL3,
    )

class DoorOpen(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    datetime = models.DateTimeField('time')
