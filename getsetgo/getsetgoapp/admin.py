from django.contrib import admin
from .models import VehicleCategory,Vehicle
# Register your models here.

# Register VehicleCategory model in the admin interface
class VehicleCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # 'name' is the field in the VehicleCategory model

admin.site.register(VehicleCategory, VehicleCategoryAdmin)

# Register Vehicle model in the admin interface
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['v_name', 'v_model', 'v_category', 'v_rate']

admin.site.register(Vehicle, VehicleAdmin)


