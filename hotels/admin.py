from django.contrib import admin
from .models import City, Hotel, HotelPrice, Journey, Car, CarPrice, JourneyPrice
# --- أسعار الفندق ضمن الفندق مباشرة
class HotelPriceInline(admin.TabularInline):
    model = HotelPrice
    extra = 1  # عدد الصفوف الفارغة الجديدة

class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'rating', 'room_type', 'view_type']
    list_filter = ['city', 'room_type', 'view_type']
    search_fields = ['name']
    inlines = [HotelPriceInline]  # عرض أسعار الفندق مباشرة داخل صفحة الفندق
    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'url', 'city', 'rating', 'view_type', 'room_type')
        }),
        ('صور الفندق', {
            'fields': ('image_main', 'image_1', 'image_2')
        }),
    )
# --- أسعار السيارة
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_type', 'fuel_type', 'transmission', 'model_year')

@admin.register(CarPrice)
class CarPriceAdmin(admin.ModelAdmin):
    list_display = ('car', 'start_date', 'end_date', 'price_per_day')
    list_filter = ('start_date', 'end_date')
    search_fields = ('car__name',)

# --- أسعار الرحلات داخل الرحلة
class JourneyPriceInline(admin.TabularInline):
    model = JourneyPrice
    extra = 1

class JourneyAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    inlines = [JourneyPriceInline]

@admin.register(Journey)
class RegisteredJourneyAdmin(JourneyAdmin):
    pass

@admin.register(JourneyPrice)
class JourneyPriceAdmin(admin.ModelAdmin):
    list_display = ('journey', 'start_date', 'end_date', 'price_usd')  
    list_filter = ('start_date',)
    search_fields = ('journey__name',)
# --- أسعار الفندق

class HotelPriceAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'start_date', 'end_date', 'num_guests', 'price_usd', 'breakfast_included', 'sea_view']
    list_filter = ['start_date', 'num_guests', 'breakfast_included', 'sea_view']
    search_fields = ['hotel__name']

admin.site.register(City)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelPrice, HotelPriceAdmin)