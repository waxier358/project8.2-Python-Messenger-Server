# project8.2-Python-Messenger-Server
I created a Python Messenger using sockets.
This application works in hub and soke mode.
Server can be started with this GUI.
Owner of server can enter his local IP address (current version will get IP address from ethernet interface automatically) and port number for server and can also start or stop server.
All connected clients appear in first scrollable frame with name and avatar.
All information about client status and all messages sent by every client will appear in second scrollable frame.

![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/42aa0142-8a34-423b-a031-685bcfbd74e2)

This is client’s  GUI.

![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/ee3c80ad-f52d-4680-ae1a-c2ccdec0c1b8)

Clients can insert IP address and port number of server, name, color of messages and choose avatar image. Connection status and information about clients and server status appear in first scrollable frame from GUI. All connected clients with names and avatars appear in second scrollable frame.  
To send messages client should press the button associated with his partner’s name and a message window will appear.

![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/a3a00572-d77a-4efe-8250-385fb943521d)

If destination client doesn’t have an open window associated with the source (client that sent the message), a message window will automatically be displayed on destination side. If any of the clients has message window associated with other client in minimized mode, the message window will be displayed on top of the screen. 
Application works on LAN and WAN network. This is a capture of a communication made in LAN network.
![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/4f740201-e580-4c68-a527-b36f71b1d3e7)
![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/89f9e49c-8593-416a-b8c9-d201aa9c6a66)
WAN communication capture:
![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/fec62e27-657f-42f2-880f-ac79ea842839)
![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/49a67323-91ca-4910-9300-c733d829d8f4)

!!! COMMUNICATION IS NOT ENCRYPTED !!!

If somebody converts hex values from above capture into a string, he will see the message:

Hex value:
7b22666c6167223a20224d455353414745222c202264617461223a207b226d657373616765223a202268656c6c6f212121215c6e222c2022706172746e65725f6e616d65223a2022636c69656e7431227d7d

string after conversion:

{"flag": "MESSAGE", "data": {"message": "hello!!!!\n", "partner_name": "client1"}}.

!!! IMPLEMENTATION !!!

If server is behind a NAT router, PORT FORWORDING must be implemented on router. On client and server site new rules must be implemented in FIREWALL.
Here is a link with more details: (https://stackoverflow.com/questions/29929107/python-3-using-sockets-over-the-internet)

!!! RECOMMENDATION !!!

For best GUI experience use a client name as short as possible.
All clients' names must have approximately the same length.
