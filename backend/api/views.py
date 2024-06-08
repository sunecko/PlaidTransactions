import requests
from os import getenv
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import load_dotenv
from api.models import AccountInfo

load_dotenv()

PLAID_CLIENT_ID = getenv("PLAID_CLIENT_ID")
PLAID_SECRET = getenv("PLAID_SECRET")
PLAID_ENV = getenv("PLAID_ENV")


class LinkTokenView(APIView):

    def post(self, request):
        data = {
            'client_id': PLAID_CLIENT_ID,
            'secret': PLAID_SECRET,
            'user': {
                'client_user_id': "1"
            },
            'redirect_uri': PlaidUrls.RedirectUri,
            'products': ["transactions"],
            'client_name': "Hector Huerta Garcia",
            'country_codes': ['US'],
            'language': 'en'
        }

        response = requests.post(PlaidUrls.CreateTokenLink, json=data)

        if response.status_code == 200:
            token_link = response.json()['link_token']
            return Response({'token_link': token_link}, status=200)
        else:
            return Response({
                'status': 'error',
                'message': 'Failed to create token link'},
                status=response.status_code)


class SaveAccessTokenView(APIView):
    def post(self, request):
        public_token = request.data.get('token')

        if not public_token:
            return Response({'error': 'Public token is required'}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.post(PlaidUrls.PublicTokenExchange, json={
            'client_id': PLAID_CLIENT_ID,
            'secret': PLAID_SECRET,
            'public_token': public_token
        })

        if response.status_code != 200:
            return Response({'error': 'Failed to exchange public token'}, status=response.status_code)

        access_token = response.json().get('access_token')
        item_id = response.json().get('item_id')
        if not access_token:
            return Response({'error': 'No access token returned'}, status=status.HTTP_400_BAD_REQUEST)

        token_instance = AccountInfo(access_token=access_token, item_id=item_id)
        token_instance.save()

        return Response({'access_token': access_token}, status=status.HTTP_201_CREATED)


class TransactionsView(APIView):
    def post(self, request):
        try:
            access_token_instance = AccountInfo.objects.last()
            access_token = access_token_instance.access_token
        except AccountInfo.DoesNotExist:
            return Response({'error': 'No access token found'}, status=status.HTTP_404_NOT_FOUND)

        response = requests.post(PlaidUrls.GetTransactions, json={
            'client_id': PLAID_CLIENT_ID,
            'secret': PLAID_SECRET,
            'access_token': access_token,
            'start_date': '2023-01-01',
            'end_date': '2024-12-31'
        })

        if response.status_code != 200:
            return Response({'error': 'Failed to fetch transactions'}, status=response.status_code)

        return Response(response.json(), status=status.HTTP_200_OK)


class PlaidUrls:
    CreateTokenLink = "https://sandbox.plaid.com/link/token/create"
    GetTransactions = "https://sandbox.plaid.com/transactions/get"
    RedirectUri = "http://localhost:5174/plaid-callback"
    PublicTokenExchange = "https://sandbox.plaid.com/item/public_token/exchange"
