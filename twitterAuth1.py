import os
from requests_oauthlib import OAuth1Session
import webbrowser
from dotenv import load_dotenv

load_dotenv()

# Twitter API credentials
API_KEY = os.getenv("API_KEY_TWITTER")
API_SECRET_KEY = os.getenv("API_KEY_TWITTER_SECRET")
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZATION_URL = "https://api.twitter.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
API_URL = "https://api.twitter.com/1.1/account/verify_credentials.json"
CALLBACK_URI = "https://ab7a-182-70-122-97.ngrok-free.app"  

def get_request_token():
    """
    Function to get the request token
    """
    oauth = OAuth1Session(API_KEY, client_secret=API_SECRET_KEY, callback_uri=CALLBACK_URI)
    data = oauth.fetch_request_token(REQUEST_TOKEN_URL)
    print("Request token obtained successfully.")
    return data

def get_authorization_url(request_token):
    """
    Function to get the authorization URL
    """
    authorization_url = f"{AUTHORIZATION_URL}?oauth_token={request_token}"
    print(f"Visit this URL to authorize the application: {authorization_url}")
    return authorization_url

def get_access_token(oauth_token, oauth_verifier):
    """
    Function to get the access token
    """
    oauth = OAuth1Session(
        API_KEY, client_secret=API_SECRET_KEY, resource_owner_key=oauth_token, verifier=oauth_verifier
    )
    data = oauth.fetch_access_token(ACCESS_TOKEN_URL)
    print("Access token obtained successfully.")
    return data

def get_user_data(access_token, access_token_secret):
    """
    Function to get user data from Twitter
    """
    oauth = OAuth1Session(
        API_KEY, client_secret=API_SECRET_KEY, resource_owner_key=access_token, resource_owner_secret=access_token_secret
    )
    response = oauth.get(API_URL, params={"include_email": "true"})
    return response.json()

def main():
    """
    Main function to execute the flow of Twitter authentication
    """
    request_token_data = get_request_token()
    request_token = request_token_data["oauth_token"]
    authorization_url = get_authorization_url(request_token)
    webbrowser.open(authorization_url)

    oauth_verifier = input("Enter the PIN or verifier code provided by Twitter: ")
    access_token_data = get_access_token(request_token, oauth_verifier)
    access_token = access_token_data["oauth_token"]
    access_token_secret = access_token_data["oauth_token_secret"]

    user_data = get_user_data(access_token, access_token_secret)
    print("User data retrieved from Twitter:")
    print(user_data)

if __name__ == "__main__":
    main()
