import tkinter
from tkinter import DISABLED, END, ttk, VERTICAL, ALL, PhotoImage, LEFT
import tkinter.scrolledtext as scrolled_text
from fonts_and_colors import font, background_color, text_color, client_name_font
import socket


class ConnectionFrame(tkinter.Frame):
    """create frame where users can:
       enter IP address of server
       enter port number of server
       start or stop server"""

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.configure(background=background_color)

        # create and place server_ip_label
        self.server_ip_label = tkinter.Label(self, text='Server IP:', font=font, background=background_color,
                                             foreground=text_color)
        self.server_ip_label.grid(row=0, column=0, pady=10, sticky='WE', padx=(20, 20))

        # create and place server_ip_entry
        self.server_ip_entry = tkinter.Entry(self, width=25, font=font, borderwidth=2)
        self.server_ip_entry.grid(row=0, column=1, padx=(0, 20))

        # find and put current local ip address in server_ip_entry
        local_ip_address = socket.gethostbyname(socket.gethostname())
        self.server_ip_entry.insert(END, local_ip_address)
        self.server_ip_entry.configure(state=DISABLED, disabledforeground='black')

        # create and place server_port_label
        self.server_port_number_label = tkinter.Label(self, text='Port Number: ', font=font, foreground=text_color,
                                                      background=background_color)
        self.server_port_number_label.grid(row=1, column=0, sticky='WE', pady=10, padx=(20, 20))

        # create and place server_port_entry
        self.server_port_number_entry = tkinter.Entry(self, width=25, font=font, borderwidth=2)
        self.server_port_number_entry.grid(row=1, column=1, padx=(0, 20))

        # create and place start server button
        self.start_button = tkinter.Button(self, font=font, foreground=text_color, background=background_color,
                                           text='Start Server', activebackground=background_color,
                                           activeforeground=text_color)
        self.start_button.grid(row=2, column=0, columnspan=2, padx=(10, 10), ipadx=155, pady=10)


class ClientsFrame(tkinter.LabelFrame):
    """create frame where clients button will be displayed
       associate command for buttons """

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.configure(text='Clients Connected:', bg=background_color, foreground='white', font=font, borderwidth=2)

        self.buttons = {}
        self.images = {}
        self.button_number = 0

        # create container frame
        self.container_frame = tkinter.Frame(self, bg='white')
        # create a canvas in above container_frame
        self.my_canvas = tkinter.Canvas(self.container_frame)
        # add a scroll_bar to above canvas
        self.y_scrollbar = ttk.Scrollbar(self.container_frame, orient=VERTICAL, command=self.my_canvas.yview)
        self.my_canvas.configure(yscrollcommand=self.y_scrollbar.set, width=400, height=400)

        def on_mousewheel(event):
            """scroll elements from canvas when mouse is above and user uses scroll button"""

            if str(event.widget.winfo_parent()) == '.!clientsframe.!frame.!canvas.!frame':
                self.my_canvas.yview_scroll(int(-1 * (event.delta / 60)), "units")

        # create scrollable frame in self.my_canvas
        self.scrollable_frame = tkinter.Frame(self.my_canvas, bg='white')
        self.my_canvas.bind("<Configure>", lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox(ALL)))
        self.my_canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.my_canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.container_frame.pack(fill='both', expand=True)
        self.my_canvas.pack(side='left', fill='both', expand=True)
        self.y_scrollbar.pack(side='right', fill='y')

    def create_buttons(self, name: str, color: str, image_name: str) -> None:
        """create and display buttons on scrollable_frame"""

        # create and add button in self.buttons dict
        self.images.update({f'image_client{self.button_number}': PhotoImage(file=f'images/{image_name}')})
        # extend_name
        while len(name) < 60:
            name += ' '
        self.buttons.update({f'button_client{self.button_number}': tkinter.Button(self.main_window.clients_frame.
                                                                                  scrollable_frame, compound=LEFT,
                                                                                  text=f' {name}', width=400,
                                                                                  justify='left',
                                                                                  height=50,
                                                                                  font=client_name_font,
                                                                                  borderwidth=2, fg=color,
                                                                                  activeforeground=color)})
        # place buttons on GUI
        for index in range(0, self.button_number + 1):
            self.buttons[f'button_client{self.button_number}'].configure(image=self.images[f'image_client'
                                                                                           f'{self.button_number}'])
            self.buttons[f'button_client{self.button_number}'].pack()
            self.main_window.clients_frame.my_canvas.configure(scrollregion=self.my_canvas.bbox(ALL))

        self.button_number += 1

    def update_clients(self, button_name: str) -> None:
        """destroy button associated to a disconnected client and update GUI """

        self.buttons.pop(f'button_{button_name}').destroy()
        self.main_window.update()
        # play disconnect sound
        self.main_window.sounds.disconnect_sound.play()

    def clear_all_buttons(self, current_connection) -> None:
        """destroy all buttons from clients_frame when current client disconnects from server
           current_connection: Connection() -> None"""

        for client_name in current_connection.all_clients_index:
            self.buttons[f'button_{client_name}'].destroy()
            self.main_window.update()
            self.main_window.clients_frame.my_canvas.configure(scrollregion=self.my_canvas.bbox(ALL))


class MessagesFrame(tkinter.LabelFrame):
    """create a frame to display messages from clients"""

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.configure(text='Messages:', bg=background_color, foreground='white', font=font, borderwidth=2, width=80,
                       height=100)

        self.chat_text = scrolled_text.ScrolledText(self, width=50, height=17, wrap=tkinter.WORD, font=font,
                                                    state=DISABLED)
        self.chat_text.pack()
