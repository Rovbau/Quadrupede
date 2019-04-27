import json
import socket

class Transmit():
    def __init__(self):
        print("Init Transmit")
        
    def send_data(self, obstacles, liste1, liste2):
        send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       
        ip = "192.168.1."
        ip = "Root"
        #ip = "127.0.0.1"
        msg = json.dumps({'Obstacles': obstacles, 'Liste1': liste1, 'Liste2': liste2})
        send.sendto(msg, (ip, 50000)) 
        send.close()
        
