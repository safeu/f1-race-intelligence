"""
===========================================================
SCRIPT: driver_images
===========================================================
Script purpose:
    Script to get driver images.
    Priority: Official F1 headshots → Wikipedia fallback

Functions present:
    get_driver_photo()
        - main function, tries F1 headshots first then Wikipedia
    get_driver_photo_wikipedia()
        - fetch driver photo from Wikipedia
"""

import requests

DRIVER_HEADSHOTS = {
    # 2025 Grid
    'Max Verstappen': 'https://www.formula1.com/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/2col/image.png',
    'Liam Lawson': 'https://www.formula1.com/content/dam/fom-website/drivers/L/LIALAW01_Liam_Lawson/lialaw01.png.transform/2col/image.png',
    'Charles Leclerc': 'https://www.formula1.com/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.png.transform/2col/image.png',
    'Lewis Hamilton': 'https://www.formula1.com/content/dam/fom-website/drivers/L/LEWHAM01_Lewis_Hamilton/lewham01.png.transform/2col/image.png',
    'Lando Norris': 'https://www.formula1.com/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.png.transform/2col/image.png',
    'Oscar Piastri': 'https://www.formula1.com/content/dam/fom-website/drivers/O/OSCPIA01_Oscar_Piastri/oscpia01.png.transform/2col/image.png',
    'George Russell': 'https://www.formula1.com/content/dam/fom-website/drivers/G/GEORUS01_George_Russell/georus01.png.transform/2col/image.png',
    'Andrea Kimi Antonelli': 'https://www.formula1.com/content/dam/fom-website/drivers/A/ANDANT01_Andrea_Kimi_Antonelli/andant01.png.transform/2col/image.png',
    'Fernando Alonso': 'https://www.formula1.com/content/dam/fom-website/drivers/F/FERALO01_Fernando_Alonso/feralo01.png.transform/2col/image.png',
    'Lance Stroll': 'https://www.formula1.com/content/dam/fom-website/drivers/L/LANSTR01_Lance_Stroll/lanstr01.png.transform/2col/image.png',
    'Pierre Gasly': 'https://www.formula1.com/content/dam/fom-website/drivers/P/PIEGAS01_Pierre_Gasly/piegas01.png.transform/2col/image.png',
    'Jack Doohan': 'https://www.formula1.com/content/dam/fom-website/drivers/J/JACDOO01_Jack_Doohan/jacdoo01.png.transform/2col/image.png',
    'Yuki Tsunoda': 'https://www.formula1.com/content/dam/fom-website/drivers/Y/YUKTSU01_Yuki_Tsunoda/yuktsu01.png.transform/2col/image.png',
    'Isack Hadjar': 'https://www.formula1.com/content/dam/fom-website/drivers/I/ISAHAD01_Isack_Hadjar/isahad01.png.transform/2col/image.png',
    'Alexander Albon': 'https://www.formula1.com/content/dam/fom-website/drivers/A/ALEALB01_Alexander_Albon/alealb01.png.transform/2col/image.png',
    'Carlos Sainz': 'https://www.formula1.com/content/dam/fom-website/drivers/C/CARSAI01_Carlos_Sainz/carsai01.png.transform/2col/image.png',
    'Nico Hulkenberg': 'https://www.formula1.com/content/dam/fom-website/drivers/N/NICHUL01_Nico_Hulkenberg/nichul01.png.transform/2col/image.png',
    'Gabriel Bortoleto': 'https://www.formula1.com/content/dam/fom-website/drivers/G/GABBOR01_Gabriel_Bortoleto/gabbor01.png.transform/2col/image.png',
    'Esteban Ocon': 'https://www.formula1.com/content/dam/fom-website/drivers/E/ESTOCO01_Esteban_Ocon/estoco01.png.transform/2col/image.png',
    'Oliver Bearman': 'https://www.formula1.com/content/dam/fom-website/drivers/O/OLIBEA01_Oliver_Bearman/olibea01.png.transform/2col/image.png',

    # 2024 drivers not in 2025
    'Sergio Perez': 'https://www.formula1.com/content/dam/fom-website/drivers/S/SERPER01_Sergio_Perez/serper01.png.transform/2col/image.png',
    'Kevin Magnussen': 'https://www.formula1.com/content/dam/fom-website/drivers/K/KEVMAG01_Kevin_Magnussen/kevmag01.png.transform/2col/image.png',
    'Valtteri Bottas': 'https://www.formula1.com/content/dam/fom-website/drivers/V/VALBOT01_Valtteri_Bottas/valbot01.png.transform/2col/image.png',
    'Guanyu Zhou': 'https://www.formula1.com/content/dam/fom-website/drivers/G/GUAZHO01_Guanyu_Zhou/guazho01.png.transform/2col/image.png',
    'Logan Sargeant': 'https://www.formula1.com/content/dam/fom-website/drivers/L/LOGSAR01_Logan_Sargeant/logsar01.png.transform/2col/image.png',
    'Daniel Ricciardo': 'https://www.formula1.com/content/dam/fom-website/drivers/D/DANRIC01_Daniel_Ricciardo/danric01.png.transform/2col/image.png',
    'Nyck De Vries': 'https://www.formula1.com/content/dam/fom-website/drivers/N/NYCDEV01_Nyck_De_Vries/nycdev01.png.transform/2col/image.png',

    # 2020-2023 drivers
    'Sebastian Vettel': 'https://www.formula1.com/content/dam/fom-website/drivers/S/SEBVET01_Sebastian_Vettel/sebvet01.png.transform/2col/image.png',
    'Kimi Raikkonen': 'https://www.formula1.com/content/dam/fom-website/drivers/K/KIMRAI01_Kimi_Raikkonen/kimrai01.png.transform/2col/image.png',
    'Antonio Giovinazzi': 'https://www.formula1.com/content/dam/fom-website/drivers/A/ANTGIO01_Antonio_Giovinazzi/antgio01.png.transform/2col/image.png',
    'Romain Grosjean': 'https://www.formula1.com/content/dam/fom-website/drivers/R/ROMGRO01_Romain_Grosjean/romgro01.png.transform/2col/image.png',
    'Daniil Kvyat': 'https://www.formula1.com/content/dam/fom-website/drivers/D/DANKVY01_Daniil_Kvyat/dankvy01.png.transform/2col/image.png',
    'Nicholas Latifi': 'https://www.formula1.com/content/dam/fom-website/drivers/N/NICLAT01_Nicholas_Latifi/niclat01.png.transform/2col/image.png',
    'Mick Schumacher': 'https://www.formula1.com/content/dam/fom-website/drivers/M/MICSCH02_Mick_Schumacher/micsch02.png.transform/2col/image.png',
    'Nikita Mazepin': 'https://www.formula1.com/content/dam/fom-website/drivers/N/NIKMAZ01_Nikita_Mazepin/nikmaz01.png.transform/2col/image.png',
    'Robert Kubica': 'https://www.formula1.com/content/dam/fom-website/drivers/R/ROBKUB01_Robert_Kubica/robkub01.png.transform/2col/image.png',
    'Pietro Fittipaldi': 'https://www.formula1.com/content/dam/fom-website/drivers/P/PIEFIT01_Pietro_Fittipaldi/piefit01.png.transform/2col/image.png',
    'Stoffel Vandoorne': 'https://www.formula1.com/content/dam/fom-website/drivers/S/STOVAN01_Stoffel_Vandoorne/stovan01.png.transform/2col/image.png',
    'Nyck de Vries': 'https://www.formula1.com/content/dam/fom-website/drivers/N/NYCDEV01_Nyck_De_Vries/nycdev01.png.transform/2col/image.png',
    'Theo Pourchaire': 'https://www.formula1.com/content/dam/fom-website/drivers/T/THEPOU01_Theo_Pourchaire/thepou01.png.transform/2col/image.png',
}


def get_driver_photo_wikipedia(driver_name):
    try:
        headers = {
            "User-Agent": "F1RaceIntelligence/1.0 (portfolio project; educational use)"
        }
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": f"{driver_name} Formula One driver 2020",
            "format": "json",
            "srlimit": 1
        }
        search_response = requests.get(search_url, params=search_params, headers=headers)
        search_data = search_response.json()

        if not search_data["query"]["search"]:
            return None

        page_title = search_data["query"]["search"][0]["title"]

        image_params = {
            "action": "query",
            "titles": page_title,
            "prop": "pageimages",
            "format": "json",
            "pithumbsize": 300
        }
        image_response = requests.get(search_url, params=image_params, headers=headers)
        image_data = image_response.json()

        pages = image_data["query"]["pages"]
        page = next(iter(pages.values()))

        if "thumbnail" in page:
            return page["thumbnail"]["source"]
        return None

    except Exception as e:
        print(f"Error fetching photo for {driver_name}: {e}")
        return None


def get_driver_photo(driver_name):
    url = DRIVER_HEADSHOTS.get(driver_name)
    if url:
        return url
    
    return get_driver_photo_wikipedia(driver_name)