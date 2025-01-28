{
    'name':'Hospital Management',
    'application':True,
    'sequence':1,
    'author': 'Fahim',
    'depends': ['mail'],
    'data':[
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'reports/patient_bill_report_action.xml',
        'reports/patient_bill_report_template.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_patient_bill_view.xml',
        'views/hospital_doctor_view.xml',
        'views/hospital_department_views.xml',
        'views/menu.xml', #keep the menu at last so that all the other files can load before it!!!

    ]
}


