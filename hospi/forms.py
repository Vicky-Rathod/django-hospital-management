from django.forms import ModelForm
from django import forms
from .models import Patient,Ipd,Discharge,TreatmentGiven,Investigation,Procedure,TreatmentAdviced,Opd, \
    DailyRound


class PatientForm(forms.ModelForm):
 
    
    class Meta:
        model = Patient
        fields = ['firstname','lastname','phone','alternate_phone','address','patient_id','gender']


class IpdForm(ModelForm):
  
    class Meta:
        model = Ipd

        fields = ['patient','ipd_id','reason_admission','provisional_diagnosis', 'rooms','date_of_admission','time_of_admission','weight','bill_responsible','bill_relation','consultant','condition_admission','secondary_consultant']
        widgets = {
            'date_of_admission': forms.DateInput(attrs={'class': 'datetimepicker3'}),
        }
    def __init__ (self, *args, **kwargs):
        available_rooms = kwargs.pop('available_rooms', None)
        super().__init__(*args, **kwargs)
        if available_rooms:
            print(self.fields['rooms'])
            self.fields['rooms'].queryset = available_rooms

class ProcedureForm(ModelForm):
    class Meta:
        model = Procedure
        fields = ['id','ipd','report','date','time']

class DischargeForm(ModelForm):
    class Meta :
        model = Discharge
        fields = ['ipd','final_diagnosis','type_discharge','discharge_condition','follow_up_advice','date_of_discharge','time_of_discharge']

class TreatmentGivenForm(ModelForm):
    class Meta:
        model = TreatmentGiven
        fields = '__all__'

class TreatmentAdvicedForm(ModelForm):
    class Meta:
        model = TreatmentAdviced
        fields = '__all__'

class InvestigationForm(ModelForm):
    class Meta:
        model = Investigation
        fields = ['name','id','report','date','ipd']

class DailyRoundForm(ModelForm):
    class Meta:
        model = DailyRound
        fields = '__all__'



class OpdForm(ModelForm):

    class Meta:
        model = Opd
        fields = '__all__'