{
    'name':'Hospital Management',
    'application':True,
    'depends': ['mail'],
    'data':[
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'reports/patient_bill_report_action.xml',
        'reports/patient_bill_report_template.xml',
        'views/menu.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_patient_bill_view.xml',
        'views/hospital_doctor_view.xml',
    ]
}


