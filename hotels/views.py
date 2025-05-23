from django.shortcuts import render, redirect, get_object_or_404
from .models import  Hotel, HotelPrice, Tour, City, TourDay, TourRating, FavoriteTour, Journey, Car, CarPrice, JourneyPrice 
from .forms import HotelForm, HotelPriceForm, TourForm, JourneyForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta 
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Prefetch, Q, Count, Sum, Avg, Min, Max
from django.utils.timezone import now
from calendar import monthrange





@login_required
def admin_dashboard(request):
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())# الاثنين
    start_of_month = today.replace(day=1)


    tours = Tour.objects.all()
    total_tours = tours.count()
    today_tours = tours.filter(created_at__date=today).count()
    week_tours = tours.filter(created_at__date__gte=start_of_week).count()
    month_tours = tours.filter(created_at__date__gte=start_of_month).count()

    total_price_month = tours.filter(created_at__date__gte=start_of_month).aggregate(total=Sum('total_price'))['total'] or 0
    top_hotels = TourDay.objects.values('hotel__name').annotate(count=Count('id')).order_by('-count')[:5]
    top_users = Tour.objects.values('user__username').annotate(count=Count('id')).order_by('-count')[:5]
# عدد الجولات لكل فترة
    tours_today = Tour.objects.filter(created_at__date=today)
    tours_week = Tour.objects.filter(created_at__date__gte=start_of_week)
    tours_month = Tour.objects.filter(created_at__date__gte=start_of_month)

    # أكثر المستخدمين نشاطاً حسب كل فترة
    active_users_today = tours_today.values('user__username').annotate(count=Count('id')).order_by('-count')[:5]
    active_users_week = tours_week.values('user__username').annotate(count=Count('id')).order_by('-count')[:5]
    active_users_month = tours_month.values('user__username').annotate(count=Count('id')).order_by('-count')[:5]

    # مجموع الأرباح
    total_today = tours_today.aggregate(total=Sum('total_price'))['total'] or 0
    total_week = tours_week.aggregate(total=Sum('total_price'))['total'] or 0
    total_month = tours_month.aggregate(total=Sum('total_price'))['total'] or 0

    return render(request, 'hotels/admin_dashboard.html', {


        'total_tours': total_tours,
        'today_tours': today_tours,
        'week_tours': week_tours,
        'month_tours': month_tours,
        'total_price_month': total_price_month,
        'top_hotels': top_hotels,
        'top_users': top_users,
        'active_users_today': active_users_today,
        'active_users_week': active_users_week,
        'active_users_month': active_users_month,
        'total_today': total_today,
        'total_week': total_week,
        'total_month': total_month,
    })

@login_required
def user_activity_view(request, username):
    user = get_object_or_404(User, username=username)
    now = timezone.now().date()

    today = now
    start_week = now - timedelta(days=now.weekday())
    start_month = now.replace(day=1)

    tours = Tour.objects.filter(user=user)

    stats = {
        'total_tours': tours.count(),
        'tours_today': tours.filter(created_at__date=today).count(),
        'tours_this_week': tours.filter(created_at__date__gte=start_week).count(),
        'tours_this_month': tours.filter(created_at__date__gte=start_month).count(),

        'avg_rating': TourRating.objects.filter(user=user).aggregate(avg=Avg('rating'))['avg'] or 0,
        'total_spent': tours.aggregate(total=Sum('total_price'))['total'] or 0,

        'cheapest_tour': tours.order_by('total_price').first(),
        'most_expensive_tour': tours.order_by('-total_price').first(),
    }

    return render(request, 'hotels/user_activity.html', {
    'profile_user': user,
    'today_count': stats['tours_today'],
    'week_count': stats['tours_this_week'],
    'month_count': stats['tours_this_month'],
    'total_count': stats['total_tours'],
    'average_rating': stats['avg_rating'],
    'total_spent': stats['total_spent'],
    'cheapest_tour': stats['cheapest_tour'],
    'most_expensive_tour': stats['most_expensive_tour'],
})

def home_view(request):
    return render(request, 'hotels/home.html')

# عرض قائمة الفنادق
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/hotel_list.html', {'hotels': hotels})

# إضافة فندق
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm()
    return render(request, 'hotels/add_hotel.html', {'form': form})

# إضافة سعر لفندق
def add_price(request):
    if request.method == 'POST':
        form = HotelPriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelPriceForm()
    return render(request, 'hotels/add_price.html', {'form': form})

def hotel_list_view(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/hotel_list.html', {'hotels': hotels})


#اضافة جولة 
@login_required
def create_tour(request):
    
    user_tours = Tour.objects.filter(user=request.user).order_by('-created_at')
    tours = Tour.objects.all().order_by('-created_at')
    user_ratings = {r.tour.id: r.rating for r in TourRating.objects.filter(user=request.user)}
    user_favorites = set(FavoriteTour.objects.filter(user=request.user).values_list('tour_id', flat=True))


    sort = request.GET.get('sort', 'newest')  # القيمة الافتراضية
# ✅ تطبيق الترتيب
    if sort == 'oldest':
        tours = Tour.objects.all().order_by('created_at')
    elif sort == 'expensive':
        tours = Tour.objects.all().order_by('-total_price')
    elif sort == 'cheapest':
        tours = Tour.objects.all().order_by('total_price')
    else:  # newest
     tours = Tour.objects.all().order_by('-created_at')

    

    if request.method == 'POST':
        num_people = int(request.POST.get('num_people'))
        has_kids = 'has_kids' in request.POST
        num_days = int(request.POST.get('num_days'))
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        request.session['tour_data'] = {
            'num_people': num_people,
            'has_kids': has_kids,
            'num_days': num_days,
            'start_date': start_date,
            'end_date': end_date,
        }
        return redirect('select_hotels_and_trips')
     # تقييمات المستخدم الحالية

    return render(request, 'hotels/create_tour.html', {
        'user_tours': user_tours,
        'tours': tours,
        'user_ratings': user_ratings,
        'user_favorites': user_favorites,
        'star_range' : [1, 2 , 3 , 4 , 5],

    })


@login_required
def start_tour(request):
    if request.method == 'POST':
        num_people = int(request.POST.get('num_people'))
        has_kids = 'has_kids' in request.POST
        num_days = int(request.POST.get('num_days'))
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        request.session['tour_data'] = {
            'num_people': num_people,
            'has_kids': has_kids,
            'num_days': num_days,
            'start_date': start_date,
            'end_date': end_date,
        }
        return redirect('select_hotels_and_trips')

    return render(request, 'hotels/start_tour.html')



#خيارات 
def select_hotels_and_trips(request):
    tour_data = request.session.get('tour_data')

    if not tour_data:
        messages.error(request, "الرجاء إدخال تفاصيل الرحلة أولاً.")
        return redirect('create_tour')

    num_days = int(tour_data['num_days'])
    days_list = range(1, num_days + 1)  # ✅ توليد الأيام في البايثون

    if request.method == 'POST':
        daily_plan = []
        for day in range(1, num_days + 1):
            hotel_id = request.POST.get(f'hotel_{day}')
            trip_description = request.POST.get(f'description_{day}')
            
            journey_id = request.POST.get(f'journey_{day}')
            price_id = request.POST.get(f'price_{day}')
            car_id = request.POST.get(f'car_{day}')
            car_price_id = request.POST.get(f'car_price_{day}')
            journey_price_id = request.POST.get(f'journey_price_{day}')
            

            hotel = Hotel.objects.get(id=hotel_id) if hotel_id else None
            daily_plan.append({
                'day': day,
                'hotel': hotel.name if hotel else 'لا يوجد',
                'description': trip_description,
                'hotel_id': hotel_id,
                'hotel_image': hotel.image_main if hotel else '',
                'hotel_url': hotel.url if hotel else '',
                'journey_id': journey_id,
                'activity': trip_description,
                'note': '',
                'price_id': price_id,
                'car_id': car_id,
                'car_price_id': car_price_id,
                'journey_price_id': journey_price_id,

            }) 

        # نحفظ الخطة للعرض النهائي
        request.session['tour_days'] = daily_plan
        return redirect('tour_summary')
    # ✅ نجيب الأسعار مع الفنادق
    journey_prices = JourneyPrice.objects.select_related('journey').all()
    cars = Car.objects.all() 
    car_prices = CarPrice.objects.select_related('car').all()
    journeys = Journey.objects.all()  
    hotels = Hotel.objects.all()
    prices = HotelPrice.objects.select_related('hotel').all()
    return render(request, 'hotels/select_plan.html', {
        'days_list': days_list,
        'num_days': num_days,
        'hotels': hotels,
        'journeys': journeys,
        'prices': prices,
        'cars': cars,
        'car_prices': car_prices,
        'journey_prices': journey_prices,

    })


  

# الملخص
@login_required
def tour_summary(request):
    tour_data = request.session.get('tour_data')
    tour_days = request.session.get('tour_days')


    if not tour_data or not tour_days:
        return render(request, 'hotels/invalid_tour.html')  # ✅ عرض صفحة خطأ
 # جمع البيانات
    hotels = {hotel.id: hotel for hotel in Hotel.objects.all()}
    hotel_prices = {p.id: p for p in HotelPrice.objects.select_related('hotel')}
    car_prices = {cp.id: cp for cp in CarPrice.objects.select_related('car')}
    journey_prices = {jp.id: jp for jp in JourneyPrice.objects.select_related('journey')}
    journeys = {j.id: j for j in Journey.objects.all()}

    total_price = 0
    summary = []

    for day in tour_days:
        hotel = hotels.get(int(day['hotel_id'])) if day.get('hotel_id') else None
        hotel_price = hotel_prices.get(int(day['price_id'])) if day.get('price_id') else None
        journey = journeys.get(int(day['journey_id'])) if day.get('journey_id') else None
        journey_price = journey_prices.get(int(day.get('journey_price_id'))) if day.get('journey_price_id') else None
        car_price = car_prices.get(int(day.get('car_price_id'))) if day.get('car_price_id') else None

        hotel_price_usd = float(hotel_price.price_usd) if hotel_price else 0
        journey_price_usd = float(journey_price.price_usd) if journey_price else 0
        car_price_usd = float(car_price.price_per_day) if car_price else 0

        day_total = hotel_price_usd + journey_price_usd + car_price_usd
        total_price += day_total

        summary.append({
            'day': day['day'],
            'hotel': hotel,
            'hotel_image': day.get('hotel_image'),
            'hotel_url': day.get('hotel_url'),
            'activity': day['activity'],
            'note': day['note'],
            'price': day_total,
            'journey': journey,
            'car_price': car_price_usd,
            'journey_price': journey_price_usd,
        })

    # حفظ الجولة
    if request.method == 'POST':
        tour = Tour.objects.create(
            user=request.user,
            num_people=tour_data['num_people'],
            has_kids=tour_data.get('has_kids', False),
            num_days=tour_data['num_days'],
            start_date=tour_data['start_date'],
            end_date=tour_data['end_date'],
            total_price=total_price
        )

        for day in summary:
            TourDay.objects.create(
                tour=tour,
                day_number=day['day'],
                hotel=day['hotel'],
                activity=day['activity'],
                journey=day['journey'],
                note=day['note'],
                price=day['price']
            )

        return redirect('tour_saved')

    return render(request, 'hotels/tour_summary.html', {
        'summary': summary,
        'total_price': total_price,
        'user': request.user,
        'num_people': tour_data['num_people'],
        'start_date': tour_data['start_date'],
        'end_date': tour_data['end_date'],
    })

@login_required
def manage_journeys(request):
    if request.method == 'POST':
        form = JourneyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت إضافة الرحلة بنجاح!")
            return redirect('manage_journeys')
    else:
        form = JourneyForm()

    journeys = Journey.objects.all()
    return render(request, 'hotels/manage_journeys.html', {
        'form': form,
        'journeys': journeys
    })





# rate
@login_required
def rate_tour(request, tour_id):
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        tour = get_object_or_404(Tour, id=tour_id)

        if rating_value:
            
            TourRating.objects.update_or_create(
                tour=tour,
                user=request.user,
                defaults={'rating': int(rating_value)}
            )
    return redirect('create_tour')

@login_required
def toggle_favorite(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    favorite, created = FavoriteTour.objects.get_or_create(user=request.user, tour=tour)
    if not created:
        favorite.delete()
    return redirect('create_tour')

@login_required
def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.user != tour.user and not request.user.is_superuser:
        messages.error(request, "ليس لديك صلاحية تعديل هذه الجولة.")
        return redirect('create_tour')

    tour_days = TourDay.objects.filter(tour=tour).select_related('hotel', 'journey')
    hotels = Hotel.objects.all()
    journeys = Journey.objects.all()

    if request.method == 'POST':
        # تحديث بيانات الجولة الأساسية
        tour.num_people = int(request.POST.get('num_people'))
        tour.has_kids = 'has_kids' in request.POST
        tour.num_days = int(request.POST.get('num_days'))
        tour.start_date = request.POST.get('start_date')
        tour.end_date = request.POST.get('end_date')
        tour.save()

        # تحديث بيانات الأيام
        for day in tour_days:
            hotel_id = request.POST.get(f'hotel_{day.id}')
            journey_id = request.POST.get(f'journey_{day.id}')
            activity = request.POST.get(f'activity_{day.id}')
            note = request.POST.get(f'note_{day.id}')

            # تحديث البيانات فقط إذا كانت صحيحة
            if hotel_id:
                try:
                    day.hotel = Hotel.objects.get(id=int(hotel_id))
                except Hotel.DoesNotExist:
                    pass

            if journey_id:
                try:
                    day.journey = Journey.objects.get(id=int(journey_id))
                except Journey.DoesNotExist:
                    day.journey = None
            else:
                day.journey = None

            day.activity = activity
            day.note = note
            day.save()

        messages.success(request, "✅ تم تعديل الجولة وتفاصيل الأيام بنجاح.")
        return redirect('view_tour_detail', tour_id=tour.id)

    return render(request, 'hotels/edit_tour.html', {
        'tour': tour,
        'tour_days': tour_days,
        'hotels': hotels,
        'journeys': journeys
    })




@login_required
def delete_tour(request, tour_id):
    tour = Tour.objects.get(id=tour_id)
    if request.user == tour.user or request.user.is_superuser:
        tour.delete()
    return redirect('create_tour')



@login_required
def view_tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    tour_days = TourDay.objects.filter(tour=tour).select_related('hotel', 'hotel__city')
    return render(request, 'hotels/view_tour_detail.html', {
        'tour': tour,
        'tour_days': tour_days
    })



# جولاتي
@login_required
def my_tours(request):
    user = request.user
    tours = Tour.objects.filter(user=user).order_by('-created_at')
    return render(request, 'hotels/my_tours.html', {'tours': tours})
#حذف جولتي
@login_required
def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.user != tour.user and not request.user.is_superuser:
        messages.error(request, "ليس لديك صلاحية حذف هذه الجولة.")
        return redirect('my_tours')

    tour.delete()
    messages.success(request, "تم حذف الجولة بنجاح.")
    return redirect('my_tours')
#بروفايل الشخص
def user_profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    tours = Tour.objects.filter(user=user_profile).order_by('-created_at')
    total_spent = tours.aggregate(total=Sum('total_price'))['total'] or 0


    return render(request, 'hotels/user_profile.html', {
        'profile_user': user_profile,
        'tours': tours,
        'total_spent': total_spent

    })

@login_required
def profile_view(request, username):
    user = User.objects.get(username=username)
    tours = Tour.objects.filter(user=user).order_by('-created_at')
    return render(request, 'hotels/profile.html', {
        'profile_user': user,
        'tours': tours
    })
def favorite_tours_view(request):
    favorites = FavoriteTour.objects.filter(user=request.user)
    tours = [fav.tour for fav in favorites]
    return render(request, 'hotels/favorite_tours.html', {'tours': tours})


def favorite_tours(request):
    favorites = request.user.favorite_tours.all()
    return render(request, 'hotels/favorite_tours.html', {
        'favorites': favorites
    })