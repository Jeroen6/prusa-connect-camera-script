import requests
import time
from secrets import * # gitignored for security

def fetch_snapshot(url):
    """
    Fetches a snapshot from the given URL and returns the image data.

    Parameters:
    - url (str): The URL of the snapshot.

    Returns:
    - bytes: The image data if successful.
    - None: If there was an error fetching the snapshot.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to retrieve snapshot. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def upload_image(http_url, fingerprint, token, image):
    """Upload an image over http"""
    response = requests.put(
        http_url,
        headers={
            "accept": "*/*",
            "content-type": "image/jpg",
            "fingerprint": fingerprint,
            "token": token,
        },
        data=image,
        stream=True,
    )
    return response
    
def main():
    prusa_connect_url = "https://webcam.connect.prusa3d.com/c/snapshot"

    try:
        while True:
            try:
                image = fetch_snapshot(image_source_url)
                if image:
                    print(len(image))
                else:
                    print("Failed to fetch the snapshot.")
                response = upload_image(prusa_connect_url, camera_fingerprint, prusa_camera_api_token, image)
                print(response)
            finally:
                None
            
            # Wait for 10 seconds before fetching the snapshot again
            time.sleep(10)
    except KeyboardInterrupt:
        print("Program interrupted and stopped.")
        

if __name__ == "__main__":
    main()
