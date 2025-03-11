import smbus
import time

# Registres pour le gyroscope
# A COMPLETER
CTRL2_G = 0x11
OUTX_L_G = 0x22
DICT_FREQ = {12.5 : 0b0001 , 26 : 0b0010 , 52 : 0b0011 , 104 : 0b0100, 208 : 0b0101, 416 :0b0110, 833 : 0b0111, 1660 : 0b1000, 3330 : 0b1001, 6660 : 0b1010 } 
DICT_RANGE = {250 : 0b00, 500 : 0b01, 1000 : 0b10, 2000 : 0b11}
DICT_RANGE_FACTOR = {250:8.75,500:17.5,1000:35,2000:70}

def gyroscope_configuration(gyro_range, gyro_freq):
    """
    Configure les paramètres du LSM6DSO pour le gyroscope.

    Arguments: 
    - gyro_range: la range du gyroscope
    - gyro_freq: la fréquence d'acquisition du gyroscope

    Résultat : l'octet à écrire dans le registre CTRL2_G pour configurer le gyroscope
    """
    # Configuration du gyroscope
    # A COMPLETER
    return (DICT_FREQ[gyro_freq] * 2**4 + DICT_RANGE[gyro_range] * 2**2)

def read_gyroscope(gyro_range):
    """
    Lit les données du gyroscope et les convertit.

    Arguments: 
    - gyro_range: la range du gyroscope

    Résultat: les données acquises par le gyroscope en unité physique sur les 3 axes
    """
    from IMU import read_raw_data, LSM6DSO_ADDR
    x, y, z = read_raw_data(LSM6DSO_ADDR, OUTX_L_G)
    
    # A COMPLETER
    sensitivity = DICT_RANGE_FACTOR[gyro_range]/1000
    return x * sensitivity, y * sensitivity, z * sensitivity
