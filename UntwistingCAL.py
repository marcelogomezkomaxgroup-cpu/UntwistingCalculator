import tkinter as tk
from tkinter import ttk

class ZetaCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Zeta Torsion Controller - Dual Units")
        self.root.geometry("600x600")
        
        # State Variables
        self.lay_length = tk.DoubleVar(value=1000)
        self.total_length = tk.StringVar(value="10000")
        self.untwist_enabled = tk.BooleanVar(value=True)
        
        self.setup_ui()
        self.calculate()

    def mm_to_inch(self, mm_val):
        try:
            return float(mm_val) * 0.0393701
        except:
            return 0.0

    def setup_ui(self):
        # 1. Bypass Switch
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)
        tk.Checkbutton(top_frame, text="Untwisting Active", variable=self.untwist_enabled, 
                       command=self.calculate, font=("Arial", 12, "bold")).pack()

        # 2. Precision Controls & Slider
        slider_frame = tk.Frame(self.root)
        slider_frame.pack(pady=20, padx=20, fill="x")
        
        # Header with Dual Units
        header_frame = tk.Frame(slider_frame)
        header_frame.pack()
        tk.Label(header_frame, text="Lay Length (P): ", font=("Arial", 10, "bold")).pack(side="left")
        self.lay_mm_label = tk.Label(header_frame, text="1000 mm", font=("Arial", 10))
        self.lay_mm_label.pack(side="left")
        self.lay_inch_label = tk.Label(header_frame, text=" (39.37 in)", font=("Arial", 10), foreground="blue")
        self.lay_inch_label.pack(side="left")
        
        # Control Buttons Row
        btn_frame = tk.Frame(slider_frame)
        btn_frame.pack(pady=10)
        
        increments = [-1000, -500, -50, -5, -1, 1, 5, 50, 500, 1000]
        for inc in increments:
            btn = tk.Button(btn_frame, text=f"{'+' if inc > 0 else ''}{inc}", 
                            width=4, command=lambda i=inc: self.adjust_slider(i))
            btn.pack(side="left", padx=2)

        self.slider = tk.Scale(slider_frame, from_=100, to_=4950, orient="horizontal", 
                               variable=self.lay_length, command=self.calculate, length=500, showvalue=0)
        self.slider.pack()

        # 3. Wire Length Input
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)
        
        input_label_frame = tk.Frame(input_frame)
        input_label_frame.pack()
        tk.Label(input_label_frame, text="Total Wire Length: ", font=("Arial", 10, "bold")).pack(side="left")
        self.total_inch_label = tk.Label(input_label_frame, text="0.00 in", font=("Arial", 10), foreground="blue")
        self.total_inch_label.pack(side="left")

        self.entry = tk.Entry(input_frame, textvariable=self.total_length, font=("Arial", 14), justify="center", width=15)
        self.entry.pack(pady=5)
        tk.Label(input_frame, text="mm", font=("Arial", 10)).pack()
        self.total_length.trace_add("write", self.calculate)

        # 4. Large Output Visual
        self.result_frame = tk.Frame(self.root, relief="ridge", bd=2, padx=30, pady=20)
        self.result_frame.pack(pady=30)
        self.result_label = tk.Label(self.result_frame, text="0.00", font=("Arial", 32, "bold"))
        self.result_label.pack()
        tk.Label(self.result_frame, text="TOTAL UNTWIST ROTATIONS", font=("Arial", 10, "bold")).pack()

    def adjust_slider(self, amount):
        current = self.lay_length.get()
        new_val = max(100, min(4950, current + amount))
        self.lay_length.set(new_val)
        self.calculate()

    def calculate(self, *args):
        # Update metric/imperial display labels
        p_mm = self.lay_length.get()
        p_inch = self.mm_to_inch(p_mm)
        self.lay_mm_label.config(text=f"{int(p_mm)} mm")
        self.lay_inch_label.config(text=f" ({p_inch:.2f} in)")

        try:
            l_mm = float(self.total_length.get())
            l_inch = self.mm_to_inch(l_mm)
            self.total_inch_label.config(text=f"{l_inch:.2f} in")
        except ValueError:
            self.total_inch_label.config(text="--- in")
            l_mm = 0

        # Torsion Calculation
        if not self.untwist_enabled.get():
            self.result_label.config(text="BYPASS", foreground="grey")
            return

        if p_mm > 0 and l_mm > 0:
            rotations = l_mm / p_mm
            self.result_label.config(text=f"{rotations:.3f}", foreground="#2e7d32")
        else:
            self.result_label.config(text="0.000", foreground="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZetaCalculator(root)
    root.mainloop()