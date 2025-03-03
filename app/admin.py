from django.contrib import admin
from .models import Fan, Talaba

class TalabaAdmin(admin.ModelAdmin):
    list_display = ('id', 'ism_fam', 'manzil', 'fan')
    search_fields = ('ism_fam',)
    list_display_links = ('ism_fam',)

class FanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom',)
    search_fields = ('nom',)
    list_display_links = ('nom',)

    # def get_talaba(self, obj):
    #     return obj.talaba.ism_fam

admin.site.register(Talaba, TalabaAdmin)
admin.site.register(Fan, FanAdmin)