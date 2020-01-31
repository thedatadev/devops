from auth import token
import json
import requests


def unpack_response(response) -> dict:
    response_json = response.content.decode('utf-8')
    response_dict = json.loads(response_json)
    return response_dict


def get_public_url() -> str:
    ''' Obtains the public URL for the HTTP ngrok tunnel '''
    tunnels_url = 'http://127.0.0.1:4040/api/tunnels'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(tunnels_url,headers=headers)
    response_dict = unpack_response(response)
    https_tunnel, http_tunnel = response_dict['tunnels']
    return http_tunnel['public_url'] + '/api'
    

def create_webhook(url) -> 'str':
    webhooks_url = 'https://api.github.com/repos/thedatadev/devops/hooks'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'name': 'web',
        'active': True,
        'events': [
            'push',
            'pull_request',
        ],
        'config': {
            'url': url,
            'content_type': 'json',
            'insecure_ssl': 0,
        },
    }
    response = requests.post(webhooks_url, headers=headers, json=data)
    response_dict = unpack_response(response)
    ping_url = response_dict['ping_url']
    return ping_url


if __name__ == '__main__':

    url = get_public_url()
    ping_url = create_webhook(url)
    # TODO - ping the webhook to make sure it's still up