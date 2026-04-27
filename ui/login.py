import customtkinter as ctk
from tkinter import messagebox
from database.consultas import validar_credenciales

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, on_success_callback=None, **kwargs):
        super().__init__(master, **kwargs)

        self.on_success_callback = on_success_callback

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Title
        self.label_title = ctk.CTkLabel(self, text="SUPER MAXIMINI", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.grid(row=1, column=1, pady=(20, 30))

        # Username Label & Entry
        self.label_username = ctk.CTkLabel(self, text="Usuario:")
        self.label_username.grid(row=2, column=1, sticky="w", pady=(0, 5))

        self.entry_username = ctk.CTkEntry(self, width=250, placeholder_text="Ingrese su usuario")
        self.entry_username.grid(row=3, column=1, pady=(0, 15))

        # Password Label & Entry
        self.label_password = ctk.CTkLabel(self, text="Contraseña:")
        self.label_password.grid(row=4, column=1, sticky="w", pady=(0, 5))

        self.entry_password = ctk.CTkEntry(self, width=250, placeholder_text="Ingrese su contraseña", show="*")
        self.entry_password.grid(row=5, column=1, pady=(0, 30))

        # Login Button
        self.btn_login = ctk.CTkButton(self, text="ENTRAR", command=self.handle_login, width=250)
        self.btn_login.grid(row=6, column=1, pady=(0, 20))

        # Status Label for messages
        self.label_status = ctk.CTkLabel(self, text="", text_color="red")
        self.label_status.grid(row=7, column=1, pady=(0, 20))

    def handle_login(self):
        usuario = self.entry_username.get()
        contrasena = self.entry_password.get()

        if not usuario or not contrasena:
            self.label_status.configure(text="Por favor ingrese usuario y contraseña.", text_color="red")
            return

        # Show loading or processing status
        self.label_status.configure(text="Validando...", text_color="gray")
        self.update() # Update UI to show the message

        # Validate credentials
        es_valido, resultado = validar_credenciales(usuario, contrasena)

        if es_valido:
            self.label_status.configure(text="Inicio de sesión exitoso.", text_color="green")
            # Optionally show a message box
            # messagebox.showinfo("Éxito", f"Bienvenido, {resultado['NombreCompleto']}")

            # If a callback was provided for successful login, call it
            if self.on_success_callback:
                self.on_success_callback(resultado)
        else:
            # Show error message
            self.label_status.configure(text=resultado, text_color="red")
            # Clear password field
            self.entry_password.delete(0, 'end')
