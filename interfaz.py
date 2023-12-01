import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
from queue import Queue
import json
from PIL import Image, ImageTk

# Coloca aquí las funciones del chatbot, como predict_classes y get_responses
from chatbot import predict_classes, get_responses
from diagrampero import generar_diagrama, clasificar_por_secciones

intents = json.loads(open('intents.json').read())

respuestas = []

class ChatInterface:
    def __init__(self, master):
        master.title("Chatbot Interface")

        # Columna izquierda para el chatbot
        self.chatbox = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=10)  # Reducir el número de filas
        self.chatbox.grid(row=0, column=0, padx=10, pady=10, rowspan=2)

        self.input_entry = tk.Entry(master, width=40)
        self.input_entry.grid(row=2, column=0, padx=10, pady=10)

        self.send_button = tk.Button(master, text="Enviar", command=self.send_message)
        self.send_button.grid(row=3, column=0, padx=10, pady=10)

        self.clear_button = tk.Button(master, text="Limpiar", command=self.clear_chatbox)
        self.clear_button.grid(row=4, column=0, padx=10, pady=10)

        # Columna derecha para mostrar la imagen
        self.canvas = tk.Canvas(master, width=400, height=300)
        self.canvas.grid(row=0, column=1, columnspan=2, padx=70, pady=70, rowspan=3)

        self.queue = Queue()

        # Iniciar el hilo para manejar las respuestas del chatbot
        self.thread = Thread(target=self.update_chatbox)
        self.thread.daemon = True
        self.thread.start()

    def send_message(self):
        user_input = self.input_entry.get()
        self.input_entry.delete(0, tk.END)

        # Enviar el mensaje al chatbot y mostrar en la interfaz
        self.queue.put(f"Usuario: {user_input}\n")

        recognized_intents = predict_classes(user_input)

        if ',' in user_input:
            intents_list = user_input.split(',')
            responses = []
            for intent_str in intents_list:
                recognized_intents = predict_classes(intent_str)
                responses.extend(get_responses(recognized_intents, intents, user_input=intent_str))
        else:
            responses = get_responses(recognized_intents, intents, user_input=user_input)

        for res in responses:
            respuestas.append(res)
            self.queue.put(f"Bot: {res}\n")

        self.canvas.delete("all")

        limpio = clasificar_por_secciones(respuestas)
        generar_diagrama(limpio)
        print(respuestas)

        # Ajusta la ruta del archivo de imagen según sea necesario
        image_path = "arquitectura.png"
        img = Image.open(image_path)
        img = img.resize((400, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=photo, anchor='nw')
        self.canvas.image = photo

        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.move)
        self.canvas.bind("<MouseWheel>", self.zoom)

    def update_chatbox(self):
        while True:
            if not self.queue.empty():
                response = self.queue.get()
                self.chatbox.insert(tk.END, response)
                self.chatbox.yview(tk.END)
            self.chatbox.update_idletasks() 

    def clear_chatbox(self):
        self.chatbox.delete(1.0, tk.END)

    def start_move(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoom(self, event):
        x, y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        scale = 1.0
        if event.delta == -120:
            scale -= .1
        if event.delta == 120:
            scale += .1
        self.canvas.scale("all", x, y, scale, scale)

def main():
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()



