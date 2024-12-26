import os
import requests
from requests_oauthlib import OAuth2Session, OAuth2


client_id = "787879506704-obeas0lp3tdn93uq1vninp2uheh5b8a0.apps.googleusercontent.com"
client_secret = "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"
redirect_uri = "https://cc02-182-70-122-97.ngrok-free.app"
print(client_id)
print(client_secret)

authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://oauth2.googleapis.com/token"
scope = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

google = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

authorization_url, state = google.authorization_url(
    authorization_base_url, access_type="offline", prompt="select_account"
)
print("This is state : ", state)
print(f"Please go to this URL and authorize: {authorization_url}")

redirect_response = input("Paste the full redirect URL here: ")


google.fetch_token(
    token_url, client_secret=client_secret, authorization_response=redirect_response
)

user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
user_info = google.get(user_info_url).json()

print("User Info:")
print(user_info)
