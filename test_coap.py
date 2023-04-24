import logging
import asyncio

from aiocoap import *

# put your board's IP address here
ESP32_IP = "ESP32-TEMP-LINK"

# un comment the type of test you want to execute
TEST = "GET"
#TEST = "PUT"
#TEST = "DELETE"

#PAYLOAD = b"tie"
#PAYLOAD = b"untie"

#URI = "temp/frijol"
#URI = "temp/zan"
#URI = "temp/calabaza"
#URI = "temp/maiz"

URI = "temp/frijol"
PAYLOAD = b"CLIENT-TEMP"

logging.basicConfig(level=logging.INFO)

async def get(ip, uri):
    protocol = await Context.create_client_context()
    request = Message(code = GET, uri = 'coap://' + ip + '/' +  uri)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Incoming data from Coap Server:')
        print('Result: %s\n%r'%(response.code, response.payload))

    # Change the payload into a float
    temperature = float(response.payload.decode())

    #Compare the current temperature
    print('\r\nComparing current temperature:')

    if(temperature < 5.0):
        print('Temperature is OK: Not Action required in field: ')
    if(temperature > 5.0):
        print('Temperature is getting high: Please irrigate the field zone: ')
    print(URI)
    print('Current temperature')
    print(temperature)


async def put(ip, uri, payload):
    context = await Context.create_client_context()
    await asyncio.sleep(2)
    request = Message(code = PUT, payload = payload, uri = 'coap://' + ip +'/' + uri)
    response = await context.request(request).response
    print('Result: %s\n%r'%(response.code, response.payload))

async def delete(ip, uri):
    context = await Context.create_client_context()
    await asyncio.sleep(2)
    request = Message(code = DELETE, uri = 'coap://' + ip +'/' + uri)
    response = await context.request(request).response
    print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

  if(TEST == "GET"):
    print("*** GET ***")
    asyncio.run(get(ESP32_IP, URI))
  if(TEST == "PUT"):
    print("*** PUT ***")
    asyncio.run(put(ESP32_IP, URI, PAYLOAD))
    print("*** GET ***")
    asyncio.run(get(ESP32_IP, URI))
  if(TEST == "DELETE"):
    print("*** DELETE ***")
    asyncio.run(delete(ESP32_IP, URI))
    print("*** GET ***")
    asyncio.run(get(ESP32_IP, URI))

