from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('adminlogin/', views.AdminLoginView.as_view(), name='adminlogin'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('changepassword/', views.UserChangePasswordView.as_view(), name='changepassword'),
    path('dietlist/', views.DietList.as_view(), name='diet'),
    path('dietlist/search/', views.FoodItemList.as_view(), name='food_item_search'),
    path('add-food/', views.add_food_to_diet, name='add_food'),
    path('activity/', views.ActivityView.as_view(), name='activity'),
    path('activity-level/', views.get_activity_level, name='activity-level'),
    path('calculate-bmi/', views.calculate_bmi, name='calculate_bmi'),
    path('bmi/', views.calculate_user_bmi, name='calculate_user_bmi'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('send-reset-password-email/', views.SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', views.PasswordResetView.as_view(), name='reset-password'),
    path('water_intake/', views.add_water_intake, name='add_water_intake'),
    # path('water-intake/', views.WaterIntakeListCreateView.as_view(), name='water_intake_list_create'),
    # path('search_diet/', views.search_diet, name='search_diet'),
    # path('add_food_to_diet/', views.add_food_to_diet, name='add_food_to_diet'),
    path('add_food_to_meal/', views.add_food_to_meal, name='add_food_to_meal'),
    path('get_user_meals/', views.get_user_meals, name='get_user_meals'),
    path('DailyCalorieTargetView/', views.DailyCalorieTargetView.as_view(), name='DailyCalorieTargetView'),
    # path('set_meals_to_meet_target/', views.set_meals_to_meet_target, name='set_meals_to_meet_target'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    ]
