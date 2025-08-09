import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("dark")  # Light, Dark, or System
ctk.set_default_color_theme("blue")  # Can be "blue", "green", etc.

class HarExtractorUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("har-image-extractor")
        self.geometry("720x460")
        self.resizable(False, False)

        # Grid config
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left block (upload)
        left_frame = ctk.CTkFrame(self, corner_radius=15)
        left_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        # Load HAR image
        har_image = ctk.CTkImage(
            light_image=Image.open("har_color_palette.png"),
            dark_image=Image.open("har_color_palette.png"),
            size=(180, 180)
        )

        image_label = ctk.CTkLabel(left_frame, text="", image=har_image)
        image_label.pack(pady=(30, 10))

        text_label = ctk.CTkLabel(left_frame, text="Загрузить.har", font=("Segoe UI", 18))
        text_label.pack()

        # Right block (recent files)
        right_frame = ctk.CTkFrame(self, corner_radius=15)
        right_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

        header_label = ctk.CTkLabel(right_frame, text="Недавние файлы", font=("Segoe UI", 20))
        header_label.pack(pady=(30, 10))

        example_label = ctk.CTkLabel(right_frame, text="📁 example", font=("Segoe UI", 16), anchor="w")
        example_label.pack(anchor="w", padx=20)

        data_label = ctk.CTkLabel(right_frame, text="📁 my_data", font=("Segoe UI", 16), anchor="w")
        data_label.pack(anchor="w", padx=20)


if __name__ == "__main__":
    app = HarExtractorUI()
    app.mainloop()
