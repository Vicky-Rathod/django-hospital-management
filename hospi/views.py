from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Patient, Ipd, Rooms, TreatmentGiven, Investigation, Procedure, TreatmentAdviced, DailyRound, \
    Discharge,DailyRound,Opd
from .forms import PatientForm, IpdForm, DischargeForm, TreatmentGivenForm, ProcedureForm, InvestigationForm, \
    TreatmentAdvicedForm,DailyRoundForm,OpdForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

@login_required
def index(request):
    patients = Patient.objects.all()
    return render(request, 'index.html', {'patients': patients})


@login_required
def new(request):
    if request.POST:
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/', messages.success(request, 'Patient is successfully created.', 'alert-success'))
        else:
            return HttpResponse(form.errors)
    else:
        form = PatientForm()
        return render(request, 'new.html', {'form': form})


@login_required
def ipd(request, patient_id):
    object = get_object_or_404(Patient, pk=patient_id)

    if request.method == "POST":
        formtwo = IpdForm(request.POST)

        if formtwo.is_valid():
            formtwo.save()

            return HttpResponseRedirect(reverse('ipdlist'))
        else:
            return HttpResponse(formtwo.errors.as_data())
    else:
        active_ipds = Ipd.objects.filter(discharge__isnull=True)
        occupied_rooms = active_ipds.values_list('rooms', flat=True).distinct()
        available_rooms = Rooms.objects.exclude(pk__in=occupied_rooms)
        formtwo = IpdForm(available_rooms=available_rooms)

    return render(request, 'newipd.html', {'object': object, 'form2': formtwo})


@login_required
def ipd_list(request):
    ipdlist = Ipd.objects.filter(discharge__isnull=True)
    return render(request, 'Ipdlist.html', {'ipd': ipdlist})



@login_required
def createappointment(request,patient_id):
    object =  get_object_or_404(Patient, pk=patient_id)
    if request.POST:
        form = OpdForm(request.POST)
        if form.is_valid():
            inves = form.save(commit=False)
            inves.object = object
            inves.save()
            return HttpResponseRedirect(reverse('opdlist'))
        else:
            return HttpResponse(form.errors)
    else:
        form = OpdForm()
        return render(request, 'appointment.html', {'form': form,'object': object,})


@login_required
def opd_list(request):
    object = Opd.objects.all()
    return render(request,'opdlist.html',{'object':object})
    
@login_required
def printopd(request,opd_id):
    object = get_object_or_404(Opd,pk=opd_id)
    return render(request,'opdprint.html',{'object':object})
@login_required
def create_patient_record(request):
    import pdb;
    pdb.set_trace()
    data = request.POST
    ipd_id = data.get('ipd_id')
    reason = data.get('admission_reason')
    provisional_diagnosis = data.get('provisional_diagnosis')
    object = get_object_or_404(Ipd, pk=ipd_id)
    object.admission_reason = reason
    object.provisional_diagnosis = provisional_diagnosis
    object.save()
    return render(request, 'dischargedetails.html')


@login_required
def discharge_detail(request, ipd_id):
    object = get_object_or_404(Ipd, pk=ipd_id)

    if request.method == "POST":
        investigation = InvestigationForm(request.POST)
        procedure = ProcedureForm(request.POST)
        treatmentgiven = TreatmentGivenForm(request.POST)
        treatmentadviced = TreatmentAdvicedForm(request.POST)
        dailyround = DailyRoundForm(request.POST)
        discharge = DischargeForm(request.POST)
        if investigation.is_valid():
            inves = investigation.save(commit=False)
            inves.object = object
            inves.save()
            return HttpResponseRedirect(request.path_info)


        elif procedure.is_valid():
            pro = procedure.save(commit=False)
            pro.object = object
            pro.save()
            return HttpResponseRedirect(request.path_info)

        elif treatmentgiven.is_valid():
            treatmentg = treatmentgiven.save(commit=False)
            treatmentg.object = object
            treatmentg.save()
            return HttpResponseRedirect(request.path_info)

        elif treatmentadviced.is_valid():
            treatmenta = treatmentadviced.save(commit=False)
            treatmenta.object = object
            treatmenta.save()
            return HttpResponseRedirect(request.path_info)

        elif dailyround.is_valid():
            dailyr = dailyround.save(commit=False)
            dailyr.object = object
            dailyr.save()
            return HttpResponseRedirect(request.path_info)

        elif discharge.is_valid():
            disch = discharge.save(commit=False)
            disch.object = object
            disch.save()
            return HttpResponseRedirect(reverse('discharge_list'))

        else:
            return HttpResponse(treatmentadviced.errors.as_data())

    else:
        treatmentgivenlist = object.treatmentgiven_set.all()
        treatmentadvicedlist = object.treatmentadviced_set.all()
        prolist = Procedure.objects.all().filter(ipd=ipd_id)
        procedure = ProcedureForm()
        investigationlist = Investigation.objects.all().filter(ipd=ipd_id)
        investigation = InvestigationForm()
        treatmentgiven = TreatmentGivenForm()
        treatmentadviced = TreatmentAdvicedForm()
        dailyround = DailyRoundForm()
        dailyroundlist = DailyRound.objects.all().filter(ipd=ipd_id)
        discharge = DischargeForm()

        return render(request, 'dischargedetails.html', {
            'object': object, 'investi': investigation, 'investilist': investigationlist,
            'procedure': procedure, 'prolist': prolist,
            'treatmentadviced': treatmentadviced, 'treatmentadvicedlist': treatmentadvicedlist,
            'treatmentgiven': treatmentgiven, 'treatmentgivenlist': treatmentgivenlist,
            'dailyround':dailyround,'dailyroundlist':dailyroundlist,
            'discharge': discharge,
        })
@login_required
def print(request,ipd_id):
     object = get_object_or_404(Ipd, pk=ipd_id)
     treatmentgivenlist = object.treatmentgiven_set.all()
     treatmentadvicedlist = object.treatmentadviced_set.all()
     prolist = Procedure.objects.all().filter(ipd=ipd_id)
     discharge = Discharge.objects.get(pk=ipd_id)
     investigationlist = Investigation.objects.all().filter(ipd=ipd_id)
   
     return render (request,'dischargeprint.html',{'discharge':discharge,'object': object,'investilist': investigationlist,'prolist': prolist,'treatmentadvicedlist': treatmentadvicedlist,'treatmentgivenlist': treatmentgivenlist})
@login_required
def discharge_list(request):
    dischargelist = Discharge.objects.all()
    return render(request, 'dischargelist.html', {'dischargelist': dischargelist})

@login_required
def discharge_history(request, ipd_id):
    object = get_object_or_404(Ipd, pk=ipd_id)
    treatmentgivenlist = object.treatmentgiven_set.all()
    treatmentadvicedlist = object.treatmentadviced_set.all()
    prolist = Procedure.objects.all().filter(ipd=ipd_id)
    procedure = ProcedureForm()
    investigationlist = Investigation.objects.all().filter(ipd=ipd_id)
   
    return render(request, 'dischargeh.html', {
            'object': object,  'investilist': investigationlist,
             'prolist': prolist,
             'treatmentadvicedlist': treatmentadvicedlist,
             'treatmentgivenlist': treatmentgivenlist,
            
            
        })
