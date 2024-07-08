import re
import time
import paho.mqtt.client as mqtt
from datetime import datetime

print("")
print("  ___  ____ ___ _______   __  __  ____ _______ _______    ____                            _____                _            ")
print(" |__ \|  _ \__ \__   __| |  \/  |/ __ \__   __|__   __|  / __ \                          / ____|              | |           ")
print("    ) | |_) | ) | | |    | \  / | |  | | | |     | |    | |  | |_   _  ___ _   _  ___   | (___   ___ _ __   __| | ___ _ __  ")
print("   / /|  _ < / /  | |    | |\/| | |  | | | |     | |    | |  | | | | |/ _ \ | | |/ _ \   \___ \ / _ \ '_ \ / _` |/ _ \ '__| ")
print("  / /_| |_) / /_  | |    | |  | | |__| | | |     | |    | |__| | |_| |  __/ |_| |  __/   ____) |  __/ | | | (_| |  __/ |    ")
print(" |____|____/____| |_|    |_|  |_|\___\_\ |_|     |_|     \___\_\\__,_|\___|\__,_|\___|  |_____/ \___|_| |_|\__,_|\___|_|    ")
print("")

log_file = 'C:/Users/YOUR_USERNAME/AppData/Roaming/.minecraft/logs/latest.log'

broker = 'YOUR_BROCKER_IP'
port = 1883
client_id = '2b2t-script'
username = 'USERNAME'
password = 'PASSWORD'
base_topic = '2b2t'

client = mqtt.Client(client_id)
client.username_pw_set(username, password)

last_position = None
last_status = "-"  # Set "unknown" status
connected = False

start_time = time.time()  # Remember script launch time
queue_1_reached = False



def check_queue_position(log_file):
    try:
        with open(log_file, 'r') as file:
            file.seek(0, 2)  # Go to end of file
            file_size = file.tell()  # Get the currrent point position 
            block_size = 1024  # The block size we will read
            start_pos = max(file_size - block_size, 0)  # Block reading start position
            content = ""

            while start_pos >= 0:
                file.seek(start_pos)  # Move the reading pointer to the starting position of the block
                content = file.read(block_size) + content  # Read the block and add it to the beginning of the content
                if '\n' in content:
                    break  # If we find a newline character, exit the loop
                start_pos -= block_size  # Go to the previous block

            match = re.search(r'Position in queue: (\d+)', content)
            if match:
                queue_position = int(match.group(1))
                return queue_position
            else:
                return None
    except FileNotFoundError:
        print(f"Log file not found: {log_file}")
        return None
    except Exception as e:
        print(f"Error reading log file: {e}")
        return None



def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        connected = True
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Connected to MQTT broker")
        if last_position is not None:  #Send last status after connection
            client.publish(base_topic, f"{last_position}")
    else:
        connected = False
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Connection failed with code {rc}")

client.on_connect = on_connect

client.loop_start()
while True:

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elapsed_time = time.time() - start_time
    elapsed_hours = int(elapsed_time // 3600)
    elapsed_minutes = int((elapsed_time % 3600) // 60)

    if not connected:
        try:
            client.connect(broker, port)
        except ConnectionRefusedError:
            print(f"{current_time} Connection refused. Check broker address, port, username, password.")
        except Exception as e:
            print(f"{current_time} Error connecting to MQTT: {e}")

    queue_position = check_queue_position(log_file)
    if queue_position is not None:
        if queue_position != last_position:
            last_position = queue_position
            last_status = f"{queue_position}"
            print(f"{current_time} Queue position changed: {last_status}, total waiting: {elapsed_hours} hours and {elapsed_minutes} minutes")
            if connected:
                client.publish(base_topic, last_status)

            if queue_position == 1 and not queue_1_reached:
                queue_1_reached = True
                #elapsed_time = time.time() - start_time
                print(f"{current_time} Queue position 1 reached after {elapsed_hours} hours and {elapsed_minutes} minutes") 

        #else:
            #print(f"{current_time} Queue position unchanged")
    else:
        print(f"{current_time} Cannot find queue position in the log file.")
        last_status = "-"
        if connected:
            client.publish(base_topic, last_status)

    time.sleep(1)

client.loop_stop() 
