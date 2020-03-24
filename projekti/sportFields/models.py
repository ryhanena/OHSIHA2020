from django.db import models

class sportField(models.Model):
    #Luo automaattisesti myös ID:n, fieldId turha?
    fieldId = models.IntegerField()
    fieldName = models.CharField(max_length=100)
    fieldLocation = models.CharField(max_length=200)

    def __str__(self):
        return self.fieldName
    
