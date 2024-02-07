from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .models import  Task


from bootstrap_datepicker_plus.widgets import DatePickerInput  # Importuj DatePickerInput

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from .models import  CustomUser

from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'job_title', 'company']
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'job_title', 'company')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['job_title'].choices = [
            ('', 'Wybierz stanowisko'),
            ('administrator', 'Administrator'),
            ('pracownik', 'Pracownik'),
            ('klient', 'Klient')
        ]
        
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'    
        
        
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'  # Wszystkie pola z modelu Order
        widgets = {
            'execution_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UploadFileForm(forms.Form):
    file = forms.FileField()
    photo = forms.ImageField(required=False)

from .models import OrderPhoto

 
        
class OrderPhotoForm(forms.ModelForm):
    class Meta:
        model = OrderPhoto
        fields = ['photo']

    def __init__(self, *args, **kwargs):
        super(OrderPhotoForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = False

from .models import Order

class EditOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'  # lub lista pól, które chcesz wyświetlić
        exclude = ['assigned_user']  # wyklucz pole 'assigned_user'
        widgets = {
            'execution_date': forms.DateInput(attrs={'type': 'date'}),
        }

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  # Załóżmy, że pole status jest zdefiniowane w modelu Order
        widgets = {
            'status': forms.Select(choices=Order.STATUS_CHOICES, attrs={'class': 'form-control'}),
        }   
        
        
        
from django import forms
from .models import Order

from django import forms
from .models import Order


class UpdateOrderForm(forms.Form):
    # Przykład, jak możesz zdefiniować pole formularza
    orders = forms.ModelMultipleChoiceField(queryset=Order.objects.none(), widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        orders_qs = kwargs.pop('orders_qs', Order.objects.none())
        super(UpdateOrderForm, self).__init__(*args, **kwargs)
        self.fields['orders'].queryset = orders_qs