from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Diet, Activity, UserDiet, DailyCalorieTarget, WaterIntake
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'name', 'is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('name',)}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'name','password', 'password1'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(CustomUser, UserModelAdmin)

admin.site.register(Diet)
admin.site.register(Activity)
# admin.site.register(WaterIntake)
admin.site.register(UserDiet)
admin.site.register(DailyCalorieTarget)
admin.site.register(WaterIntake)
