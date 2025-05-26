import argparse
from multiprocessing import Process, Queue
import os
from config import (
    GPS_BEIDOU_GLONASS,
    LSM6DSO_ADDR, LIS3MDL_ADDR,
    ACCEL_RANGE, ACCEL_FREQ,
    GYRO_RANGE, GYRO_FREQ,
    MAGNETO_RANGE, MAGNETO_FREQ
)
from core.gnss_position_kalman import get_position
from core.imu_acquisition_kalman import get_imu_data
import time
import numpy as np
from scipy.spatial.transform import Rotation as R

# Dossiers prédéfinis pour les sauvegardes
GNSS_SAVE_DIR = "../results/acquisitionsGPS/"
IMU_SAVE_DIR = "../results/acquisitionsIMU/"

def ensure_dir_exists(directory):
    """Crée le dossier s'il n'existe pas"""
    if not os.path.exists(directory):
        os.makedirs(directory)

class KalmanFilterRealTime:
    def __init__(self, initial_magneto, initial_gps):
        self.dt = 1.0  # intervalle de temps en secondes

        # Matrices du filtre de Kalman
        self.F = np.array([
            [1, 0, 0, self.dt, 0, 0],
            [0, 1, 0, 0, self.dt, 0],
            [0, 0, 1, 0, 0, self.dt],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
        ])

        self.B = np.array([
            [0.5 * self.dt**2, 0, 0],
            [0, 0.5 * self.dt**2, 0],
            [0, 0, 0.5 * self.dt**2],
            [self.dt, 0, 0],
            [0, self.dt, 0],
            [0, 0, self.dt],
        ])

        self.H = np.zeros((3, 6))
        self.H[0, 0] = 1
        self.H[1, 1] = 1
        self.H[2, 2] = 1

        # Initialisation de l'état
        Rt = 6371000  # Rayon de la Terre en mètres
        x = Rt * np.cos(np.radians(initial_gps['lat'])) * np.cos(np.radians(initial_gps['lon']))
        y = Rt * np.cos(np.radians(initial_gps['lat'])) * np.sin(np.radians(initial_gps['lon']))
        z = Rt * np.sin(np.radians(initial_gps['lat']))

        self.state_mean = np.array([x, y, z, 0, 0, 0])
        self.state_cov = np.eye(6) * 0.1

        # Initialisation des angles à partir du magnétomètre
        w0 = np.array(initial_magneto)
        norme_w0 = np.linalg.norm(w0)
        self.theta_x = np.arccos(w0[0] / norme_w0)
        self.theta_y = np.arccos(w0[1] / norme_w0)
        self.theta_z = np.arccos(w0[2] / norme_w0)

        self.transition_covariance = np.eye(6) * 0.01
        self.observation_covariance = np.eye(3) * 1

    def predict(self, accel, gyro):
        # Mise à jour des angles avec le gyroscope
        self.theta_x += gyro[0]
        self.theta_y += gyro[1]
        self.theta_z += gyro[2]

        # Correction de l'accélération avec les angles actuels
        w = np.array([self.theta_x, self.theta_y, self.theta_z])
        angle = np.linalg.norm(w)
        if angle != 0:
            axis = -w / angle
            rot = R.from_rotvec(axis * angle)
            accel_corr = rot.apply(accel)
        else:
            accel_corr = accel

        # Prédiction
        self.state_mean = self.F @ self.state_mean + self.B @ accel_corr
        self.state_cov = self.F @ self.state_cov @ self.F.T + self.transition_covariance

        return self.state_mean[:3]  # Retourne la position prédite

    def update(self, gps_data):
        Rt = 6371000
        x = Rt * np.cos(np.radians(gps_data['lat'])) * np.cos(np.radians(gps_data['lon']))
        y = Rt * np.cos(np.radians(gps_data['lat'])) * np.sin(np.radians(gps_data['lon']))
        z = Rt * np.sin(np.radians(gps_data['lat']))
        observation = np.array([x, y, z])

        # Innovation
        y = observation - self.H @ self.state_mean
        S = self.H @ self.state_cov @ self.H.T + self.observation_covariance
        K = self.state_cov @ self.H.T @ np.linalg.inv(S)

        # Mise à jour
        self.state_mean = self.state_mean + K @ y
        self.state_cov = (np.eye(6) - K @ self.H) @ self.state_cov

        return self.state_mean  # Retourne l'état complet mis à jour

def run_gnss_acquisition(save_path=None, no_LCD=False, kalman_queue=None, kalman_mode=False):
    get_position(mode=GPS_BEIDOU_GLONASS, csv_out=save_path, no_LCD=no_LCD,
                kalman_queue=kalman_queue, kalman_mode=kalman_mode)

def run_imu_acquisition(save_path=None, kalman_queue=None, kalman_mode=False):
    get_imu_data(
        LSM6DSO_ADDR, LIS3MDL_ADDR,
        ACCEL_RANGE, ACCEL_FREQ,
        GYRO_RANGE, GYRO_FREQ,
        MAGNETO_RANGE, MAGNETO_FREQ,
        save_path,
        kalman_queue=kalman_queue,
        kalman_mode=kalman_mode
    )

def run_kalman_filter(imu_queue, gnss_queue):
    # Attendre les premières données pour initialiser
    initial_magneto = imu_queue.get()
    initial_gps = gnss_queue.get()

    kf = KalmanFilterRealTime(initial_magneto, initial_gps)

    while True:
        # Vérifier les nouvelles données IMU pour la prédiction
        while not imu_queue.empty():
            imu_data = imu_queue.get()
            accel = np.array([imu_data['accel_x'], imu_data['accel_y'], imu_data['accel_z']])
            gyro = np.array([imu_data['gyro_x'], imu_data['gyro_y'], imu_data['gyro_z']])
            predicted_pos = kf.predict(accel, gyro)
            print(f"Position prédite: {predicted_pos}")

        # Vérifier les nouvelles données GNSS pour la mise à jour
        while not gnss_queue.empty():
            gps_data = gnss_queue.get()
            updated_state = kf.update(gps_data)
            print(f"Position mise à jour: {updated_state[:3]}")
            print(f"Vitesse: {updated_state[3:6]}")

if __name__ == "__main__":
    # Créer les dossiers s'ils n'existent pas
    ensure_dir_exists(GNSS_SAVE_DIR)
    ensure_dir_exists(IMU_SAVE_DIR)

    parser = argparse.ArgumentParser(description="Script pour lancer simultanément l'acquisition GNSS et IMU")
    parser.add_argument('--no-LCD',
                       action='store_true',
                       help="Ne rien afficher sur le LCD pour le GNSS")
    parser.add_argument('--base-filename',
                       type=str,
                       default=None,
                       help="Nom de base pour les fichiers de sortie (sans extension)")
    parser.add_argument('-k', '--kalman',
                       action='store_true',
                       help="Activer le filtre de Kalman en temps réel")

    args = parser.parse_args()

    # Construire les chemins complets si un nom de base est fourni
    gnss_save_path = None
    imu_save_path = None

    if args.base_filename:
        timestamp = time.strftime("%Y%m%d")
        filename = f"{args.base_filename}_{timestamp}" if args.base_filename else timestamp
        gnss_save_path = os.path.join(GNSS_SAVE_DIR, f"{filename}_gnss.csv")
        imu_save_path = os.path.join(IMU_SAVE_DIR, f"{filename}_imu.csv")

    # Création des queues pour le filtre de Kalman si activé
    imu_queue = None
    gnss_queue = None
    kalman_process = None

    if args.kalman:
        imu_queue = Queue()
        gnss_queue = Queue()
        kalman_process = Process(target=run_kalman_filter, args=(imu_queue, gnss_queue))
        kalman_process.start()

    # Création des processus
    gnss_process = Process(
        target=run_gnss_acquisition,
        kwargs={
            'save_path': gnss_save_path,
            'no_LCD': args.no_LCD,
            'kalman_queue': gnss_queue,
            'kalman_mode': args.kalman
        }
    )

    imu_process = Process(
        target=run_imu_acquisition,
        kwargs={
            'save_path': imu_save_path,
            'kalman_queue': imu_queue,
            'kalman_mode': args.kalman
        }
    )

    gnss_process.start()
    imu_process.start()

    try:
        gnss_process.join()
        imu_process.join()
        if args.kalman:
            kalman_process.join()
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur...")
        gnss_process.terminate()
        imu_process.terminate()
        if args.kalman:
            kalman_process.terminate()
        gnss_process.join()
        imu_process.join()
        if args.kalman:
            kalman_process.join()
        print("Processus arrêtés.")
