# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, jsonify, request
from data.clinic_detail import clinic_detail
from data.clinics import clinics
from data.doctors import doctors
from data.specialties import specialties
app = Flask(__name__)

@app.route('/')
def showHome():
  return render_template('index.html',css_file='css/home.css')

@app.route('/clinics/')
def showClinics():
  return render_template('clinics.html', css_file='css/basic.css', header_img='img/clinics.jpg', h1='Clinics', h2='Check out clinics from Mandalay',clinics=clinics)

@app.route('/clinics/json')
def showClinicsJSON():
  return jsonify(clinics=clinics)

@app.route('/doctors/')
def showDoctors():
  return render_template('doctors.html', css_file='css/basic.css', header_img='img/doctors.jpg', h1='doctors', h2='Check out doctors from Mandalay', doctors=doctors, sp=[s['specialty_name'] for s in specialties])

def getClinicDetail(clinic_id):
  if not (clinic_id > 0 and clinic_id < 24):
    return None
  clinic = clinics[clinic_id - 1].copy()
  doc_ids = [i['doctor_id'] for i in clinic_detail if i['clinic_id'] == clinic_id]
  clinic['doctors'] = []
  for i in doc_ids:
    d = doctors[i-1]
    specialty = specialties[d['specialist'] - 1]['specialty_name']
    clinic['doctors'].append({ '_id': d['_id'],
     'doctor_name': d['doctor_name'],
     'degree': d['degree'],
     'specialty': specialty})
  return clinic

@app.route('/clinic/<int:clinic_id>/')
def showClinic(clinic_id):
  clinic = getClinicDetail(clinic_id)
  if clinic:
    return render_template('clinic_detail.html', css_file='css/basic.css', header_img='img/clinic_detail.jpg',
     h1=clinic['clinic_name'], h2=clinic['address'], p=clinic['phone'], doctors=clinic['doctors'])
  else:
    return 'No data associalted with clinic id of %d' % clinic_id

@app.route('/clinic/<int:clinic_id>/json')
def showClinicJSON(clinic_id):
  clinic = getClinicDetail(clinic_id)
  if clinic:
    return jsonify(clinic=clinic)
  else:
    return 'No data associalted with clinic id of %d' % clinic_id

# Labs testing
@app.route('/testNames')
def testNames():
  with open('./data/testNames.json', 'r', encoding='utf-8') as content_file:
    content = content_file.read()
  return content, 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/referer')
def referer():
  with open('./data/referer.json', 'r', encoding='utf-8') as content_file:
    content = content_file.read()
  return content, 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/auth')
def authentication():
  phone_no = request.args.get('phone_no')
  numbers = ['09970392283', '09970392284']
  pin = request.args.get('pin')
  if phone_no in numbers and pin == '123456':
    return '"True"'
  else:
    return '"False"'

if __name__ == '__main__':
  app.debug = True
  app.run(host='',port=8080)