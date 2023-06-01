import paho.mqtt.client as mqtt
import pandas as pd
import json
import joblib
import time
from sklearn.ensemble import RandomForestClassifier
import xgboost
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

def send_dataframe_rows_broker(broker_address, port, topic, file_path, model_path):
    # Cargar el archivo xlsx como un DataFrame
    df = pd.read_excel(file_path)
  
    # Cargar el modelo desde el archivo .pkl
    model = joblib.load(model_path)
    model = model[1]

    # Crear un cliente MQTT
    client = mqtt.Client("Python1")
    client.username_pw_set('Ivan',password = 'alpamayo') #configure user and password for MQTT broker connection

    # Conectar al broker MQTT
    client.connect(broker_address,port)

    # Iterar sobre las filas del DataFrame
    d = {0:'Sin Consumo', 1:'Zona 2', 2:'Zona 3', 3:'Igual' }
  
    for _, row in df.iterrows():
        # Obtener las características de la fila como una matriz NumPy
        features = pd.DataFrame(row.values.reshape(1, -1), columns = df.columns.tolist())
        # Realizar la predicción con el modelo cargado
        prediction = model.predict(features)
        ind = np.argmax(prediction)
        prediction = d[ind]        
        probability = model.predict_proba(features)[0] #.max()

        # Crear un diccionario con los resultados
        result = {'PotAct': features.loc[0, 'Global_active_power'],
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
        time.sleep(20)

    #Desconectar del broker MQTT
    client.disconnect()

broker_address = "127.0.0.1"
port=1883
topic = "Prediccion"
file_path ="./Data/produccion.xlsx"
model_path ="./Modelo/Model.pkl"
#file_path = "C:/Users/ander/Desktop/UAM/Doctorado/Industria 4.0/Final/produccion.xlsx"
#model_path = "C:/Users/ander/Desktop/UAM/Doctorado/Industria 4.0/Final/Model.pkl"

send_dataframe_rows_broker(broker_address, port, topic, file_path, model_path)