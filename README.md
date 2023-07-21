# project8.2-Python-Messenger-Server
I created a Python Messenger using sockets.
This application works in hub and soke mode.
Server can be started with this GUI.
Owner of server can enter his local IP address (current version will get IP address from ethernet interface automatically) and port number for server and can also start or stop server.
All connected clients appear in first scrollable frame with name and avatar.
All information about client status and all messages sent by every client will appear in second scrollable frame.

![image](https://github.com/waxier358/project8.2-Python-Messenger-Server/assets/105735620/4b8bf66b-c43f-49b6-83da-580242059be3)


This is client’s  GUI.

![image](https://github.com/waxier358/project8.2-Python-Messenger-Server/assets/105735620/da4afaf9-d7e0-494e-8c56-ea516f3a1f7e)


Clients can insert IP address and port number of server, name, color of messages and choose avatar image. Connection status and information about clients and server status appear in first scrollable frame from GUI. All connected clients with names and avatars appear in second scrollable frame.  
To send messages client should press the button associated with his partner’s name and a message window will appear.

![image](https://github.com/waxier358/project8.2-Python-Messenger-Server/assets/105735620/36a58344-fd0e-4418-b938-49a0090db7cb)


If destination client doesn’t have an open window associated with the source (client that sent the message), a message window will automatically be displayed on destination side. If any of the clients has message window associated with other client in minimized mode, the message window will be displayed on top of the screen. 
Application works on LAN and WAN network. This is a capture of a communication made in LAN network.
![image](https://github.com/waxier358/project8.2-Python-Messenger-Server/assets/105735620/cd6fff6c-a7da-4f1f-8363-5ff8fe33d507)

![image](https://github.com/waxier358/project8.2-Python-Messenger-Server/assets/105735620/7bab3f91-527a-401b-9b2d-9a11c6ad2a10)

WAN communication capture:
![image](https://github.com/waxier358/project8.2-Python-Messenger-Server/assets/105735620/ba13ea61-ad75-4945-8e92-5bee96a6c180)

![image](https://github.com/waxier358/project8.2-Python-Messenger-Server/assets/105735620/89c1b5e5-d184-4d74-ad61-5e0f7d785581)


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
