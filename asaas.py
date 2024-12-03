import requests
from datetime import datetime, timedelta

class CreateCollection:
    def __init__(self, environment="test", key="", maturity=3) -> None:
        """environment = test / production"""
        if environment == "test":
            self.url = "https://sandbox.asaas.com/api/"
        else:
            self.url = "https://api.asaas.com/"

        today = datetime.today()
        due_date = today + timedelta(days=maturity)
        self.formatted_due_date = due_date.strftime("%Y-%m-%d")

        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "access_token": key
        }

    def create_customers(self, name="John Doe", cpfCnpj="24971563792", email="john.doe@asaas.com.br",
                         phone="4738010919", mobilePhone="4799376637", address="Av. Paulista", 
                         addressNumber="150", complement="Sala 201", province="Centro", 
                         postalCode="01310-000", externalReference="12987382", 
                         additionalEmails="john.doe@asaas.com,john.doe.silva@asaas.com.br", 
                         municipalInscription="46683695908", stateInscription="646681195275"):
        url = self.url + "v3/customers"

        payload = {
            "name": name,
            "cpfCnpj": cpfCnpj,
            "email": email,
            "phone": phone,
            "mobilePhone": mobilePhone,
            "address": address,
            "addressNumber": addressNumber,
            "complement": complement,
            "province": province,
            "postalCode": postalCode,
            "externalReference": externalReference,
            "additionalEmails": additionalEmails,
            "municipalInscription": municipalInscription,
            "stateInscription": stateInscription
        }

        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            customer_id = data.get("id")
            return customer_id
        else:
            print(f"Erro ao criar cliente: {response.status_code}")
            return response.text

    def create_charge(self, customer_id, billingType="PIX", value=129, description=""):
        """ billingType = BOLETO / PIX / CREDIT_CARD"""
        url = self.url + "v3/payments"

        payload = {
            "billingType": billingType,
            "customer": customer_id,
            "value": value,
            "dueDate": self.formatted_due_date,
            "description": description
        }

        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if billingType == "BOLETO":
                return data.get("bankSlipUrl")
            else:
                return data.get("invoiceUrl")
        else:
            print(f"Erro ao criar cobrança: {response.status_code}")
            return response.text

    def check_payments(self, customer_id):
        url = self.url + f"v3/payments?customer={customer_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            payments = data.get("data", [])
            if payments:
                status = payments[0].get("status")
                return status
            else:
                return "Nenhum pagamento encontrado."
        else:
            print(f"Erro ao verificar pagamentos: {response.status_code}")
            return response.text
