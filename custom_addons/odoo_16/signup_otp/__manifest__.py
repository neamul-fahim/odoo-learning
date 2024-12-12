{
    'name': 'Signup',
    'version': '1.0',
    'category': 'Website',
    'summary': 'A simple signup_otp page with email verification using OTP.',
    'author': 'Your Name',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/signup_page.xml',
        'views/otp_verification_page.xml',
        'views/welcome_page.xml',
    ],
    'installable': True,
    'application': True,
    'website': 'https://yourwebsite.com',
}
