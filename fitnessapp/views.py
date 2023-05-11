from django.shortcuts import render
from rest_framework.views import APIView
from fitnessapp.renderers import UserRenderer
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, DietSerializer
from .serializers import ActivitySerializer, SendPasswordResetEmailSerializer, PasswordResetSerializer, WaterIntakeSerializer
from .serializers import FoodItemFilter, FoodItemSerializer, UserDietSerializer, DailyCalorieTargetSerializer
from rest_framework import status, generics, filters
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import csv
from django.http import HttpResponse
from .models import Diet, Activity, FoodItem,DailyCalorieTarget, CustomUser, WaterIntake
from rest_framework.decorators import api_view, permission_classes
import datetime
from django.core.cache import cache
from .models import Diet, UserDiet
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from itertools import groupby
from django.shortcuts import get_object_or_404

from django.utils import timezone
from datetime import *
from datetime import datetime
# Create your views here.




# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
    return Response({'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
      return Response({'message': 'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    

class AdminLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None and user.is_staff:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
      return Response({'message': 'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)    
    


class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = PasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated]) 
class DietList(APIView):
  def get(self, request, format=None):
    diets = Diet.objects.all()
    serializer = DietSerializer(diets, many = True)
    return Response(serializer.data)
  
  def post(self, request,format=None):
    csv_file = request.FILES.get('file')
    print(csv_file)
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    print("<---------------------------->")
    print(reader.fieldnames)
    for row in reader:
      diet = Diet.objects.create(
        Food=row['Food'],
        Measure=row['Measure'],
        Grams=row['Grams'],
        Calories=row['Calories'],
        Protein=row['Protein'],
        Fat=row['Fat'],
        Saturated_Fat = row['Saturated_Fat'],
        Fiber = row['Fiber'],
        Carbs = row['Carbs'],
        Category = row['Category']
        )
      diet.save()
    return HttpResponse("CSV file has been uploaded successfully")
  
@permission_classes([IsAuthenticated]) 
class FoodItemList(generics.ListAPIView):
    queryset = Diet.objects.all()
    serializer_class = DietSerializer
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filter_backends = [DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['Food', 'Category']

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)

        # create a new instance of SearchedDiet for each searched item
        # searched_diets = []
        # for diet in response.data:
        #     searched_diets.append({
        #         'Food': diet['Food'],
        #         'Category': diet['Category']
        #     })
        # serializer = SearchedDietSerializer(data=searched_diets, many=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        # return response


# @permission_classes([IsAuthenticated]) 
# class FoodItemList(generics.ListAPIView):
#     queryset = Diet.objects.all()
#     serializer_class = DietSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = FoodItemFilter




class ActivityView(APIView):
    def get(self, request, format=None):
        A_id = request.query_params.get('A_id')
        gym_activity = Activity.objects.filter(A_id=A_id)
        activity_level = self.get_activity_level(gym_activity)
        serializer = ActivitySerializer(gym_activity, many=True)
        data = serializer.data
        for activity in data:
          # activity_level = self.get_activity_level(gym_activity)
          activity['activity_level'] = activity_level
        return Response(data)
        
        data['activity_level'] = activity_level
        return Response(data)
    def post(self, request, format=None):
        serializer = ActivitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        A_id = serializer.data.get('A_id')
        steps = serializer.data.get('steps')
        calories_burned = serializer.data.get('calories_burned')
        workout_duration = serializer.data.get('workout_duration')
        s = steps + calories_burned + workout_duration
        return Response({'message': "Success",'activity level': s}, status=status.HTTP_200_OK)
           

        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
            return Response({'message': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

    def get_activity_level(self, gym_activity):
        activity_score = sum(activity.steps + activity.calories_burned + activity.workout_duration for activity in gym_activity)
        if activity_score > 10000:
            return "Highly Active"
        elif activity_score > 5000:
            return "Moderately Active"
        else:
            return "Less Active"
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_activity_level(request):
    calories_burned = request.data.get('calories_burned')
    print(calories_burned)
    steps_taken = request.data.get('steps_taken')
    print(steps_taken)
    workout_duration = request.data.get('workout_duration')
    print(workout_duration)

    if calories_burned is None:
       return Response({'error': 'calories_burned is required'}, status=400)
    if steps_taken is None:
       return Response({'error': 'steps_taken is required'}, status=400)
    if workout_duration is None:
       return Response({'error': 'workout_duration is required'}, status=400)

    # Calculate activity level based on inputs
    activity_level = calculate_activity_level(calories_burned, steps_taken, workout_duration)

    # Return activity level as response
    return Response({'activity_level': activity_level})

def calculate_activity_level(calories_burned, steps_taken, workout_duration):
    # Calculate total activity
    total_activity = int(calories_burned) + int(steps_taken) * 0.05 + int(workout_duration) * 10
    
    # Determine activity level based on total activity
    if total_activity < 100:
        activity_level = 'Sedentary'
    elif total_activity < 500:
        activity_level = 'Lightly Active'
    elif total_activity < 1000:
        activity_level = 'Moderately Active'
    else:
        activity_level = 'Very Active'

    return activity_level

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_bmi(request):
   user = request.user
   height = user.height
   weight = user.weight
   if height is None or weight is None:
      return Response({'error': 'Both height and weight are required'}, status=400)
   height_in_m = height / 100
   bmi = weight / (height_in_m ** 2)
   bmi = round(bmi, 2)
   y = ""
   if bmi < 18:
      y = "underweight"
   elif bmi < 25:
      y = "perfect"
   elif bmi < 30:
      y = "overweight"
   elif bmi > 30:
      y = "obese"
   return Response({'bmi': bmi, 'y': y})


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def calculate_user_bmi(request):
    height = request.data.get('height')
    weight = request.data.get('weight')
    if height is None:
        return Response({'error': 'height is required'}, status=400)
    if weight is None:
        return Response({'error': 'weight is required'}, status=400)
    height_in_m =(float(height) / 100)
    bmi = float(weight) / (height_in_m ** 2)
    bmi = round(bmi, 2)
    y = ""
    if bmi < 18:
      y = "underweight"
    elif bmi < 25:
      y = "perfect"
    elif bmi < 30:
      y = "overweight"
    elif bmi > 30:
      y = "obese"
    return Response({'bmi': bmi, 'y':y})


class SendPasswordResetEmailView(APIView):
   renderer_classes = [UserRenderer]
   def post(self, request, format=None):
      serializer = SendPasswordResetEmailSerializer(data = request.data)
      if serializer.is_valid(raise_exception=True):
         return Response({'msg':'Passsword Reset link send, Please check your email'}, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
   renderer_classes = [UserRenderer]
   def post(self, request, uid, token, format=None):
      serializer = PasswordResetSerializer(data=request.data,context={'uid':uid, 'token':token})
      if serializer.is_valid(raise_exception=True):
         return Response({'msg':'Password reset successfully'}, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_activity_level(request):
    if request.method == 'POST':
        user_id = request.user.id
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get today's date and the amount of water consumed
        # date = timezone.date()
        steps = request.data.get('steps')
        calories_burned = request.data.get('calories_burned')
        workout_duration = request.data.get('workout_duration')

        if steps is None:
            return Response({'error': 'steps_taken is required'}, status=400)
        
        if calories_burned is None:
            return Response({'error': 'calories_burned is required'}, status=400)
        
        if workout_duration is None:
            return Response({'error': 'workout_duration is required'}, status=400)
        
        activity = Activity(user=user, steps=steps, calories_burned=calories_burned, workout_duration=workout_duration, date=date)
        activity.save()

        # Calculate activity level based on inputs
        activity_level = calculate_activity_level(calories_burned, steps, workout_duration)

        # Return activity level as response
        return Response({'activity_level': activity_level})
        # Create a new WaterIntake object and save it to the database
        
def calculate_activity_level(calories_burned, steps_taken, workout_duration):
        # Calculate total activity
    total_activity = int(calories_burned) + int(steps_taken) * 0.05 + int(workout_duration) * 10
        
        # Determine activity level based on total activity
    if total_activity < 100:
        activity_level = 'Sedentary'
    elif total_activity < 500:
        activity_level = 'Lightly Active'
    elif total_activity < 1000:
        activity_level = 'Moderately Active'
    else:
        activity_level = 'Very Active'

    return activity_level
            
    
    if request.method == 'GET':
        user_id = request.user.id

        # Get date from request query params, default to today's date
        date_string = request.query_params.get('date', str(date.today()))

        # Parse date string into date object
        date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()

        # Get user's water intake for given date
        try:
            activity = Activity.objects.get(user_id=user_id, date=date_obj)
        except Activity.DoesNotExist:
            return Response({"detail": "Activity not found for the given date"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize water intake data and return response
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def add_water_intake(request):
    if request.method == 'POST':
        user_id = request.user.id
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get today's date and the amount of water consumed
        # date = timezone.date()
        glasses = request.data.get('glasses')

        # Create a new WaterIntake object and save it to the database
        intake = WaterIntake(user=user, date=date, glasses=glasses)
        intake.save()

        return Response({"message": "Water intake added successfully."}, status=status.HTTP_201_CREATED)
    
    
    if request.method == 'GET':
        user_id = request.user.id

        # Get date from request query params, default to today's date
        date_string = request.query_params.get('date', str(date.today()))

        # Parse date string into date object
        date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()

        # Get user's water intake for given date
        try:
            water_intake = WaterIntake.objects.get(user_id=user_id, date=date_obj)
        except WaterIntake.DoesNotExist:
            return Response({"detail": "Water intake not found for the given date"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize water intake data and return response
        serializer = WaterIntakeSerializer(water_intake)
        return Response(serializer.data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        # Invalidate the refresh and access tokens for the user
        try:
            refresh_token = request.COOKIES.get('refresh')
            if refresh_token:
                # blacklist the refresh token
                from rest_framework_simplejwt.tokens import RefreshToken
                token = RefreshToken(refresh_token)
                token.blacklist()
            # Clear the access token cookie
            response = Response({"detail": "Successfully logged out."})
            response.delete_cookie('access')
            return response
        except Exception as e:
            return Response({"detail": "An error occurred while logging out."}, status=500)
        

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def add_food_to_diet(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = FoodItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
       food_items = FoodItem.objects.filter(user=request.user)
       serializer = FoodItemSerializer(food_items, many=True)
       return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_food_to_meal(request):
    food_id = request.data.get('food_id')
    meal_type = request.data.get('meal_type')
    if not food_id or not meal_type:
        return Response({'error': 'food_id and meal_type are required.'}, status=status.HTTP_400_BAD_REQUEST)
    food = Diet.objects.get(id=food_id)
    if not food:
        return Response({'error': f'Could not find food with id={food_id}'}, status=status.HTTP_404_NOT_FOUND)
    user_diet, created = UserDiet.objects.get_or_create(user=request.user, food=food, meal_type=meal_type)
    if not created:
        return Response({'error': 'This food has already been added to your meal.'}, status=status.HTTP_400_BAD_REQUEST)
    # Copy over the relevant fields from the Diet object to the UserDiet object
    user_diet.FoodName = food.Food
    user_diet.Measure = food.Measure
    user_diet.Grams = food.Grams
    user_diet.Calories = food.Calories
    user_diet.Protein = food.Protein
    user_diet.Fat = food.Fat
    user_diet.Saturated_Fat = food.Saturated_Fat
    user_diet.Fiber = food.Fiber
    user_diet.Carbs = food.Carbs
    user_diet.Category = food.Category
    user_diet.save()
    serializer = UserDietSerializer(user_diet)
    return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_meals(request):
    user_diets = UserDiet.objects.filter(user=request.user).order_by('meal_type', 'date')
    meals_by_type = {}
    for user_diet in user_diets:
        meal_type = user_diet.meal_type
        if meal_type not in meals_by_type:
            meals_by_type[meal_type] = []
        meals_by_type[meal_type].append(user_diet)

    serializer_data = {}
    for meal_type, user_diets in meals_by_type.items():
        serializer_data[meal_type] = UserDietSerializer(user_diets, many=True).data

    return Response(serializer_data)



class DailyCalorieTargetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        target_calories = request.data.get('target_calories') 
        user = request.user
        if target_calories is None:
            return Response({'error': 'target_calories is required'}, status=400)

        # Check if a target for the day already exists
        try:
            daily_target = DailyCalorieTarget.objects.get(user=user, date_added=date.today())
            daily_target.target_calories = target_calories
            daily_target.save()
        except DailyCalorieTarget.DoesNotExist:
            daily_target = DailyCalorieTarget.objects.create(
                user=user,
                date_added=date.today(),
                target_calories=target_calories # Add this line
            )
        else:
            return Response({"message": "Target already exists"})

        return Response({"message": "Daily calorie target set successfully."})



@api_view(['POST'])
def set_meals_to_meet_target(request):
    # Get user's daily calorie target
    user_id = request.user.id
    target = DailyCalorieTarget.objects.get(user_id=user_id)
    calorie_target = target.target_calories

    # Calculate calorie limit for each meal
    breakfast_limit = round(calorie_target * 0.3)
    lunch_limit = round(calorie_target * 0.4)
    dinner_limit = round(calorie_target * 0.3)

    # Get food items from UserDiet table for the user
    user_diet_items = UserDiet.objects.filter(user_id=user_id)

    # Sort food items by calorie count
    sorted_items = sorted(user_diet_items, key=lambda x: x.Calories)

    # Initialize meal lists
    breakfast = []
    lunch = []
    dinner = []

    # Add food items to each meal until the calorie limit is reached
    for item in sorted_items:
        if int(item.Calories) <= breakfast_limit:
            breakfast.append(item)
            breakfast_limit -= int(item.Calories)
        elif int(item.Calories) <= lunch_limit:
            lunch.append(item)
            lunch_limit -= int(item.Calories)
        elif int(item.Calories) <= dinner_limit:
            dinner.append(item)
            dinner_limit -= int(item.Calories)

        # Break out of loop if all meals have reached their calorie limit
        if breakfast_limit == 0 and lunch_limit == 0 and dinner_limit == 0:
            break

    # Serialize meal lists and return response
    breakfast_serializer = UserDietSerializer(breakfast, many=True)
    lunch_serializer = UserDietSerializer(lunch, many=True)
    dinner_serializer = UserDietSerializer(dinner, many=True)

    response_data = {
        "breakfast": breakfast_serializer.data,
        "lunch": lunch_serializer.data,
        "dinner": dinner_serializer.data
    }

    return Response(response_data)

@api_view(['GET'])
def get_meals_to_meet_target(request):
    # Get user's daily calorie target
    user_id = request.user.id
    target = DailyCalorieTarget.objects.get(user_id=user_id)
    calorie_target = target.target_calories

    # Calculate calorie limit for each meal
    breakfast_limit = round(calorie_target * 0.3)
    lunch_limit = round(calorie_target * 0.4)
    dinner_limit = round(calorie_target * 0.3)

    # Get food items from UserMeal table for the user
    user_meals = UserMeal.objects.filter(user_id=user_id)

    # Initialize meal lists
    breakfast = []
    lunch = []
    dinner = []

    # Add food items to each meal
    for meal in user_meals:
        if meal.meal_type == "Breakfast":
            breakfast.append(meal)
            breakfast_limit -= int(meal.food.Calories)
        elif meal.meal_type == "Lunch":
            lunch.append(meal)
            lunch_limit -= int(meal.food.Calories)
        elif meal.meal_type == "Dinner":
            dinner.append(meal)
            dinner_limit -= int(meal.food.Calories)

    # Serialize meal lists and return response
    breakfast_serializer = UserMealSerializer(breakfast, many=True)
    lunch_serializer = UserMealSerializer(lunch, many=True)
    dinner_serializer = UserMealSerializer(dinner, many=True)

    response_data = {
        "breakfast": breakfast_serializer.data,
        "lunch": lunch_serializer.data,
        "dinner": dinner_serializer.data
    }

    return Response(response_data)
