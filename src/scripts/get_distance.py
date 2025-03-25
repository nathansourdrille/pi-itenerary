from core.gnss_distance import get_distance
import argparse
from config import GPS_BEIDOU_GLONASS        

if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('latitude', 
                        type=float,
                        help="Latitude du point d'intérêt (en degrés décimaux)")
    parser.add_argument('longitude', 
                        type=float,
                        help="Longitude du point d'intérêt (en degrés décimaux)")
    args = parser.parse_args()
	
    get_distance((args.latitude,args.longitude),mode=GPS_BEIDOU_GLONASS)

