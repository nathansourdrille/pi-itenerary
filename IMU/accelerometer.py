import smbus
import time

# Registres pour l'accéléromètre
# A COMPLETER
CTRL1_XL = 0x10
OUTX_L_A = 0x28
DICT_FREQ = {12.5 : 0b0001 , 26 : 0b0010 , 52 : 0b0011 , 104 : 0b0100, 208 : 0b0101, 416 :0b0110, 833 : 0b0111, 1660 : 0b1000, 3330 : 0b1001, 6660 : 0b1010 } 
DICT_RANGE = {2 : 0b00, 4 : 0b10, 8 : 0b11, 16 : 0b01}
DICT_RANGE_FACTOR = {2:0.061,4:0.122,8:0.244,16:0.488}
def accelerometer_configuration(accel_range, accel_freq):
    """
    Configure les paramètres du LSM6DSO pour l'accéléromètre.

    Arguments: 
    - accel_range: la range de l'accélérateur
    - accel_freq: la fréquence d'acquisition de l'accélérateur

    Résultat : l'octet à écrire dans le registre CTRL1_XL pour configurer l'accéléromètre
    """
    # Configuration de l'accéléromètre
    # A COMPLETER

    return (DICT_FREQ[accel_freq] * 2**4 + DICT_RANGE[accel_range] * 2**2)

def read_accelerometer(accel_range):
    """
    Lit les données de l'accéléromètre et les convertit.

    Arguments: 
    - accel_range: la range de l'accéléromètre

    Résultat: les données acquises par de l'accéléromètre en unité physique sur les 3 axes
    """
    from IMU import read_raw_data, LSM6DSO_ADDR
    x, y, z = read_raw_data(LSM6DSO_ADDR, OUTX_L_A)

    # A COMPLETER
    sensitivity = DICT_RANGE_FACTOR[accel_range]/1000
    return x * sensitivity, y * sensitivity, z * sensitivity

