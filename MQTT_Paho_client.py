import paho.mqtt.client as mqtt
import time


#model_client = mqtt.client(client_id="PythonModel", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
#model_client.username_pw_set('Ivan',password = 'alpamayo')

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

mqtt.Client.connected_flag=False#create flag in class
broker="127.0.0.1"
port=1883
client = mqtt.Client("python1")             #create new instance
client.username_pw_set('Ivan',password = 'alpamayo') #configure user and password for MQTT broker connection
client.on_connect=on_connect  #bind call back function
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
client.on_publish = on_publish                         #assign function to callback
client.loop_start()
print("Connecting to broker ",broker)
client.connect(broker,port)      #connect to broker
n_atmp=0
while not client.connected_flag and n_atmp<10: #wait in loop while not connected
    print("In wait loop ",n_atmp," attempt")
    time.sleep(1)
    n_atmp+=1
print("in Main Loop")
ret= client.publish("bulb1","on") #publish

client.loop_stop()    #Stop loop 
client.disconnect() # disconnect