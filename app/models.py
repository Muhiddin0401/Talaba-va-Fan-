from django.db import models

class Fan(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


class Talaba(models.Model):
    ism_fam = models.CharField(max_length=50)
    sharf = models.CharField(max_length=50)
    tel_raqam = models.CharField(max_length=13, blank=True, null=True)
    manzil = models.CharField(max_length=100)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, related_name="get_talaba", null=True, blank=True)
    views = models.IntegerField(default=0)
    fayl = models.FileField(upload_to='talaba_files/', null=True, blank=True)

    def __str__(self):
        return f"{self.ism_fam}"