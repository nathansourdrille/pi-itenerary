from core.gnss_position import get_position
import argparse
from config import GPS_BEIDOU_GLONASS

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--no-LCD', 
                      action='store_true',
                      help="Permet de ne rien afficher sur le LCD.")
  parser.add_argument('--save-path', '-s',
                      type=str,
                      default=None,
                      help="Chemin où sauvegarder les données."
    )
  args = parser.parse_args()
  
  get_position(mode=GPS_BEIDOU_GLONASS,csv_out=args.save_path,no_LCD=args.no_LCD)