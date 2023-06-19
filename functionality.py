import json
from tkinter import DISABLED, END, NORMAL
import socket
import threading
import pygame
from fonts_and_colors import admin_color


class Sounds:
    """Sounds class plays sounds"""
    def __init__(self, main_window):
        pygame.init()
        self.main_window = main_window

        self.connect_sound = pygame.mixer.Sound('sounds/connect_sound.mp3')
        self.disconnect_sound = pygame.mixer.Sound('sounds/disconnect_sound.mp3')
        self.receive_send_message_sound = pygame.mixer.Sound('sounds/receive_send_message_sound.mp3')
        self.error_sound = pygame.mixer.Sound('sounds/error_sound.mp3')


class Connection:
    """Connection class stores all information about connection"""
    def __init__(self):

        self.encoder = 'utf-8'
        self.server_ip = str()
        self.server_port = int()
        self.packet_length = 10
        self.server_socket = socket.socket()

        self.clients_sockets = []
        self.clients_ip = []
        self.clients_names = []
        self.clients_color = []
        self.clients_images = []
        self.all_clients_index = []
        self.all_clients = {}
        self.clients_number = 0


class Functionality:
    """Functionality class controls app"""

    def __init__(self, main_window):

        self.main_window = main_window
        self.is_start = False

    def start_stop_server(self, current_connection: Connection) -> None:
        """start stop server"""

        if self.is_start:
            self.stop_server(current_connection)
        else:
            self.start_server(current_connection)

    def start_server(self, current_connection: Connection) -> None:
        # get server_ip and server_port from GUI
        current_connection.server_ip = self.main_window.connection_frame.server_ip_entry.get()
        try:
            current_connection.server_port = int(self.main_window.connection_frame.server_port_number_entry.get())
        except ValueError:
            self.main_window.messages_frame.chat_text.config(state=NORMAL)
            self.main_window.messages_frame.chat_text.insert(END, f'Port number must be a number!\n', admin_color)
            self.main_window.messages_frame.chat_text.tag_config(admin_color, foreground=admin_color)
            self.main_window.messages_frame.chat_text.see(END)
            self.main_window.messages_frame.chat_text.config(state=DISABLED)

            # play error sound
            self.main_window.sounds.error_sound.play()
        else:
            # create socket
            current_connection.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # bind ip address and port number
            try:
                current_connection.server_socket.bind((current_connection.server_ip, current_connection.server_port))
            except OverflowError:
                self.main_window.messages_frame.chat_text.config(state=NORMAL)
                self.main_window.messages_frame.chat_text.insert(END, f'Port number must be a number'
                                                                      f' between 1-65535!\n', admin_color)
                self.main_window.messages_frame.chat_text.tag_config(admin_color, foreground=admin_color)
                self.main_window.messages_frame.chat_text.see(END)
                self.main_window.messages_frame.chat_text.config(state=DISABLED)
                # play error sound
                self.main_window.sounds.error_sound.play()

            else:
                # put server_socket in listening
                current_connection.server_socket.listen()

                # update GUI
                self.main_window.connection_frame.server_port_number_entry.configure(state=DISABLED)
                self.main_window.messages_frame.chat_text.delete(1.0, END)
                self.main_window.messages_frame.chat_text.config(state=NORMAL)
                self.main_window.messages_frame.chat_text.insert(END, f'Server starts at port '
                                                                      f'{current_connection.server_port}!'
                                                                      f'\n', admin_color)
                self.main_window.messages_frame.chat_text.tag_config(admin_color, foreground=admin_color)
                self.main_window.messages_frame.chat_text.config(state=DISABLED)
                # play connect sound
                self.main_window.sounds.connect_sound.play()

                # update GUI
                # modify is_start value
                self.is_start = True
                # change start button text
                self.main_window.connection_frame.start_button.config(text='Stop Server')

                # create a thread to continuously listen for connections
                connect_thread = threading.Thread(target=self.connect_client, args=(current_connection,))
                connect_thread.start()

    def stop_server(self, current_connection: Connection) -> None:

        message_data = {'message': 'Server is closing...'}

        message_packet = self.create_message('SERVER CLOSE', message_data)
        message_json = json.dumps(message_packet)
        # calculate length
        packet_length = str(len(message_json))
        while len(packet_length) < 10:
            packet_length += ' '
        # send SERVER CLOSE message to all connected clients
        for client_connected in current_connection.clients_sockets:
            # send packet_length of message packet
            client_connected.send(packet_length.encode(self.main_window.connection.encoder))
            # send SERVER CLOSE packet
            client_connected.send(message_json.encode(self.main_window.connection.encoder))

        # update GUI
        self.main_window.clients_frame.clear_all_buttons(current_connection)
        self.main_window.connection_frame.start_button.config(text='Start Server')
        self.main_window.connection_frame.server_port_number_entry.config(state=NORMAL)
        self.main_window.connection_frame.server_port_number_entry.delete(0, END)
        self.main_window.messages_frame.chat_text.config(state=NORMAL)
        self.main_window.messages_frame.chat_text.insert(END, 'Server Stop!\n', admin_color)
        self.main_window.messages_frame.chat_text.tag_config(admin_color, foreground=admin_color)
        self.main_window.messages_frame.chat_text.see(END)
        self.main_window.messages_frame.chat_text.config(state=DISABLED)

        # clear class attributes
        current_connection.clients_sockets.clear()
        current_connection.clients_ip.clear()
        current_connection.clients_names.clear()
        current_connection.clients_color.clear()
        current_connection.clients_images.clear()
        current_connection.all_clients_index.clear()
        current_connection.all_clients.clear()

        # play disconnect sound
        self.main_window.sounds.disconnect_sound.play()

        # close server_socket
        def close_server_socket():
            current_connection.server_socket.close()

        self.main_window.after(700, close_server_socket())

        self.is_start = False
        self.main_window.connection_frame.start_button.config(text='Start Server')

    def connect_client(self, current_connection: Connection):
        """listening for clients and connect them to server"""
        while True:
            try:
                # accept clients
                client_socket, client_address = current_connection.server_socket.accept()
            except OSError:
                break
            else:
                # send info flag message
                message_packet = self.create_message('INFO', 'Send your information!')
                message_json = json.dumps(message_packet)
                # calculate length
                packet_length = str(len(message_json))
                while len(packet_length) < 10:
                    packet_length += ' '
                # send info request
                # send packet_length
                client_socket.send(packet_length.encode(current_connection.encoder))
                # send packet
                client_socket.send(message_json.encode(current_connection.encoder))
                # receive info answer
                # receive packet_length
                packet_length = client_socket.recv(current_connection.packet_length).decode(current_connection.encoder)
                # receive info packet
                message_json = client_socket.recv(int(packet_length))
                self.process_message(message_json, client_socket, current_connection)

    @staticmethod
    def create_message(flag: str, data) -> dict:
        """data: str or dict"""
        return {'flag': flag,
                'data': data}

    def process_message(self, message_json: bytes, client_socket: socket.socket(), current_connection: Connection):
        # decode and turn string to dict
        message_packet = json.loads(message_json)
        flag = message_packet['flag']

        if flag == 'INFO':
            name = message_packet['data']['name']
            color = message_packet['data']['color']
            image_name = message_packet['data']['image_name']

            self.main_window.messages_frame.chat_text.config(state=NORMAL)
            self.main_window.messages_frame.chat_text.insert(END,
                                                             f'Client {name} connected to the server!\n', color)
            self.main_window.messages_frame.chat_text.tag_config(color, foreground=color)
            self.main_window.messages_frame.chat_text.see(END)
            self.main_window.messages_frame.chat_text.config(state=DISABLED)

            # play connect sound
            self.main_window.sounds.connect_sound.play()

            # add socket, name, color, ip and image
            current_connection.clients_sockets.append(client_socket)
            current_connection.clients_names.append(name)
            current_connection.clients_ip.append(client_socket.getpeername()[0])
            current_connection.clients_images.append(image_name)
            current_connection.clients_color.append(color)

            current_connection.all_clients_index.append(f'client{current_connection.clients_number}')

            current_connection.all_clients.update({f'client{current_connection.clients_number}': {'name': name,
                                                                                                  'color': color,
                                                                                                  'image_name':
                                                                                                      image_name}})
            current_connection.clients_number += 1

            self.main_window.clients_frame.create_buttons(name, color, image_name)
            self.send_information_about_all_clients(client_socket, current_connection)
        elif flag == 'DISCONNECT':
            index = current_connection.clients_sockets.index(client_socket)
            # clients_names
            client_name = current_connection.clients_names.pop(index)
            # clients_color
            client_color = current_connection.clients_color.pop(index)
            # update gui
            self.main_window.messages_frame.chat_text.config(state=NORMAL)
            self.main_window.messages_frame.chat_text.insert(END,
                                                             f'Client {client_name} disconnect from server!\n',
                                                             client_color)
            self.main_window.messages_frame.chat_text.tag_config(client_color, foreground=client_color)
            self.main_window.messages_frame.chat_text.see(END)
            self.main_window.messages_frame.chat_text.config(state=DISABLED)
            # update clients_images
            current_connection.clients_images.pop(index)
            # update clients_ip
            current_connection.clients_ip.pop(index)
            button_for_delete = current_connection.all_clients_index[index]
            # update all_clients_index
            current_connection.all_clients_index.pop(index)
            # update all clients
            current_connection.all_clients.pop(button_for_delete)
            self.main_window.clients_frame.update_clients(button_for_delete)
            self.main_window.messages_frame.chat_text.configure(background='white')
            # send disconnect flag to all clients
            message_packet = self.create_message('DISCONNECT', button_for_delete)
            message_json = json.dumps(message_packet)
            # calculate length
            packet_length = str(len(message_json))
            while len(packet_length) < 10:
                packet_length += ' '
            # send DISCONNECT message
            current_connection.clients_sockets.remove(client_socket)
            client_socket.close()

            for each_socket in current_connection.clients_sockets:
                # send packet_length
                each_socket.send(packet_length.encode(current_connection.encoder))
                # send packet
                each_socket.send(message_json.encode(current_connection.encoder))

            # play disconnect sound
            self.main_window.sounds.error_sound.play()

        elif flag == 'MESSAGE':
            destination_index = current_connection.all_clients_index.index(message_packet['data']['partner_name'])
            destination_name = current_connection.clients_names[destination_index]

            socket_to_send = current_connection.clients_sockets[destination_index]

            source_index = current_connection.clients_sockets.index(client_socket)
            source_client = current_connection.all_clients_index[source_index]

            source_name = current_connection.clients_names[source_index]
            source_color = current_connection.clients_color[source_index]

            self.main_window.messages_frame.chat_text.config(state=NORMAL)
            self.main_window.messages_frame.chat_text.insert(END, f'{source_name} -> {destination_name}:'
                                                                  f' {message_packet["data"]["message"]}', source_color)
            self.main_window.messages_frame.chat_text.tag_config(source_color, foreground=source_color)
            self.main_window.messages_frame.chat_text.see(END)
            self.main_window.messages_frame.chat_text.config(state=DISABLED)

            message_data = {'message': message_packet['data']['message'],
                            'partner_name': message_packet['data']['partner_name'],
                            'source_client': source_client}

            message_packet = self.create_message('MESSAGE', message_data)
            message_json = json.dumps(message_packet)
            # calculate length
            packet_length = str(len(message_json))
            while len(packet_length) < 10:
                packet_length += ' '
            # send packet_length of message packet
            socket_to_send.send(packet_length.encode(self.main_window.connection.encoder))
            # send MESSAGE packet
            socket_to_send.send(message_json.encode(self.main_window.connection.encoder))

    def send_information_about_all_clients(self, client_socket: socket.socket(), current_connection: Connection):
        message = self.create_message('ALL CLIENTS', current_connection.all_clients)
        message_json = json.dumps(message)
        # calculate length
        packet_length = str(len(message_json))
        while len(packet_length) < 10:
            packet_length += ' '
        # send ALL CLIENTS message
        # send packet_length
        for each_client_socket in current_connection.clients_sockets:
            each_client_socket.send(packet_length.encode(current_connection.encoder))
            # send packet
            each_client_socket.send(message_json.encode(current_connection.encoder))
        # start receive message thread
        receive_thread = threading.Thread(target=self.receive_message, args=(current_connection, client_socket))
        receive_thread.start()

    def receive_message(self, current_connection, client_socket):
        """receive message, decode and send it to self.process_message"""
        while True:
            try:
                packet_length = client_socket.recv(current_connection.packet_length)
                message_json = client_socket.recv(int(packet_length))
                self.process_message(message_json, client_socket, current_connection)
            except OSError:
                # Socket close
                break
            except ValueError:
                # receive empty string
                break
