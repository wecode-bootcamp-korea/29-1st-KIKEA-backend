from django.db   import models
from core.models import TimeStampModel

class User(TimeStampModel):
    name         = models.CharField(max_length=45)
    email        = models.EmailField(max_length=100, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)
    address      = models.CharField(max_length=100)
    point        = models.PositiveIntegerField()

    class Meta:
        db_table = 'users'