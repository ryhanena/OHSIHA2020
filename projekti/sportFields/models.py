from django.db import models

class sportField(models.Model):
    fieldId = models.CharField(max_length=20)
    fieldName = models.CharField(max_length=100)
    fieldLocation = models.CharField(max_length=200)
    class Meta:
        db_table = "sportField"
# Create your models here.
