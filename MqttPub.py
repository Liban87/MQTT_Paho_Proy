import paho.mqtt.client as mqtt
import pandas as pd
import json
import joblib
import time
from sklearn.ensemble import RandomForestClassifier
import xgboost
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

def send_dataframe_rows_broker(broker_address, topic, file_path, model_path):
    # Cargar el archivo xlsx como un DataFrame
    df = pd.read_excel(file_path)

    # Cargar el modelo desde el archivo .pkl
    model = joblib.load(model_path)
    model = model[0]

    # Crear un cliente MQTT
    client = mqtt.Client()

    # Conectar al broker MQTT
    client.connect(broker_address)

    # Iterar sobre las filas del DataFrame
    d = {0:'No Consumption', 1:'Sub metering 2', 2:'Sub metering 3', 3:'Equal' }
    
    for _, row in df.iterrows():
        # Obtener las características de la fila como una matriz NumPy
        features = pd.DataFrame(row.values.reshape(1, -1), columns = df.columns.tolist())

        # Realizar la predicción con el modelo cargado
        prediction = model.predict(features)
        prediction = d[int(prediction)]        
        probability = model.predict_proba(features)[0]

        # Crear un diccionario con los resultados
        result = {
            'PotAct': features.loc[0, 'Global_active_power'],
            'PotReact': features.loc[0, 'Global_reactive_power'],
            'Volt': features.loc[0, 'Voltage'],
            'Int': features.loc[0, 'Global_intensity'],
            'prediction': prediction,
            'probability': probability.tolist()
        }

        # Convertir el diccionario en una cadena JSON
        payload = json.dumps(result)

        # Publicar los resultados en el topic especificado
        client.publish(topic, payload)

        # Esperar 1 minuto
        time.sleep(5)

    # Desconectar del broker MQTT
    #client.disconnect()

broker_address = "test.mosquitto.org"
topic = "ALSW/Prediccion"
file_path = "C:/Users/ander/Desktop/UAM/Doctorado/Industria 4.0/Final/Data/produccion.xlsx"
model_path = "C:/Users/ander/Desktop/UAM/Doctorado/Industria 4.0/Final/Modelo/Model.pkl"

send_dataframe_rows_broker(broker_address, topic, file_path, model_path)


#client = mqtt.Client()
#client.connect("test.mosquitto.org", 1883, 60)
#client.publish("ALSW/temp", "99")
