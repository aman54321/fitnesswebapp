from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.utils import timezone
import datetime
#  Custom User Manager
class CustomUserManager(BaseUserManager):
  def create_user(self, email, name, height, weight, age, password=None, password1=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
            email=self.normalize_email(email),
            name=name,
            height=height,
            weight=weight,
            age=age
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, height, weight, age, name, password):
      """
      Creates and saves a superuser with the given email, name and password.
      """
      user = self.create_user(
          email,
          name=name,
          height=height,
          weight=weight,
          age=age,
          password=password
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class CustomUser(AbstractBaseUser):
  email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
  name = models.CharField(max_length=255)
  height = models.FloatField()
  weight = models.FloatField()
  age = models.IntegerField()
  password = models.CharField(max_length=100)

  is_active = models.BooleanField(default=True)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'height', 'weight', 'age','password']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
    #   return self.is_admin
      return True

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin



class Diet(models.Model):
    Food = models.CharField(max_length=100)
    Measure = models.CharField(max_length=100)
    Grams = models.IntegerField()
    Calories = models.CharField(max_length=100)
    Protein = models.CharField(max_length=100)
    Fat = models.CharField(max_length=100)
    Saturated_Fat = models.CharField(max_length=100)
    Fiber = models.CharField(max_length=100)
    Carbs = models.CharField(max_length=100)
    Category = models.CharField(max_length=100)

    def __str__(self):
        return self.Food
    
class UserDiet(models.Model):
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food = models.ForeignKey(Diet, on_delete=models.CASCADE)
    FoodName = models.CharField(max_length=100, blank=True)
    Measure = models.CharField(max_length=100)
    Grams = models.IntegerField(null=True)
    Calories = models.CharField(max_length=100)
    Protein = models.CharField(max_length=100)
    Fat = models.CharField(max_length=100)
    Saturated_Fat = models.CharField(max_length=100)
    Fiber = models.CharField(max_length=100)
    Carbs = models.CharField(max_length=100)
    Category = models.CharField(max_length=100)
    meal_type = models.CharField(choices=MEAL_CHOICES, max_length=50)
    date = models.DateField(default=datetime.date.today)


class Activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    steps = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    workout_duration = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'date']


class WaterIntake(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    glasses = models.PositiveIntegerField()

    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user} - {self.glasses} glasses"



class FoodItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    meal_type = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'date_added']


class DailyCalorieTarget(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    target_calories = models.PositiveIntegerField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'date_added']

