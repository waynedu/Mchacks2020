from django.db import models


class Family(models.Model):
    last_name = models.CharField(max_length=50, default='')


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email_address = models.CharField(max_length=50)
    dob = models.CharField(max_length=50)
    last_known_location = models.CharField(max_length=15000, default='')
    subject_id = models.CharField(max_length=50)

    family = models.ForeignKey(Family, default=None, null=True, on_delete=models.CASCADE)



