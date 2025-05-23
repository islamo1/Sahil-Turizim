from django import forms
from .models import Hotel, HotelPrice, Tour, Journey 

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'phone', 'url', 'city', 'rating', 'view_type', 'room_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'view_type': forms.Select(attrs={'class': 'form-select'}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
        }

class HotelPriceForm(forms.ModelForm):
    class Meta:
        model = HotelPrice
        fields = ['hotel', 'start_date', 'end_date', 'num_guests', 'price_usd', 'breakfast_included', 'sea_view']
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'num_guests': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_usd': forms.NumberInput(attrs={'class': 'form-control'}),
            'breakfast_included': forms.CheckboxInput(),
            'sea_view': forms.CheckboxInput(),
        }
class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['num_people', 'has_kids', 'num_days', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }


        from .models import Journey

class JourneyForm(forms.ModelForm):
    class Meta:
        model = Journey
        fields = ['name', 'description', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
        }
