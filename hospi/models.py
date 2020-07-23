from django.db import models
import datetime
from django.utils.timezone import now

# Create your models here.


Consultant = (
    ('Doctor1', 'Doctor1'),
    ('Doctor2', 'Doctor2'),

)

Gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

Admission_condition = (
    ('Undetermined', 'Undetermined'),
    ('Stable', 'Stable'),
    ('Serious', 'Serious'),
)

Discharge_type = (
    ('Discharge', 'Discharge'),
    ('Dama', 'Dama'),
    ('Dead', 'Dead'),
    ('Transfer', 'Transfer'),

)

Route = (
    ('Oral', 'Oral'),
    ('IV', 'IV'),
    ('IM', 'IM'),
    ('Other', 'Other'),
    ('L/A', 'L/A'),
    ('R/T', 'R/T'),
    ('S.C', 'S.C'),
    ('Other', 'Other'),
)

Doses_type = (
    ('OD', 'OD'),
    ('BD', 'BD'),
    ('TDS', 'TDS'),
    ('QID', 'QID'),
    ('STAT', 'STAT'),
)


# def increment_booking_number():
# last_patient = Patient.objects.all().order_by('id').last()
# if not last_patient:
# return 'REG/' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '1000'
# patient_id = last_patient.patient_id
# patient_int = int(patient_id[9:13])
# new_patient_int = patient_int + 1
# new_patient_id = 'REG/' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_patient_int).zfill(4)
# return new_patient_id


class Patient(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20)
    address = models.TextField()
    patient_id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=6, choices=Gender)


class Opd(models.Model):
    opd_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True,null=True)
    date = models.DateField(default=datetime.date.today)
    time =  models.TimeField(blank=True, default=now)

class Rooms(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Ipd(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True)
    reason_admission = models.CharField(max_length=200, blank=True)
    provisional_diagnosis = models.CharField(max_length=200, )
    ipd_id = models.AutoField(primary_key=True)
    weight = models.CharField(max_length=10, blank=True)
    bill_responsible = models.CharField(max_length=100, blank=True)
    bill_relation = models.CharField(max_length=100, blank=True)
    rooms = models.ForeignKey(Rooms, on_delete=models.CASCADE, blank=True)
    date_of_admission = models.DateField(default=datetime.date.today)
    time_of_admission = models.TimeField(blank=True, default=now)
    condition_admission = models.CharField(max_length=20, choices=Admission_condition)
    consultant = models.CharField(max_length=20, choices=Consultant)
    secondary_consultant = models.CharField(max_length=200)

    def __str__(self):
        return self.patient.firstname


class TreatmentGiven(models.Model):
    id = models.AutoField(primary_key=True)
    ipd = models.ForeignKey(Ipd, on_delete=models.CASCADE, default=None)
    medicine_name = models.CharField(max_length=100, null=True)
    types_of_doses = models.CharField(max_length=100, choices=Doses_type, blank=True)
    route = models.CharField(max_length=100, choices=Route, blank=True)
    number_of_days = models.IntegerField(null=True)


class TreatmentAdviced(models.Model):
    id = models.AutoField(primary_key=True)
    ipd = models.ForeignKey(Ipd, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=100, blank=True)
    types_ofdoses = models.CharField(max_length=100, blank=True)
    number_ofdays = models.IntegerField(blank=True)
    discription = models.CharField(max_length=100)


class Investigation(models.Model):
    id = models.AutoField(primary_key=True)
    ipd = models.ForeignKey(Ipd, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    report = models.TextField(max_length=500)
    date = models.DateField(("Date"), default=datetime.date.today)


class Procedure(models.Model):
    id = models.AutoField(primary_key=True)
    ipd = models.ForeignKey(Ipd, on_delete=models.CASCADE)
    report = models.TextField(max_length=500)
    date = models.DateField(("Date"), default=datetime.date.today)
    time = models.TimeField(blank=True, default=now)


class DailyRound(models.Model):
    id = models.AutoField(primary_key=True)
    ipd = models.ForeignKey(Ipd, on_delete=models.CASCADE)
    temp = models.CharField(max_length=50)
    pulse = models.CharField(max_length=50)
    bp = models.CharField(max_length=50)
    rs = models.CharField(max_length=50)
    cvs = models.CharField(max_length=50)
    pa = models.CharField(max_length=50)
    cns = models.CharField(max_length=50)
    pupils = models.CharField(max_length=50)
    planter = models.CharField(max_length=50)
    other = models.CharField(max_length=50)
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(blank=True, default=now)


class Discharge(models.Model):
    id =  models.AutoField(primary_key=True)
    ipd = models.ForeignKey(Ipd, on_delete=models.CASCADE, default=None)
    final_diagnosis = models.CharField(max_length=100, blank=True)
    discharge_condition = models.CharField(max_length=100)
    follow_up_advice = models.CharField(max_length=100)
    type_discharge = models.CharField(max_length=30, choices=Discharge_type)
    date_of_discharge = models.DateField(default=datetime.date.today)
    time_of_discharge = models.TimeField(blank=True, default=now)
