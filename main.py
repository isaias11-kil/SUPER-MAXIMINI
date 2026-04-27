import customtkinter as ctk
from ui.login import LoginWindow

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SUPER MAXIMINI")
        self.geometry("800x600")

        # Set theme and color
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Initialize Login Frame
        self.show_login()

    def show_login(self):
        # Clear main window
        for widget in self.winfo_children():
            widget.destroy()

        self.login_frame = LoginWindow(self, on_success_callback=self.on_login_success)
        self.login_frame.pack(expand=True, fill="both")

    def on_login_success(self, user_data):
        # Callback to handle successful login
        print(f"Logged in successfully as: {user_data['NombreCompleto']}")

        # Here you would typically destroy the login frame and show the main dashboard
        self.login_frame.destroy()

        # Display a simple welcome message for now
        welcome_label = ctk.CTkLabel(self, text=f"Bienvenido al sistema,\n{user_data['NombreCompleto']} ({user_data['Rol']})", font=ctk.CTkFont(size=24, weight="bold"))
        welcome_label.pack(expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
