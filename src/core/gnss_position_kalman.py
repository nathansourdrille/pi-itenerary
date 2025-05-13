import time
from sensors.GNSS import GNSS
from utils import CSVHandler, LCD
from config import GNSS_DEVICE_ADDR, LCD_DEVICE_ADDR, GPS_BEIDOU_GLONASS


def get_position(mode=GPS_BEIDOU_GLONASS,
                 csv_out=None,
                 no_LCD=False,
                 kalman_queue=None,
                 kalman_mode=False):
    """
    Lit les données GNSS et affiche la position du module GNSS sur l'invité de commandes et le LCD.

    Arguments:
    - mode: Mode de fonctionnement du module GNSS. Valeur par défaut à GPS_BEIDOU_GLONASS.
    - csv_out: Le chemin et nom de fichier CSV pour l'enregistrement des acquisitions GNSS.
             S'il n'est pas défini, aucun enregistrement n'est effectué.
    - no_LCD: Booléen optionnel indiquant si on ne veut pas utiliser le LCD. Valeur par défaut à False.
    - kalman_queue: queue pour envoyer les données au filtre de Kalman
    - kalman_mode: booléen indiquant si le filtre de Kalman est activé
    """

    gnss = GNSS(1, GNSS_DEVICE_ADDR)
    gnss.initialisation(mode)
    save_csv = False
    if csv_out is not None:
        save_csv = True
        if not(csv_out.endswith('.csv')):
            csv_out += '.csv'
        record = CSVHandler(csv_out)
        record.create_csv_with_header(['Timestamp','UTC','Latitude','Longitude'])

    if not(no_LCD):
        lcd_display = LCD(LCD_DEVICE_ADDR)

    first_iteration = True
    try:
        while True:
            gnss.wait_for_next_scan()
            gnss.update()

            if save_csv and gnss.reception_ok:
                record.append_row([gnss.timestamp, gnss.utc, gnss.latitude.coordinates_DD, gnss.longitude.coordinates_DD])

            latitude = gnss.latitude.coordinates_DMM
            longitude = gnss.longitude.coordinates_DMM

            if kalman_mode and gnss.reception_ok:
                if first_iteration:
                    # Envoyer les premières données GPS pour initialisation
                    kalman_queue.put({
                        'lat': gnss.latitude.coordinates_DD,
                        'lon': gnss.longitude.coordinates_DD
                    })
                    first_iteration = False
                else:
                    # Envoyer les données GPS pour mise à jour
                    kalman_queue.put({
                        'lat': gnss.latitude.coordinates_DD,
                        'lon': gnss.longitude.coordinates_DD
                    })

            if gnss.reception_ok:
                if not(no_LCD):
                    lcd_display.afficher(f"Lat: {latitude}\nLon: {longitude}")
                print("--------------------------------------------------------------")
                print(f"Nombre de satellites utilisés: {gnss.number_satellites}")
                print(f"Latitude : {latitude}")
                print(f"Longitude : {longitude}")
                print("")
            else:
                if not(no_LCD):
                    lcd_display.afficher("Recherche de    signal GNSS...")
                print("Recherche de signal GNSS...")

    except KeyboardInterrupt as e:
        print("Arrêt du programme")
        if not(no_LCD):
            lcd_display.effacer()
