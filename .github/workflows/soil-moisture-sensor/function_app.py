import azure.functions as func
import datetime
import json
import logging
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
app = func.FunctionApp()
CONNECTION_STRING = "HostName=PlantManager.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=PXXIxkimG0ubmJ/z1/wByylingHiNDdxHAIoTJz9dB0="
DEVICE_ID = "Moisture-sensor"
METHOD_NAME = "relay_on"
METHOD_PAYLOAD = ""

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="eventhubname",
                               connection="EventHubConnectionString") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))
    dictionary=json.loads(azeventhub.get_body().decode('utf-8'))     
    number=dictionary["soil_moisture"] 
    registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
    if number>450:  
       # Call the direct method.
        deviceMethod = CloudToDeviceMethod(method_name="relay_on", payload="")
        response = registry_manager.invoke_device_method(DEVICE_ID, deviceMethod)
    else:
        deviceMethod = CloudToDeviceMethod(method_name="relay_off", payload="")
        response = registry_manager.invoke_device_method(DEVICE_ID, deviceMethod)
