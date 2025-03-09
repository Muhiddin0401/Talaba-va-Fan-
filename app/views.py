from tempfile import template

from django.urls import reverse_lazy
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from .form import FanForm, TalabaForm
import qrcode


# def asosiy(request):
#     fanlar = Fan.objects.all()
#     talabalar = Talaba.objects.all()
#
#     context = {
#         'Fan': fanlar,
#         'Talaba': talabalar,
#     }
#
#     return render(request, "Asosiy.html", context)

class asosiy(ListView):
    model = Talaba
    template_name = 'Asosiy.html'
    context_object_name = 'Talaba'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Fan'] = Fan.objects.all()
        return context

# def Fan_talabasi(request, fan_id):
#     fan = get_object_or_404(Fan, id = fan_id)
#     talabalar = Talaba.objects.filter(fan=fan)
#     context = {
#         'fan': fan,
#         'talaba': talabalar,
#     }
#
#     return render(request, "Fan_talabasi.html", context)

class Fan_talabasi(ListView):
    model = Talaba
    template_name = 'Fan_talabasi.html'
    context_object_name = 'Talaba'

    def get_queryset(self):
        fan = get_object_or_404(Fan, id = self.kwargs['fan_id'])

        return Talaba.objects.filter(fan=fan)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fan'] = get_object_or_404(Fan, id = self.kwargs['fan_id'])
        context['Fan'] = Fan.objects.all()
        return context

# def Talaba_haqida(request, talaba_id):
#     talaba = get_object_or_404(Talaba, id=talaba_id)
#     context = {'talaba': talaba}
#     return render(request, "Talaba.html", context)

class Talaba_haqida(DetailView):
    model = Talaba
    template_name = 'Talaba.html'
    context_object_name = 'talaba'
    pk_url_kwarg = "talaba_id"

# def add_talaba(request):
#     if request.method == 'POST':
#         form = TalabaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('asosiy')
#     else:
#         form = TalabaForm()
#     context = {'form': form}
#     return render(request, "add_talaba.html", context)

class add_talaba(CreateView):
    model = Talaba
    template_name = 'add_talaba.html'
    form_class = TalabaForm
    success_url = reverse_lazy('asosiy')

# def del_talaba(request, talaba_id):
#     talaba = get_object_or_404(Talaba, id=talaba_id)
#     if request.method == 'POST':
#         talaba.delete()
#         messages.success(request, f"{talaba.ism_fam} muvaffaqiyatli o‘chirildi!")
#         return redirect('asosiy')
#     return redirect('asosiy')

class del_talaba(DeleteView):
    model = Talaba
    success_url = reverse_lazy('asosiy')

# def upd_talaba(request, talaba_id):
#     talaba = get_object_or_404(Talaba, id=talaba_id)
#     if request.method == 'POST':
#         form = TalabaForm(request.POST, instance=talaba)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"{talaba.ism_fam} muvaffaqiyatli yangilandi!")
#             return redirect('asosiy')
#     else:
#         form = TalabaForm(instance=talaba)
#     context = {'form': form, 'talaba': talaba}
#     return render(request, 'upd_fan.html', context)

class upd_talaba(UpdateView):
    model = Talaba
    form_class = TalabaForm
    template_name = 'upd_talaba.html'
    success_url = reverse_lazy(asosiy)

# def add_fan(request):
#     if request.method == 'POST':
#         form = FanForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Fan muvaffaqiyatli qo'shildi!")
#             return redirect('asosiy')
#     else:
#         form = FanForm()
#     context = {'form': form}
#     return render(request, 'add_fan.html', context)

class add_fan(CreateView):
    model = Fan
    template_name = 'add_fan.html'
    form_class = FanForm
    success_url = reverse_lazy('asosiy')

# def del_fan(request, fan_id):
#     fan = get_object_or_404(Fan, id=fan_id)
#     if request.method == 'POST':
#         fan.delete()
#         messages.success(request, f"{fan.nom} fani muvaffaqiyatli o‘chirildi!")
#         return redirect('asosiy')
#     return redirect('asosiy')

class del_fan(DeleteView):
    model = Fan
    success_url = reverse_lazy('asosiy')

# def upd_fan(request, fan_id):
#     fan = get_object_or_404(Fan, id=fan_id)
#     if request.method == 'POST':
#         form = FanForm(request.POST, instance=fan)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Fan muvaffaqiyatli yangilandi!")
#             return redirect('asosiy')
#     else:
#         form = FanForm(instance=fan)
#     context = {'form': form, 'fan': fan}
#     return render(request, 'upd_fan.html', context)

class upd_fan(UpdateView):
    model = Fan
    form_class = FanForm
    template_name = 'upd_fan.html'
    success_url = reverse_lazy('asosiy')

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

    p.drawImage("qr_code.png", 400, 650, width=100, height=100)

    # PDF ni tugatish
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{talaba.ism_fam}_malumot.pdf"'
    return response