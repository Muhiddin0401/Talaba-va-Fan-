from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.contrib.auth import authenticate, login, logout
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from .form import FanForm, TalabaForm, UserLoginForm  # forms.py dan to‘g‘ri import
import qrcode
from django.db.models import Q
import tempfile

def asosiy(request):
    query = request.GET.get('q', '')
    if query:
        fanlar = Fan.objects.filter(nom__icontains=query)
        talabalar = Talaba.objects.filter(ism_fam__icontains=query)
    else:
        fanlar = Fan.objects.all()
        talabalar = Talaba.objects.all()

    context = {
        'Fan': fanlar,
        'Talaba': talabalar,
    }

    return render(request, "Asosiy.html", context)

def Fan_talabasi(request, fan_id):
    fan = get_object_or_404(Fan, id=fan_id)
    talabalar = Talaba.objects.filter(fan=fan)
    context = {
        'fan': fan,
        'talaba': talabalar,
    }

    return render(request, "Fan_talabasi.html", context)

def Talaba_haqida(request, talaba_id):
    talaba = get_object_or_404(Talaba, id=talaba_id)
    context = {'talaba': talaba}
    return render(request, "Talaba.html", context)

def add_talaba(request):
    if request.method == 'POST':
        form = TalabaForm(request.POST, request.FILES)  # Fayl yuklash uchun request.FILES qo‘shildi
        if form.is_valid():
            form.save()
            return redirect('asosiy')
    else:
        form = TalabaForm()
    context = {'form': form}
    return render(request, "add_talaba.html", context)

def del_talaba(request, talaba_id):
    talaba = get_object_or_404(Talaba, id=talaba_id)
    if request.method == 'POST':
        talaba.delete()
        messages.success(request, f"{talaba.ism_fam} muvaffaqiyatli o‘chirildi!")
        return redirect('asosiy')
    return redirect('asosiy')

def upd_talaba(request, talaba_id):
    talaba = get_object_or_404(Talaba, id=talaba_id)
    if request.method == 'POST':
        form = TalabaForm(request.POST, request.FILES, instance=talaba)
        if form.is_valid():
            form.save()
            messages.success(request, f"{talaba.ism_fam} muvaffaqiyatli yangilandi!")
            return redirect('asosiy')
    else:
        form = TalabaForm(instance=talaba)
    context = {'form': form, 'talaba': talaba}
    return render(request, 'upd_talaba.html', context)

def add_fan(request):
    if request.method == 'POST':
        form = FanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fan muvaffaqiyatli qo'shildi!")
            return redirect('asosiy')
    else:
        form = FanForm()
    context = {'form': form}
    return render(request, 'add_fan.html', context)

def del_fan(request, fan_id):
    fan = get_object_or_404(Fan, id=fan_id)
    if request.method == 'POST':
        fan.delete()
        messages.success(request, f"{fan.nom} fani muvaffaqiyatli o‘chirildi!")
        return redirect('asosiy')
    return redirect('asosiy')

def upd_fan(request, fan_id):
    fan = get_object_or_404(Fan, id=fan_id)
    if request.method == 'POST':
        form = FanForm(request.POST, instance=fan)
        if form.is_valid():
            form.save()
            messages.success(request, "Fan muvaffaqiyatli yangilandi!")
            return redirect('asosiy')
    else:
        form = FanForm(instance=fan)
    context = {'form': form, 'fan': fan}
    return render(request, 'upd_fan.html', context)

def download_talaba_pdf(request, talaba_id):
    talaba = get_object_or_404(Talaba, id=talaba_id)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f"Talaba: {talaba.ism_fam}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Sharf: {talaba.sharf}")
    p.drawString(100, 710, f"Telefon: {talaba.tel_raqam or 'Yo‘q'}")
    p.drawString(100, 690, f"Manzil: {talaba.manzil}")
    p.drawString(100, 670, f"Fan: {talaba.fan.nom if talaba.fan else 'Tanlanmagan'}")

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data("https://najottalim.uz/")
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')

    # QR kodni diskka saqlash o‘rniga to‘g‘ridan-to‘g‘ri foydalanish
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    # Temporary fayl yaratish
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file.write(qr_buffer.read())
        temp_file_path = temp_file.name

    p.drawImage(temp_file_path, 400, 650, width=100, height=100)

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{talaba.ism_fam}_malumot.pdf"'
    return response

def login_view(request):
    # Har safar login formasini ko‘rsatish uchun avtomatik yo‘naltirishni o‘chirish
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=phone, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin')
                else:
                    return redirect('user')
            else:
                messages.error(request, "Telefon raqami yoki parol xato!!!")
        else:
            messages.error(request, "Forma ma’lumotlari noto‘g‘ri!")
    else:
        form = UserLoginForm()
        # Agar foydalanuvchi tizimga kirgan bo‘lsa, uni logout qilish yoki login formasini ko‘rsatish
        if request.user.is_authenticated:
            logout(request)  # Foydalanuvchini chiqarib yuborish

    return render(request, 'login.html', {'form': form})

def admin_panel(request):
    return render(request, 'Asosiy.html')  # Yoki Asosiy_panel.html

def staff_panel(request):
    return render(request, 'add_fan.html')

def user_panel(request):
    return render(request, 'upd_fan.html')