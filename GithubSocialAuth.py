import os
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import WebApplicationClient
import webbrowser
from database_script_social_auth import Session, User
from dotenv import load_dotenv

load_dotenv()

AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
API_URL = "https://api.github.com/user"

# GitHub OAuth credentials
CLIENT_ID = os.getenv("CLIENT_ID_GITHUB")
CLIENT_SECRET = os.getenv("CLIENT_SECRET_GITHUB")
REDIRECT_URI = "https://d178-182-70-122-97.ngrok-free.app"

client = WebApplicationClient(CLIENT_ID)
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


def save_user_to_db(user_data):
    """
    Function to save user data to github user database
    """

    session = Session()
    existing_user = session.query(User).filter_by(github_id=user_data["id"]).first()
    if existing_user:
        print(f"User {user_data['login']} already exists in the database.")
    else:
        user = User(
            github_id=user_data["id"],
            username=user_data["login"],
            email=user_data.get("email"),
            avatar_url=user_data.get("avatar_url"),
        )
        session.add(user)
        session.commit()
        print(f"User {user_data['login']} saved to the database.")
    session.close()


def main():
    """
    Main function to execute the flow of github authentication
    """
    
    authorization_url = get_authorization_url()
    # webbrowser.open(authorization_url)
    authorization_response = input("Paste the full redirect URL here: ")
    get_access_token(authorization_response)
    user_data = get_user_data()
    print("User data retrieved from GitHub:")
    print(user_data)
    save_user_to_db(user_data)


if __name__ == "__main__":
    main()
