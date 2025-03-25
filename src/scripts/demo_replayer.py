from core.replayer import simulate_from_csv, print_data_callback

"""
Script pour une démo d'un replayer, c'est-à-dire un code pour simuler les données 
en temps réel à partir d'un fichier CSV d'acquisition.
"""

if __name__ == '__main__':
    csv_path = ... # Chemin du fichier CSV à simuler
    simulate_from_csv(csv_path, print_data_callback, speed_factor=1.0)