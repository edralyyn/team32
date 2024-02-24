import tkinter as tk
from functions import collect_data, forecast

class ButtonCustomizer:
    @staticmethod
    def customize_button(button):
        button.config(
            bg="#3c7c6e",
            fg="white",
            relief=tk.FLAT,
            font=("Helvetica"),
            bd=0
            )

class GUI:
    def __init__(self, root):
        self.root = root
        self.background_color = "#88a5cd"
        
        self.root.title("Predictive Maintenance System")
        self.root.configure(bg=self.background_color)

        self.nav_bar = tk.Frame(self.root, bg=self.background_color)
        self.nav_bar.pack(side="top", fill="x", padx=10, pady=10)

        collect = tk.Button(self.nav_bar, text="Collect", command=self.on_collect_click)
        collect.pack(side="left", padx=5)
        ButtonCustomizer.customize_button(collect)

        forecast_button = tk.Button(self.nav_bar, text="Forecast", command=self.on_forecast_click)
        forecast_button.pack(side="left", padx=5)
        ButtonCustomizer.customize_button(forecast_button)
    
        self.frame1 = tk.Frame(self.root, bg=self.background_color, bd=0)  # Use the same background color
        self.frame1.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        self.canvas1 = tk.Canvas(self.frame1, bg="white")
        self.canvas1.pack(fill="both", expand=True)

        self.frame2 = tk.Frame(self.root, bg=self.background_color, bd=0)  # Use the same background color
        self.frame2.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        self.canvas2 = tk.Canvas(self.frame2, bg="white")
        self.canvas2.pack(fill="both", expand=True)

        self.root.bind("<Configure>", self.resize_frames)

    def resize_frames(self, event):
        width = event.width

        frame1_width = width // 4
        frame2_width = width - frame1_width
        
        self.frame1.config(width=frame1_width)
        self.frame2.config(width=frame2_width)
    
    def on_collect_click(self):
        collect_data(self.canvas1)

    def on_forecast_click(self):
        forecast()

def main():
    root = tk.Tk()
    gui = GUI(root)
    root.geometry("1200x700")
    root.mainloop()

if __name__ == "__main__":
    main()
