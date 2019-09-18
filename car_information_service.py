import requests
from bs4 import BeautifulSoup


def get_car_information(license_plate):
    return scrape_from_regnr(license_plate)


def scrape_from_regnr(license_plate):
    url_params = "s1=" + license_plate[0] + "&s2=" + license_plate[1] + "&s3=" + license_plate[2] + "&s4=" \
        + license_plate[3] + "&s5="  + license_plate[4] + "&s6=" + license_plate[5] + "&s7=" + license_plate[6]

    url = "https://regnr.info/husker-ikke-hele-regnr?" + url_params
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    car_information = soup.find(id="huskerikke_right").contents[3].contents[0].contents[2]

    return {
        "registreringsnummer": license_plate,
        "merke": car_information.contents[1].string.split(' ', 1)[0], # assume all brands are one-worded
        "modell": car_information.contents[1].string.split(' ', 1)[1],
        "farge": car_information.contents[3].string
    }


def get_car_information_from_api(license_plate):
    api = "https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/kjoretoyoppslag/v1/kjennemerkeoppslag/kjoretoy/"
    response = requests.get(api + license_plate).json()

    return {
        "registreringsnummer": response["kjennemerke"],
        "merke": response["tekniskKjoretoy"]["merke"],
        "modell": response["tekniskKjoretoy"]["handelsbetegnelse"],
        "farge": response["tekniskKjoretoy"]["karosseri"]["farge"]
    }
