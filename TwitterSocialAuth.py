import os
import webbrowser
from requests_oauthlib import OAuth2Session
from database_script_social_auth import Session, User
from dotenv import load_dotenv


load_dotenv()

AUTHORIZATION_BASE_URL = "https://twitter.com/i/oauth2/authorize"
TOKEN_URL = "https://api.twitter.com/oauth2/token"
API_URL = "https://api.twitter.com/2/me"

CLIENT_ID = os.getenv("CLIENT_ID_TWITTER")
CLIENT_SECRET = os.getenv("CLIENT_SECRET_TWITTER")
REDIRECT_URI = "https://ab7a-182-70-122-97.ngrok-free.app"

oauth_session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)

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
    
    try:
        oauth_session.fetch_token(TOKEN_URL, authorization_response=authorization_response, client_secret=CLIENT_SECRET)
        print("Access token obtained successfully.")
    except Exception as e:
        print(f"Error during token exchange: {str(e)}")


def get_user_data():
    """
    Function to get user data
    """
    
    response = oauth_session.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to retrieve user data. Status code: {response.status_code}"}

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
