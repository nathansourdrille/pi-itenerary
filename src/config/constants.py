# Adresses I2C et USB des composants
PORT_LIDAR = ...                 # Port USB connecté au LiDAR
PORT_BUZZER = ...                # Port GPIO du buzzer
LSM6DSO_ADDR = 0x6b               # Adresse I2C du capteur LSM6DSO (Accéléromètre/Gyroscope)
LIS3MDL_ADDR = 0x1E               # Adresse I2C du capteur LIS3MDL (Magnétomètre)
GNSS_DEVICE_ADDR = 0x20           # Adresse I2C du module GNSS
LCD_DEVICE_ADDR = 0x27
            # Adresse I2C de l'écran LCD

# Constantes des registres du GNSS
I2C_START_GET = 29
I2C_ID = 30
I2C_DATA_LEN_H = 31
I2C_DATA_LEN_L = 32
I2C_ALL_DATA = 33
I2C_GNSS_MODE = 34
I2C_SLEEP_MODE = 35

# Mode de sélection des satellites GNSS
GPS = 1
BEIDOU = 2
GPS_BEIDOU = 3
GLONASS = 4
GPS_GLONASS = 5
BEIDOU_GLONASS = 6
GPS_BEIDOU_GLONASS = 7

# Constantes des registres de configuration de l'IMU
CTRL1_XL = 0x10                   # Registre de configuration de l'accéléromètre
CTRL2_G = 0x11                    # Registre de configuration du gyroscope
CTRL_REG1 = 0x20                  # Registre de configuration du magnétomètre (fréquence d'acquisition)
CTRL_REG2 = 0x21                  # Registre de configuration du magnétomètre (plage d'acquisition)
OUTX_L_A = 0x28                   # Registre de lecture de l'accéléromètre
OUTX_L_G = 0x22                   # Registre de lecture du gyroscope
OUT_X_L = 0x28                    # Registre de lecture du magnétomètre

# Constantes de configuration du LiDAR
MIN_RANGE = ...                  # Portée minimale du LiDAR en mm
MAX_RANGE = ...                  # Portée maximale du LiDAR en mm

# Mappages des fréquences (Hz) pour le magnétomètre
CONFIG_MAG_FREQ = {
    0.625: 0b000000,
    1.25: 0b000010,
    2.5: 0b000100,
    5: 0b000110,
    10: 0b001000,
    20: 0b001010,
    40: 0b001100,
    80: 0b001110,
    155: 0b110001,
    300: 0b100001,
    560: 0b010001,
    1000: 0b000001,
}

# Mappages des plages (full-scale range) pour le magnétomètre
CONFIG_MAG_RANGE = {
    4: 0,   # ±4 gauss
    8: 1,   # ±8 gauss
    12: 2,   # ±12 gauss
    16: 3,   # ±16 gauss
}

# Sensibilités du magnétomètre pour conversion des données brutes en unités physiques
CONFIG_MAG_SENSITIVITY = {
    4: 6842,   # LSB/gauss
    8: 3421,   # LSB/gauss
    12: 2281,   # LSB/gauss
    16: 1711,  # LSB/gauss
}

CONFIG_ACCELEROMETER_FREQ = {
    12.5 : 0b0001 ,
    26 : 0b0010 ,
    52 : 0b0011 ,
    104 : 0b0100,
    208 : 0b0101,
    416 :0b0110,
    833 : 0b0111,
    1660 : 0b1000,
    3330 : 0b1001,
    6660 : 0b1010 }

CONFIG_ACCELEROMETER_RANGE = {
    2 : 0b00,
    4 : 0b10,
    8 : 0b11,
    16 : 0b01}

DICT_RANGE_FACTOR = {2:0.061,4:0.122,8:0.244,16:0.488}

CONFIG_GYRO_RANGE = {
    250 : 0b00,
    500 : 0b01,
    1000 : 0b10,
    2000 : 0b11
}
