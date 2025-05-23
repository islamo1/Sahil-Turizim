from django.db import models
from django.contrib.auth.models import User

class City(models.Model): 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hotel(models.Model): 
    name = models.CharField(max_length=200) 
    phone = models.CharField(max_length=20, blank=True) 
    url = models.URLField(blank=True) 
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True) 
    rating = models.FloatField(blank=True, null=True) 
    view_type = models.CharField(
        max_length=50, blank=True,
        choices=[('city', 'City'), ('sea', 'Sea'), ('mountain', 'Mountain')]
    ) 
    room_type = models.CharField(
        max_length=50, blank=True,
        choices=[('single', 'Single'), ('double', 'Double'), ('suite', 'Suite'), ('apartment', 'Apartment')]
    )
# 🖼️ الصور
    image_main = models.URLField(blank=True, help_text="رابط صورة رئيسية للفندق")
    image_1 = models.URLField(blank=True, help_text="صورة إضافية رقم 1")
    image_2 = models.URLField(blank=True, help_text="صورة إضافية رقم 2")
    def __str__(self):
        return f"{self.name} - {self.city.name if self.city else 'No City'}"


class HotelPrice(models.Model): 
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="prices") 
    start_date = models.DateField() 
    end_date = models.DateField() 
    num_guests = models.PositiveIntegerField(default=2) 
    price_usd = models.DecimalField(max_digits=6, decimal_places=2) 
    breakfast_included = models.BooleanField(default=False) 
    sea_view = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hotel.name} | {self.start_date} - {self.end_date} | {self.price_usd}$ for {self.num_guests} guests"

    class Meta:
        ordering = ['start_date']


class Tour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_people = models.PositiveIntegerField()
    has_kids = models.BooleanField(default=False)
    num_days = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"جولة {self.id} للمستخدم {self.user.username}"
    
    

class TourRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)

class Meta:
        unique_together = ('user', 'tour')  # تقييم واحد فقط لكل مستخدم
        def __str__(self):
         return f"{self.user.username} ⭐ {self.rating} - جولة {self.tour.id}"

class FavoriteTour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tour')  # كل جولة مرة واحدة فقط بالمفضلة

class Car(models.Model):
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=100, choices=[
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('van', 'Van'),
        ('truck', 'Truck'),
        ('convertible', 'Convertible'),
    ])
    fuel_type = models.CharField(max_length=50, choices=[
        ('gasoline', 'بنزين'),
        ('diesel', 'ديزل'),
        ('electric', 'كهرباء'),
        ('hybrid', 'هايبرد'),
    ])
    transmission = models.CharField(max_length=50, choices=[
        ('manual', 'عادي'),
        ('automatic', 'أوتوماتيك'),
    ])
    model_year = models.PositiveIntegerField()
    image = models.URLField(blank=True, help_text="رابط صورة للسيارة")

    def __str__(self):
        return f"{self.name} ({self.model_year})"


class CarPrice(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='prices')
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.car.name} | {self.start_date} - {self.end_date} | {self.price_per_day}$/يوم"

    class Meta:
        ordering = ['start_date']


class TourDay(models.Model):
    tour = models.ForeignKey(Tour, related_name='tour_days', on_delete=models.CASCADE)
    day_number = models.PositiveIntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    journey = models.ForeignKey('Journey', on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.CharField(max_length=200, blank=True)
    note = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
   
    def __str__(self):
        return f"يوم {self.day_number} من الجولة {self.tour.id}"


class DailyPlan(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='daily_plans')
    day_number = models.PositiveIntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Day {self.day_number} of Tour {self.tour.id}"
    
class Journey(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="مثال: 🏕🌲🌴")

    def __str__(self):
        return f"{self.name} {self.icon}"
    
class JourneyPrice(models.Model):
    journey = models.ForeignKey('Journey', on_delete=models.CASCADE, related_name='prices')
    start_date = models.DateField()
    end_date = models.DateField()
    price_usd = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.journey.name} | {self.start_date} - {self.end_date} | ${self.price_usd}"


    