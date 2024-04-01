import requests, random

API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = ''
BOTTOKEN = ''

def refresh_token():
    try:
        refresh = open('refresh.txt', 'r').read().splitlines()
        refresh = random.choice(refresh)

        print(refresh)

        with open("refresh.txt", "r") as f:
            lines = f.readlines()
        with open("refresh.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != refresh:
                    f.write(line)

        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    except:
        pass
    try:
        r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
        print(r.json())

        access_token = r.json()['access_token']
        refresh_token = r.json()['refresh_token']

        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        r = requests.get('https://discordapp.com/api/users/@me', headers=headers).json()
        uid = r['id']

        f = open('db.txt', 'a')
        f.write(f'{access_token}:{uid}\n')
        f.close()

        f = open('refreshnew.txt', 'a')
        f.write(f'{refresh_token}\n')
        f.close()
    except:
        pass

def loop():
    while True:
        refresh_token()

loop()