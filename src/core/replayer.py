import pandas as pd
import time

def print_data_callback(ts, data):
    """
    Fonction callback qui affiche les données dès qu'elles arrivent.

    Arguments:
    - ts: Timestamp des données
    - data: Tuple contenant les données acquises à l'instant timestamp
    """
    print(f"[{ts:.3f}] → {data}")

def simulate_from_csv(csv_path, callback, speed_factor=1.0):
    """
    Simule un flux de données à partir d'un fichier CSV.

    Arguments:
    - csv_path: Chemin du fichier CSV avec un timestamp en première colonne (format UNIX time).
    - callback: Fonction appelée à chaque ligne du CSV. Signature: callback(timestamp, row_data_dict)
    - speed_factor: >1 accélère, <1 ralentit, 1 = temps réel.
    """
    df = pd.read_csv(csv_path)
    df.columns = [col.strip() for col in df.columns]

    if len(df.columns) < 2:
        raise ValueError("Le fichier CSV doit avoir au moins deux colonnes (timestamp + données).")

    # Extraction du temps initial
    timestamps = df.iloc[:, 0].astype(float).values
    start_time = time.time() 

    for i in range(len(df)):
        current_time = time.time()
        simulated_timestamp = timestamps[i]

        # Envoie les données à l'utilisateur
        data = df.iloc[i, 1:].to_dict()
        callback(simulated_timestamp, data)

        if i < len(df) - 1:
            wait = (simulated_timestamp - timestamps[0]) / speed_factor + start_time - current_time
            if wait > 0:
                time.sleep(wait)

