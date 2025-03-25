from config import GPS_BEIDOU_GLONASS,GPS_GLONASS,BEIDOU_GLONASS,GPS_BEIDOU,GLONASS,GPS,BEIDOU, CONFIG_MAG_FREQ, CONFIG_MAG_RANGE, CONFIG_ACCELEROMETER_FREQ, CONFIG_ACCELEROMETER_RANGE, CONFIG_GYRO_RANGE

# Paramètres du GNSS
MODE_GNSS = GPS_BEIDOU_GLONASS

# Paramètres de l'IMU
ACCEL_RANGE= CONFIG_ACCELEROMETER_RANGE[4]                  # Plage de mesure de l'accéléromètre (g)
ACCEL_FREQ= CONFIG_ACCELEROMETER_FREQ[208]                   # Fréquence d'échantillonnage de l'accéléromètre (Hz)
GYRO_RANGE= CONFIG_GYRO_RANGE[500]                   # Plage de mesure du gyroscope (dps)
GYRO_FREQ= CONFIG_ACCELEROMETER_FREQ[208]                   # Fréquence d'échantillonnage du gyroscope (Hz)
MAGNETO_RANGE= 8              # Plage de mesure du magnétomètre (gauss)
MAGNETO_FREQ= 20              # Fréquence d'échantillonnage du magnétomètre (Hz)

# Paramètres du LiDAR
MIN_ANGLE=...                    # Angle minimal du scan en degrés
MAX_ANGLE=...                    # Angle maximal du scan en degrés
QUALITY_THRESHOLD=...            # Seuil de qualité des mesures du LiDAR (entre 0 et 15)
SCAN_SKIP = 3                    # Ignorer X scans pour alléger l'affichage (via stream_scan.py)
