from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import serializers
from fitnessapp.utils import Util
from .models import CustomUser, Diet, Activity, FoodItem, UserDiet, DailyCalorieTarget, WaterIntake
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import django_filters

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password1 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = CustomUser
    fields=['email', 'name','height', 'weight', 'age', 'password', 'password1']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password1 = attrs.get('password1')
    if password != password1:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return CustomUser.objects.create_user(**validate_data)
  

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = CustomUser
    fields = ['email', 'password']


class AdminLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = CustomUser
    fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['id', 'email', 'name','height', 'weight', 'age',]


class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password1 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password1']

  def validate(self, attrs):
    password = attrs.get('password')
    password1 = attrs.get('password1')
    user = self.context.get('user')
    if password != password1:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs
  
class DietSerializer(serializers.ModelSerializer):
  class Meta:
    model = Diet
    fields = '__all__'

class UserDietSerializer(serializers.ModelSerializer):
   class Meta:
      model = UserDiet
      fields = '__all__'

class FoodItemFilter(django_filters.FilterSet):
    class Meta:
        model = Diet
        fields = {
            'Food': ['icontains'],
            'Category': ['icontains'],
        }

class DietFilter(django_filters.FilterSet):
    Food = django_filters.CharFilter(lookup_expr='icontains')
    Category = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Diet
        fields = ['Food', 'Category']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField()
  class Meta:
    fields = ['email']

  def validate(self,attrs):
    email = attrs.get('email')
    if CustomUser.objects.filter(email=email).exists():
      user = CustomUser.objects.get(email=email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:8000/reset/'+uid+'/'+token
      print('Password Reset Link', link)
      body = 'Click following link to reset your password' + link
      data = {
        'subject':'Reset your password',
        'body': body,
        'to_email': user.email

      }
      Util.send_email(data)
      return attrs
    else:
      raise ValidationErr('You are not the registered user')
    
class PasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=100, style={'input_type':'password'}, write_only=True)
  password1 = serializers.CharField(max_length=100, style={'input_type': 'password'}, write_only=True)
  class Meta:
    fields = ['password','password1']

  def validate(self,attrs):
    try:
      password = attrs.get('password')
      password1 = attrs.get('password1')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password1:
        raise serializers.ValidationError("Password and confirm password do not match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = CustomUser.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise ValidationError('Token is not valid or expired')

      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user,token)
      raise ValidationError('Token is not valid')
    

class WaterIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        fields = '__all__'


class FoodItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model = FoodItem
        fields = ('user', 'name', 'calories', 'meal_type', 'date_added')


class DailyCalorieTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCalorieTarget
        fields = ('target_calories','date_added')
        unique_together = ('target_calories','date_added')
