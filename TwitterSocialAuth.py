import os
import webbrowser
from requests_oauthlib import OAuth2Session
from database_script_social_auth import Session, User
from dotenv import load_dotenv


load_dotenv()

AUTHORIZATION_BASE_URL = "https://api.x.com/oauth/authorize"
TOKEN_URL = "https://api.x.com/2/oauth2/token"
API_URL = "https://api.x.com/2/users"

# twitter OAuth credentials
CLIENT_ID = os.getenv("CLIENT_ID_TWITTER")
CLIENT_SECRET = os.getenv("CLIENT_SECRET_TWITTER")
REDIRECT_URI = "https://ab7a-182-70-122-97.ngrok-free.app"

oauth_session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)

# oauth2_user_handler = tweepy.OAuth2UserHandler(
#     client_id=CLIENT_ID,
#     redirect_uri=REDIRECT_URI,
#     scope=['users.read','offline.access'],
#     client_secret=CLIENT_SECRET
# )

def get_authorization_url():
    """
    Function to get authorization url
    """

    authorization_url, state = oauth_session.authorization_url(AUTHORIZATION_BASE_URL)
    print(f"Visit this URL to authorize the application: {authorization_url}")
    return authorization_url


def get_access_token(authorization_response):
    """
    Function to get access token
    """
    
    oauth_session.fetch_token(
        TOKEN_URL,
        authorization_response=authorization_response,
        client_secret=CLIENT_SECRET,
    )
    print("Access token obtained successfully.")


def get_user_data():
    """
    Function to get user data
    """
    
    response = oauth_session.get(API_URL)
    return response.json()

def main():
    """
    Main function to execute the flow of twitter authentication
    """
    
    authorization_url = get_authorization_url()
    webbrowser.open(authorization_url)
    authorization_response = input("Paste the full redirect URL here: ")
    get_access_token(authorization_response)
    user_data = get_user_data()
    print("User data retrieved from twitter:")
    print(user_data)


if __name__ == "__main__":
    main()
