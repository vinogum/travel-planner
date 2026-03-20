import requests

ART_INSTITUTE_API_URL = "https://api.artic.edu/api/v1/artworks"


def check_artwork_exists(external_id: int) -> bool:
    try:
        response = requests.get(f"{ART_INSTITUTE_API_URL}/{external_id}", timeout=5)
        if response.status_code == 200:
            return True
        return False
    except requests.RequestException:
        return False
