from django.db import models

# Create your models here.
# class City(models.Model):
#     name = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.name}: {self.country}"


# class Weather(models.Model):
#     city = models.ForeignKey(City, on_delete=models.CASCADE)
#     temperature = models.FloatField()
#     description = models.CharField(max_length=250)
#     icon = models.CharField(max_length=20)
#     date_time = models.DateTimeField()

#     def __str__(self):
#         return f"{self.city}- {self.date_time}"


class City(models.Model):
    #city = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    #country = models.CharField(max_length=100)
    temperature = models.FloatField(default=0)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=20)
    #date_time = models.DateTimeField(default="")
    
    def __str__(self):
        return f"{self.city}"