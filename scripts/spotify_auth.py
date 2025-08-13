#!/usr/bin/env python3
"""
Spotify Authorization Helper
Run this to get the authorization URL and complete the OAuth flow
"""

import os
import sys
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

def main():
    # Create auth manager
    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:8888/callback'),
        scope="user-read-playback-state user-modify-playback-state",
        open_browser=False  # Don't auto-open browser
    )
    
    # Get the authorization URL
    auth_url = auth_manager.get_authorize_url()
    
    print("=" * 60)
    print("SPOTIFY AUTHORIZATION SETUP")
    print("=" * 60)
    print("\n1. Open this URL in any browser (phone/computer):")
    print("\n" + auth_url)
    print("\n2. Log in with the Spotify account you want to use")
    print("\n3. Click 'Agree' to authorize the app")
    print("\n4. You'll be redirected to a URL that looks like:")
    print("   http://127.0.0.1:8888/callback?code=LONG_CODE_HERE")
    print("\n5. Copy the ENTIRE redirect URL and paste it below")
    print("=" * 60)
    
    # Get the redirect URL from user
    redirect_response = input("\nPaste the full redirect URL here: ").strip()
    
    try:
        # Parse the response URL to get the code
        code = auth_manager.parse_response_code(redirect_response)
        
        if code:
            print("\n✓ Got authorization code!")
            print("Getting access token...")
            
            # Get the access token
            token_info = auth_manager.get_access_token(code)
            
            if token_info:
                print("✓ Successfully authenticated!")
                print("\nThe .cache file has been created with your credentials.")
                print("Copy this .cache file to your Raspberry Pi.")
                
                # Test the connection
                sp = spotipy.Spotify(auth_manager=auth_manager)
                user = sp.current_user()
                
                # Handle cases where email might not be available
                email = user.get('email', 'No email available')
                display_name = user.get('display_name', user.get('id', 'Unknown'))
                print(f"\n✓ Connected as: {display_name} ({email})")
                print(f"User ID: {user.get('id', 'Unknown')}")
                
                # Check current playback
                try:
                    playback = sp.current_playback()
                    if playback and playback['is_playing']:
                        print(f"Currently playing: {playback['item']['name']} by {playback['item']['artists'][0]['name']}")
                    else:
                        print("No active playback detected. Start playing something on Spotify to test controls.")
                except Exception as e:
                    print("Could not check current playback (this is normal if nothing is playing)")
                    
            else:
                print("✗ Failed to get access token")
        else:
            print("✗ No authorization code found in the URL")
            print("Make sure you copied the complete URL including the ?code= part")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("- Make sure you copied the ENTIRE URL from the browser")
        print("- The URL should contain '?code=' followed by a long string")
        print("- If you see '?error=' in the URL, check your app settings")

if __name__ == "__main__":
    main()