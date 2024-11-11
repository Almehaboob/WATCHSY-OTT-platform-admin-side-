from django.contrib.auth.models import AbstractUser
from django.db import models

class User_table(AbstractUser):
    is_blocked = models.BooleanField(default=False)




class Movie(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200)
    video = models.CharField(max_length=200)  
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    def __str__(self):
        return self.title



class Plan(models.Model):
    name=models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200)
    price=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    
    
class rating_table(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    user=models.ForeignKey(User_table,on_delete=models.CASCADE)
    rating=models.FloatField()
    



class UserSubscriptions(models.Model):
    user = models.ForeignKey(User_table, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)  # Automatically add the current date

    def __str__(self):
        return f"{self.user} subscribed to {self.plan}"

    
    
    

class watchlater_table(models.Model):
    user=models.ForeignKey(User_table,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    date=models.DateField()
    
    
    

class watch_history_table(models.Model):
    user=models.ForeignKey(User_table,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    date=models.DateField()
    