import argparse
from multiprocessing import Process
import os
from config import (
    GPS_BEIDOU_GLONASS,
    LSM6DSO_ADDR, LIS3MDL_ADDR,
    ACCEL_RANGE, ACCEL_FREQ,
    GYRO_RANGE, GYRO_FREQ,
    MAGNETO_RANGE, MAGNETO_FREQ
)
from core.gnss_position import get_position
from core.imu_acquisition import get_imu_data
import time

# Dossiers prédéfinis pour sauvegarder les fichiers d'acquisition GNSS et IMU
GNSS_SAVE_DIR = "../results/acquisitionsGPS/"
IMU_SAVE_DIR = "../results/acquisitionsIMU/"

def ensure_dir_exists(directory):
    """Crée le dossier spécifié s'il n'existe pas."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def run_gnss_acquisition(save_path=None, no_LCD=False):
    """
    Lance l'acquisition GNSS.
    - save_path : chemin du fichier CSV où sauvegarder les données.
    - no_LCD : booléen, si True, n'affiche rien sur le LCD.
    """
    get_position(mode=GPS_BEIDOU_GLONASS, csv_out=save_path, no_LCD=no_LCD)

def run_imu_acquisition(save_path=None):
    """
    Lance l'acquisition IMU avec les paramètres importés de config.
    - save_path : chemin du fichier CSV où sauvegarder les données.
    """
    get_imu_data(
        LSM6DSO_ADDR, LIS3MDL_ADDR,
        ACCEL_RANGE, ACCEL_FREQ,
        GYRO_RANGE, GYRO_FREQ,
        MAGNETO_RANGE, MAGNETO_FREQ,
        save_path
    )

if __name__ == "__main__":
    # S'assure que les dossiers de sauvegarde existent avant d'écrire dedans
    ensure_dir_exists(GNSS_SAVE_DIR)
    ensure_dir_exists(IMU_SAVE_DIR)

    # Gestion des arguments en ligne de commande
    parser = argparse.ArgumentParser(description="Script pour lancer simultanément l'acquisition GNSS et IMU")
    parser.add_argument('--no-LCD',
                        action='store_true',
                        help="Ne rien afficher sur le LCD pour le GNSS")
    parser.add_argument('--base-filename',
                        type=str,
                        default=None,
                        help="Nom de base pour les fichiers de sortie (sans extension)")

    args = parser.parse_args()

    # Préparer les chemins complets des fichiers si un nom de base est donné
    gnss_save_path = None
    imu_save_path = None

    if args.base_filename:
        # Génère un timestamp de type AAAAMMJJ pour éviter d'écraser les fichiers existants
        timestamp = time.strftime("%Y%m%d")
        filename = f"{args.base_filename}_{timestamp}" if args.base_filename else timestamp

        # Crée les noms complets des fichiers CSV
        gnss_save_path = os.path.join(GNSS_SAVE_DIR, f"{filename}_gnss.csv")
        imu_save_path = os.path.join(IMU_SAVE_DIR, f"{filename}_imu.csv")

    # Création de deux processus distincts pour lancer en parallèle les acquisitions GNSS et IMU
    gnss_process = Process(
        target=run_gnss_acquisition,
        kwargs={'save_path': gnss_save_path, 'no_LCD': args.no_LCD}
    )

    imu_process = Process(
        target=run_imu_acquisition,
        kwargs={'save_path': imu_save_path}
    )

    # Démarrage des deux processus
    gnss_process.start()
    imu_process.start()

    try:
        # Attend la fin des deux processus
        gnss_process.join()
        imu_process.join()
    except KeyboardInterrupt:
        # En cas d'interruption utilisateur (Ctrl+C), on arrête proprement les processus enfants
        print("\nArrêt demandé par l'utilisateur...")
        gnss_process.terminate()
        imu_process.terminate()
        gnss_process.join()
        imu_process.join()
        print("Processus arrêtés.")
