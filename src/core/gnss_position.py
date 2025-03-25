import time
from sensors.GNSS import GNSS
from utils import CSVHandler, LCD
from config import GNSS_DEVICE_ADDR, LCD_DEVICE_ADDR, GPS_BEIDOU_GLONASS


def get_position(mode=GPS_BEIDOU_GLONASS,
                 csv_out=None,
                 no_LCD=False):
  """
  Lit les données GNSS et affiche la position du module GNSS sur l'invité de commandes et le LCD.

  Arguments:
  - mode: Mode de fonctionnement du module GNSS. Valeur par défaut à GPS_BEIDOU_GLONASS.
  - csv_out: Le chemin et nom de fichier CSV pour l'enregistrement des acquisitions GNSS.
             S'il n'est pas défini, aucun enregistrement n'est effectué.
  - no_LCD: Booléen optionnel indiquant si on ne veut pas utiliser le LCD. Valeur par défaut à False.
  """

  gnss = GNSS(1, GNSS_DEVICE_ADDR)
  gnss.initialisation(mode)
  save_csv=False
  if csv_out is not None:
    save_csv=True
    if not(csv_out.endswith('.csv')):
      csv_out +='.csv'
    record = CSVHandler(csv_out)
    record.create_csv_with_header(['Timestamp','UTC','Latitude','Longitude'])

  if not(no_LCD):
    lcd_display = LCD(LCD_DEVICE_ADDR)

  try:
    while True:
      # Actualisation des données GNSS
      gnss.wait_for_next_scan()  # Attend que le GNSS obtienne le scan suivant
      gnss.update()
      if save_csv and gnss.reception_ok:
        record.append_row([gnss.timestamp,gnss.utc,gnss.latitude.coordinates_DD,gnss.longitude.coordinates_DD])

      # A COMPLETER
      latitude = gnss.latitude.coordinates_DMM
      longitude = gnss.longitude.coordinates_DMM

      # Affichage sur le LCD
      if gnss.reception_ok:
        if not(no_LCD):
          # A COMPLETER
          lcd_display.afficher(...)
      else:
        if not(no_LCD):
          lcd_display.afficher("Recherche de    signal GNSS...")

      # Affichage sur console
      if gnss.reception_ok:
        print("--------------------------------------------------------------")
        print(f"Nombre de satellites utilisés: {gnss.number_satellites}")
        print(f"Latitude : {latitude}")
        print(f"Longitude : {longitude}")
        print("")
      else:
        print("Recherche de signal GNSS...")

  except KeyboardInterrupt as e:
    print("Arrêt du programme")
    if not(no_LCD):
      lcd_display.effacer()
