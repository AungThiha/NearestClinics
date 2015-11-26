# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from data.clinic_detail import clinic_detail
from data.clinics import clinics
from data.doctors import doctors
from data.specialties import specialties
app = Flask(__name__)


#Making an API EndPoint (GET Request)
@app.route('/clinics/json')
def showClinics():
	return jsonify(clinics=clinics)

@app.route('/clinic/<int:clinic_id>/json')
def showClinic(clinic_id):
  if not (clinic_id > 0 and clinic_id < 24):
    return 'No data associated with the clinic id of %d' % clinic_id 
  clinic = clinics[clinic_id - 1].copy()
  clinic_id_str = str(clinic_id)
  print clinic_id_str
  doc_ids = [int(i['doctor_id']) for i in clinic_detail if i['clinic_id'] == clinic_id_str]
  clinic['doctors'] = []
  for i in doc_ids:
    d = doctors[i-1]
    d['specialty'] = specialties[int(d['specialist'])]['specialty_name']
    clinic['doctors'].append(d)
  return jsonify(clinic=clinic)

if __name__ == '__main__':
	app.run(host='',port=8080)