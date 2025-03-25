from config import GPS_BEIDOU_GLONASS,GPS_GLONASS,BEIDOU_GLONASS,GPS_BEIDOU,GLONASS,GPS,BEIDOU

# Paramètres du GNSS
MODE_GNSS = GPS_BEIDOU_GLONASS

# Paramètres de l'IMU
ACCEL_RANGE=...                  # Plage de mesure de l'accéléromètre (g)
ACCEL_FREQ=...                   # Fréquence d'échantillonnage de l'accéléromètre (Hz)  
GYRO_RANGE=...                   # Plage de mesure du gyroscope (dps)
GYRO_FREQ=...                    # Fréquence d'échantillonnage du gyroscope (Hz)
MAGNETO_RANGE=...                # Plage de mesure du magnétomètre (gauss)
MAGNETO_FREQ=...                 # Fréquence d'échantillonnage du magnétomètre (Hz)

# Paramètres du LiDAR
MIN_ANGLE=...                    # Angle minimal du scan en degrés
MAX_ANGLE=...                    # Angle maximal du scan en degrés
QUALITY_THRESHOLD=...            # Seuil de qualité des mesures du LiDAR (entre 0 et 15)
SCAN_SKIP = 3                    # Ignorer X scans pour alléger l'affichage (via stream_scan.py)