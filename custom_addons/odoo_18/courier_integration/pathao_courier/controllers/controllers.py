
from odoo import http
from odoo.http import request
import requests


demo_sandbox_credentials = {
    'base_url': 'https://courier-api-sandbox.pathao.com',
    'client_id': '7N1aMJQbWm',
    'client_secret': 'wRcaibZkUdSNz2EI9ZyuXLlNrnAv0TdPUPXMnD39',
    'username': 'test@pathao.com',
    'password': 'lovePathao',
    'grant_type': 'password'
}

credentials = {
    'base_url': 'https://api-hermes.pathao.com',
    'client_id': 'GRb46qJeBL',
    'client_secret': 'GUzjh8RonDEVIOcWooZaHBc4LsAtpkhO4FrhRScu',
    'username': '',
    'password': '',
    'grant_type': ''
}



demo_payload = {
    "client_id": demo_sandbox_credentials.get('client_id'),
   "client_secret": demo_sandbox_credentials.get('client_secret'),
   "grant_type": demo_sandbox_credentials.get('grant_type'),
   "username": demo_sandbox_credentials.get('username'),
   "password": demo_sandbox_credentials.get('password')
}



demo_request_parameter = {
    'Content-Type': 'application/json',
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyNjciLCJqdGkiOiI0M2EzYWRkYTQ0NTAzMTI5MWIwMTAwYWMyZmQ3ZmQ0YzY1Y2U1OTkzMDMwZGQ3ZGYzMGM1NDc5ZDEyZTQ4MGU2OGZkZGQyNWI0M2EzMWRhNyIsImlhdCI6MTc0NTc1MTI3My4yODQ4NiwibmJmIjoxNzQ1NzUxMjczLjI4NDg2MiwiZXhwIjoxNzQ2MTgzMjczLjI2OTgwMywic3ViIjoiMzUyIiwic2NvcGVzIjpbXX0.kJKjX059ubQolyZMAtM2YKV15uYsk8dl3V8pEklyQH22cUgfzZI-GV7JlHZzO5pbDFIqjff5Pdx6xfrUZTPvILDltZ-sWmXhYpmtHSaRdpdNAlCs4rPhAcvpKGA3bn7woWa4gcvOS21zdzoKFT8ZnPhWJpB0WsY7yJ34t3PYd_-CTqcaM7lu_YY56WxfIFP-oZQeKpAGvCES3FdymIJpqm-4mzkIYR8JJ0AIJwklx4WWi_IGLzQj_djHFnc5xFwED0vBT-yR7tKoMBvH5TCogp0xDwkni5U5xGUz2Ldo8cz5jIUFfT5S1yztlPSdaUsk__-JV79rB-aBj4eZzgB-04kfzxg6Nk3-rfy6dTby8V76prIrQu52QdPDdNTdw0Z5MZN-nq_W7JcDgRHcHMrhp-IjBgQ__azkBwLCe_s4347oAPc4K-uq0sDdQ8fP0POURAhHuA-jTpYEXNWKovrlSxdONk9_FGFYzUnJe72xKAGkS5VExeGhfW7pQjA1DAlLnthEdrfcz5reqghFuak7qQdsh9Wgfvmee6dUKFlNp77bsFhUUcVNOm6RcflePmJynRM1wYXjVh3kHXGF8c4B3pEGvlK2js-lSrLR86ICnC9_PYbRfKgRcU_uc1H_eKro2ZLcXS_VjfNYuYRToFvnrE_hvauTa1QuLznFPCvRs0I",
    "refresh_token": "def50200ca29541f476913bf7267d288f19e1fac4c1329ca3afd47a6c6fefa454420509f0574760988dfa6f014c160b88199c189dbdf693c5a1aa9c1bc1a71607cc79dd03ecefe1f60d2e587109b292968cc5737453df2be3f22384792ebe97387c38676bc0865ca520c3b87408e29d8210868635a335e45f7ba40699aeae768e76bed0fd40216c4b4e64176561af99055900c1e3725880c289ef3735b377264ed76b7a93686acb27880eaf71add088a6a4ce0033c17ee85566221e4871fdf3c8f9add232e37b85117e75679730927b971db13c5f9c893a9d2c43316704ed68e72a1624b2a7eeb159931488671fa417851d4424e4e6d6dbeb239ca679a755c7b4af8ab92faeef75e9e319792413aeeab988d23fb151e6267960a20e5a81f65bb4534c58ef57334a871de0d4873c494bdf222a77d037b42bd9e5199a6cf3e14de2f835b7b5e052e6ea7b3d8c2c948e4a73929a1315208841c140627ac25e7168c8121072c25",

}



demo_headers = {
    'Content-Type': f"{demo_request_parameter.get('Content-Type')}; charset=UTF-8",
    'Authorization': f"Bearer {demo_request_parameter.get('access_token')}"
}


class PathaoCourier(http.Controller):

    @http.route('/pathao/get/access_token', type='json', auth='none')
    def pathao_get_access_token(self):
        print(f'------------------ pathao/get/access_token -------------------')

        demo_url = f"{demo_sandbox_credentials['base_url']}/aladdin/api/v1/issue-token"
        response = requests.post(demo_url, headers = demo_request_parameter.get('Content-Type'), json=demo_payload)

        print(f'response status code ------- {response.status_code}')
        print(f'response status text ------- {response.text}')

        return {'status':response.status_code, 'response':response.json()}


    @http.route('/pathao/get/cities', type='json', auth='none')
    def pathao_get_cities(self):
        print(f'---------------  /pathao/get/cities --------------------')



        demo_url = f"{demo_sandbox_credentials['base_url']}/aladdin/api/v1/city-list"
        response = requests.get(demo_url, headers=demo_headers, data='')
        print(f'response status code ------- {response.status_code}')
        print(f'response status text ------- {response.text}')

        return {'status':response.status_code, 'response':response.json()}

    @http.route('/pathao/get/zones_of_city/<int:city_id>', type='json', auth='none')
    def pathao_get_zones_of_city(self, city_id):
        print(f'---------------  /pathao/get/zones_of_city --------------------')



        demo_url = f"{demo_sandbox_credentials['base_url']}/aladdin/api/v1/cities/{city_id}/zone-list"
        response = requests.get(demo_url, headers=demo_headers, data='')
        print(f'response status code ------- {response.status_code}')
        print(f'response status text ------- {response.text}')

        return {'status':response.status_code, 'response':response.json()}

    @http.route('/pathao/get/area_of_zone/<int:zone_id>', type='json', auth='none')
    def pathao_get_area_of_zone(self, zone_id):
            print(f'---------------  /pathao/get/area_of_city --------------------')



            demo_url = f"{demo_sandbox_credentials['base_url']}/aladdin/api/v1/zones/{zone_id}/area-list"
            response = requests.get(demo_url, headers=demo_headers, data='')
            print(f'response status code ------- {response.status_code}')
            print(f'response status text ------- {response.text}')

            return {'status':response.status_code, 'response':response.json()}

    @http.route('/pathao/price_calculate', type='json', auth='none')
    def pathao_price_calculate(self, **kwargs):
        print(f'---------------  /pathao/get/area_of_city --------------------')

        pay_load = {
            "store_id": kwargs.get('merchant_store_id'),
           "item_type": kwargs.get('item_type'),
           "delivery_type": kwargs.get('delivery_type'),
           "item_weight": kwargs.get('item_weight'),
           "recipient_city": kwargs.get('recipient_city'),
           "recipient_zone": kwargs.get('recipient_zone')
        }
        print(f'pay_load -------  {pay_load}')


        demo_url = f"{demo_sandbox_credentials['base_url']}/aladdin/api/v1/merchant/price-plan"
        response = requests.get(demo_url, headers=demo_headers, data=pay_load)
        print(f'response status code ------- {response.status_code}')
        print(f'response status text ------- {response.text}')

        return {'status': response.status_code, 'response': response.json()}



    @http.route('/pathao/get/store/info', type='json', auth='none')
    def pathao_get_store_info(self):
        print(f'---------------  /pathao/get/store/info --------------------')



        demo_url = f"{demo_sandbox_credentials['base_url']}/aladdin/api/v1/stores"
        response = requests.get(demo_url, headers=demo_headers, data='')
        print(f'response status code ------- {response.status_code}')
        print(f'response status text ------- {response.text}')

        return {'status': response.status_code, 'response': response.json()}

