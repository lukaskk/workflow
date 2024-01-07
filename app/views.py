from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  Task
from .forms import  TaskForm
from django.contrib.auth import get_user_model
from django.http import FileResponse
import imaplib
import email
import openpyxl
from email import policy
from django.core.files.base import ContentFile

from .forms import UploadFileForm
from .models import Order
from django.shortcuts import render
from .models import CustomUser
from .forms import CustomUserCreationForm


# Używaj niestandardowego modelu użytkownika


from django.views.generic import ListView, CreateView, UpdateView

from .forms import CustomUserForm

def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Załóżmy, że user_list to URL do listy użytkowników
    else:
        form = CustomUserCreationForm()
    return render(request, 'add_user.html', {'form': form})

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserForm(instance=user)

    return render(request, 'edit_user.html', {'form': form})


def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')

    return render(request, 'delete_user.html', {'user': user})



# Lista klientów

# views.py
def filter_orders_by_name(request, name):
    orders = Order.objects.filter(name=name)  # Filtruj zlecenia według nazwy
    total_orders = orders.count()
    completed_orders = orders.filter(status='Completed').count()

    if total_orders > 0:
        progress_percentage = (completed_orders / total_orders) * 100
    else:
        progress_percentage = 0

    context = {
        'orders': orders,
        'filter_name': name,
        'progress_percentage': progress_percentage,
    }

    return render(request, 'orders_filtered_list.html', context)



def home(request):
    return render(request, 'home.html')

@login_required


def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})





@login_required  # Upewniamy się, że tylko zalogowani użytkownicy mają dostęp


def task_list(request):
    user = request.user
    tasks = Task.objects.none()  # Domyślnie nie pokazujemy żadnych zadań

    if user.is_authenticated:
        # Sprawdzamy, czy użytkownik jest administratorem lub pracownikiem
        if user.is_administrator() or user.is_employee():
            tasks = Task.objects.all()  # Administrator i pracownik widzą wszystkie zadania
        elif user.is_client():
            # Klient widzi zadania przypisane do jego firmy
            tasks = Task.objects.filter(client_name=user.company)

    return render(request, 'task_list.html', {'tasks': tasks})



@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'create_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'delete_task.html', {'task': task})




import datetime
import random



def generate_unique_id():
    # Używamy czasu uniksowego (timestamp) do uzyskania unikalnej wartości
    timestamp = int(datetime.datetime.now().timestamp())
    
    # Generujemy losową liczbę i dodajemy ją do timestamp
    random_number = random.randint(0, 9999)
    unique_id = (timestamp + random_number) % 900000000  # Utrzymanie 6 cyfr

    return str(unique_id).zfill(6)  # Dodajemy zera na początku, jeśli jest krótszy niż 6 cyfr





def upload_excel(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            for row in sheet.iter_rows(min_row=2):
                # Generowanie unikatowego ID
                order_id = row[0].value
                name = row[1].value
                street = row[2].value
                city = row[3].value
                postal_code = row[4].value
                client = row[5].value
                execution_date = row[6].value
                time_spent = row[7].value

                Order.objects.create(
                    order_id=order_id,
                    name=name,
                    street=street,
                    city=city,
                    postal_code=postal_code,
                    client=client,
                    execution_date=execution_date,
                    time_spent=time_spent
                )

            return redirect('order_list')

    else:
        form = UploadFileForm()

    return render(request, 'upload_excel.html', {'form': form})



def order_list(request):
    orders = Order.objects.all()  # Pobranie wszystkich zleceń
    return render(request, 'order_list.html', {'orders': orders})

from app.forms import OrderForm # Zakładając, że masz formularz OrderForm

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')  # Przekierowanie do listy zleceń
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})

def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'edit_order.html', {'form': form})

def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'delete_order.html', {'order': order})


from .models import  OrderPhoto
from .forms import EditOrderForm, OrderPhotoForm

def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = EditOrderForm(request.POST, instance=order)
        photo_form = OrderPhotoForm(request.POST, request.FILES)
        if form.is_valid() and photo_form.is_valid():
            form.save()
            photo_instance = photo_form.save(commit=False)
            photo_instance.order = order
            photo_instance.save()
            return redirect('order_list')
    else:
        form = EditOrderForm(instance=order)
        photo_form = OrderPhotoForm()

    return render(request, 'edit_order.html', {'form': form, 'photo_form': photo_form, 'order': order})


from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from app.models import Order
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Rejestruj czcionkę
pdfmetrics.registerFont(TTFont('Lato', 'static/fonts/Afacad-VariableFont_wght.ttf'))
import io

def generate_pdf(request, order_id):
    order = Order.objects.get(order_id=order_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order.order_id}.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Lato", 16)

    # Wymiary strony A4
    page_width, page_height = A4

    # Zaczynamy od góry strony
    y_position = page_height - 30

    # Dodajemy informacje o zleceniu
    fields = [
        f"Order ID: {order.order_id}",
        f"Name: {order.name}",
        f"Street: {order.street}",
        f"City: {order.city}",
        f"Postal Code: {order.postal_code}",
        f"Client: {order.client}",
        f"Execution Date: {order.execution_date.strftime('%Y-%m-%d') if order.execution_date else 'N/A'}",
        f"Assigned User: {order.assigned_user.username if order.assigned_user else 'N/A'}",
        f"Status: {order.get_status_display()}",
    ]

    for field in fields:
        p.drawString(50, y_position, field)
        y_position -= 20

    # Dodajemy zdjęcia
    photos = order.photos.all()
    for photo in photos:
        if y_position < 150:  # Jeśli jesteśmy blisko końca strony, zaczynamy nową
            p.showPage()
            y_position = page_height - 30

        try:
            img_path = photo.photo.path
            img = ImageReader(img_path)
            p.drawImage(img, 50, y_position - 300, width=400, height=300, preserveAspectRatio=True)
            y_position -= 260  # Zmniejszamy y o wysokość obrazu plus trochę miejsca
        except IOError:
            print("Nie można załadować obrazu: ", img_path)

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='application/pdf')


def download_photo(request, photo_id):
    photo = OrderPhoto.objects.get(id=photo_id)
    # Upewnij się, że ścieżka do pliku zdjęcia jest poprawna
    file_path = photo.photo.path
    return FileResponse(open(file_path, 'rb'))

# views.py






# Dane do logowania do serwera IMAP
IMAP_SERVER = 'lukaskk.nazwa.pl'
EMAIL_ACCOUNT = 'raport@jklm.eu'
EMAIL_PASSWORD = 'rt4523aaQQ@@!!'
IMAP_PORT = 993 



def check_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select('inbox')

    result, data = mail.search(None, 'ALL')
    mail_ids = data[0].split()

    for mail_id in mail_ids:
        result, data = mail.fetch(mail_id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email, policy=policy.default)

        # Analiza tytułu wiadomości e-mail
        email_subject = email_message['subject']
        order_id = email_subject
       
        if order_id:
            try:
                order = Order.objects.get(order_id=order_id)
                update_order_with_email(order, email_message)
                # Oznaczanie wiadomości jako usuniętej
                mail.store(mail_id, '+FLAGS', '\\Deleted')
            except Order.DoesNotExist:
                print(f"Order with ID {order_id} does not exist.")
        else:
            print("Order ID not found in email subject.")

    # Usunięcie oznaczonych wiadomości
    mail.expunge()
    mail.close()
    mail.logout()

def extract_order_id(subject):
    if subject and subject.startswith('Order ID: '):
        return subject.split('Order ID: ')[1].strip()
    return None

def update_order_with_email(order, email_message):
    order.status = 'Completed'
    order.execution_date = datetime.datetime.now()  # Ustawienie bieżącej daty jako daty wykonania
    order.save()

    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        file_data = part.get_payload(decode=True)
        file_name = part.get_filename()

        if file_data and file_name:
            photo = OrderPhoto(order=order)
            photo.photo.save(file_name, ContentFile(file_data), save=True)

def run():
    check_emails()

if __name__ == '__main__':
    run()

    
    
from django.urls import reverse
 # Zaimportuj funkcję, którą chcesz wywołać

def update_database(request):
    check_emails()
    # Przekierowanie z powrotem na stronę, z której przycisk został kliknięty
    return redirect(reverse('home'))    



def delete_photo(request, photo_id):
    photo = get_object_or_404(OrderPhoto, pk=photo_id)
    order_id = photo.order.id
    photo.delete()
    return redirect('edit_order', pk=order_id)





