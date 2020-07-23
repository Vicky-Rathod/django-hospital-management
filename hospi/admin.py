from django.contrib import admin
from .models import Patient,Ipd,Rooms,TreatmentAdviced,TreatmentGiven,Discharge,Procedure,Investigation,DailyRound,Opd

admin.site.register(Opd)# Register your models here.

admin.site.register(Patient)
admin.site.register(Ipd)
admin.site.register(Rooms)
admin.site.register(TreatmentAdviced)
admin.site.register(TreatmentGiven)
admin.site.register(Investigation)
admin.site.register(DailyRound)
admin.site.register(Discharge)
admin.site.register(Procedure)
