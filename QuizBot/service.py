import secrets
import requests

class HTTPService:
    @staticmethod
    def send_request(method, url, headers=None, data=None):
        try:
            response = requests.request(method, url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'HTTP Request failed: {e}')
            return None
class LineService:
    @staticmethod
    def build_auth_url(client_id, redirect_uri, scope):
        state = secrets.token_urlsafe(16)
        nonce = secrets.token_urlsafe(16)
        auth_url = f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}&nonce={nonce}"
        return auth_url, state

    @staticmethod
    def exchange_token(code, redirect_uri, client_id, client_secret):
        body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        url = 'https://api.line.me/oauth2/v2.1/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return HTTPService.send_request('POST', url, headers=headers, data=body)

    @staticmethod
    def get_profile(access_token):
        url = 'https://api.line.me/v2/profile'
        headers = {'Authorization': f'Bearer {access_token}'}
        return HTTPService.send_request('GET', url, headers=headers)
    
    @staticmethod
    def verify_id_token(id_token, client_id):
        body = {
            'id_token': id_token,
            'client_id': client_id
        }
        url = 'https://api.line.me/oauth2/v2.1/verify'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return HTTPService.send_request('POST', url, headers=headers, data=body)