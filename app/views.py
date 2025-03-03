from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from .form import FanForm, TalabaForm
import qrcode


def asosiy(request):
    fanlar = Fan.objects.all()
    talabalar = Talaba.objects.all()

    context = {
        'Fan': fanlar,
        'Talaba': talabalar,
    }

    return render(request, "Asosiy.html", context)

def Fan_talabasi(request, fan_id):
    fan = get_object_or_404(Fan, id = fan_id)
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
        form = TalabaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asosiy')
    else:
        form = TalabaForm()
    context = {'form': form}
    print("Context:", context)  # Terminalda context chiqadi
    return render(request, "add_talaba.html", context)

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

    qr_img.save("qr_code.png")

    p.drawImage("qr_code.png", 400, 650, width=100, height=100)  # QR kod joylashuvi

    # PDF ni tugatish
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{talaba.ism_fam}_malumot.pdf"'
    return response