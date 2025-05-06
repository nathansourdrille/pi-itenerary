import csv
import time
from config.constants import GNSS_DEVICE_ADDR, LCD_DEVICE_ADDR, GPS_BEIDOU_GLONASS, LSM6DSO_ADDR, LIS3MDL_ADDR
from sensors.GNSS import GNSS
from sensors.IMU import read_IMU, initialize_sensors
from utils import LCD
from core.gnss_distance import compute_distance, format_distance
import math

def compute_relative_direction(target_bearing, imu_heading):
    """
    Calcule la direction relative à suivre en fonction de l'orientation du joueur.
    Retourne la direction cardinale et l'angle de différence.
    """
    difference = (target_bearing - imu_heading + 360) % 360

    if difference < 22.5 or difference >= 337.5:
        return "devant vous", "↑"
    elif 22.5 <= difference < 67.5:
        return "devant à droite", "↗"
    elif 67.5 <= difference < 112.5:
        return "à droite", "→"
    elif 112.5 <= difference < 157.5:
        return "derrière à droite", "↘"
    elif 157.5 <= difference < 202.5:
        return "derrière vous", "↓"
    elif 202.5 <= difference < 247.5:
        return "derrière à gauche", "↙"
    elif 247.5 <= difference < 292.5:
        return "à gauche", "←"
    else:
        return "devant à gauche", "↖"

def get_imu_heading():
    """
    Lit les données du magnétomètre pour déterminer l'orientation du joueur.
    Retourne l'angle en degrés (0-360) par rapport au nord magnétique.
    """
    _, _, _, _, _, _, mag_x, mag_y, _ = read_IMU(LSM6DSO_ADDR, LIS3MDL_ADDR, 4, 1000, 2000, 104, 4)

    heading = math.degrees(math.atan2(mag_y, mag_x))
    heading = (heading + 360) % 360

    return heading

def load_checkpoints(csv_file):
    """Charge les points de passage depuis un fichier CSV."""
    checkpoints = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                try:
                    lat = float(row[0])
                    lon = float(row[1])
                    checkpoints.append((lat, lon))
                except ValueError:
                    continue
    return checkpoints

def orientation_game(checkpoint_file):
    """
    Jeu de course d'orientation utilisant GNSS pour la position et IMU pour l'orientation.
    """
    checkpoints = load_checkpoints(checkpoint_file)
    if not checkpoints:
        print("Aucun point de passage valide trouvé dans le fichier.")
        return

    gnss = GNSS(1, GNSS_DEVICE_ADDR)
    gnss.initialisation(GPS_BEIDOU_GLONASS)
    lcd_display = LCD(LCD_DEVICE_ADDR)
    initialize_sensors(LSM6DSO_ADDR, LIS3MDL_ADDR, 4, 104, 1000, 104, 4, 20)

    current_checkpoint = 0
    total_checkpoints = len(checkpoints)

    try:
        while current_checkpoint < total_checkpoints:
            target = checkpoints[current_checkpoint]

            while True:
                gnss.update()

                if not gnss.reception_ok:
                    lcd_display.afficher("Recherche de    signal GNSS...")
                    time.sleep(1)
                    continue

                current_pos = (gnss.latitude.coordinates_DD, gnss.longitude.coordinates_DD)
                distance = compute_distance(current_pos, target)

                imu_heading = get_imu_heading()
                target_bearing = compute_bearing(current_pos, target)
                direction_text, direction_arrow = compute_relative_direction(target_bearing, imu_heading)

                lcd_line1 = f"P{current_checkpoint+1}/{total_checkpoints} {direction_arrow}"
                lcd_line2 = f"{format_distance(distance)}"
                lcd_display.afficher(f"{lcd_line1}\n{lcd_line2}")

                print("\n" * 5)
                print("=== COURSE D'ORIENTATION ===")
                print(f"Point {current_checkpoint+1}/{total_checkpoints}")
                print(f"Distance: {format_distance(distance)}")
                print(f"Direction: {direction_text} ({direction_arrow})")
                print(f"Orientation: {imu_heading:.1f}°")
                print(f"Vers: {target_bearing:.1f}°")
                print(f"Position: {current_pos[0]:.6f}, {current_pos[1]:.6f}")

                if distance < 5:
                    lcd_display.afficher(f"Point {current_checkpoint+1} atteint!")
                    print(f"\nPoint {current_checkpoint+1} atteint!")
                    time.sleep(3)
                    current_checkpoint += 1
                    break

                time.sleep(0.5)

        lcd_display.afficher("Course terminee! Felicitations!")
        print("\nCourse terminée! Félicitations!")
        time.sleep(5)

    except KeyboardInterrupt:
        print("Arrêt du programme")
    finally:
        lcd_display.effacer()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Jeu de course d'orientation avec GNSS et IMU")
    parser.add_argument('checkpoints_file', type=str, help="Fichier CSV des points de passage (lat,lon)")
    args = parser.parse_args()

    orientation_game(args.checkpoints_file)
