import tkinter as tk
from tkinter import ttk, messagebox
from api import get_pokemon, get_pokemon_by_type
from utils import load_image_from_url
import random

# Stat color helper
def stat_color(value):
    if value >= 80:
        return "green"
    elif value >= 50:
        return "orange"
    else:
        return "red"

# Type colors
TYPE_COLORS = {
    "Fire": "#F08030",
    "Water": "#6890F0",
    "Grass": "#78C850",
    "Electric": "#F8D030",
    "Psychic": "#F85888",
    "Ice": "#98D8D8",
    "Dragon": "#7038F8",
    "Dark": "#705848",
    "Fairy": "#EE99AC",
    "Normal": "#A8A878",
    "Fighting": "#C03028",
    "Flying": "#A890F0",
    "Poison": "#A040A0",
    "Ground": "#E0C068",
    "Rock": "#B8A038",
    "Bug": "#A8B820",
    "Ghost": "#705898",
    "Steel": "#B8B8D0"
}

class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Pokédex Lab")
        self.root.geometry("800x780")
        self.root.configure(bg="#e0f7fa")
        self.history = []
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(
            self.root, text="Pokédex Lab", font=("Arial", 28, "bold"),
            bg="#e0f7fa", fg="#00796B"
        )
        self.title_label.pack(pady=20)

        search_frame = tk.Frame(self.root, bg="#e0f7fa")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Enter Pokémon Name or ID:", bg="#e0f7fa", fg="#004D40", font=("Arial", 12)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=20, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Search", bg="#00796B", fg="white", command=self.search_pokemon).pack(side=tk.LEFT)
        tk.Button(search_frame, text="🎲 Mystery Pokémon", bg="#004D40", fg="white", command=self.random_pokemon).pack(side=tk.LEFT, padx=5)

        # Main content + history side by side
        content_frame = tk.Frame(self.root, bg="#e0f7fa")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left frame: main content
        left_frame = tk.Frame(content_frame, bg="#e0f7fa")
        left_frame.pack(side="left", fill="both", expand=True)

        self.result_text = tk.Text(left_frame, width=55, height=8, font=("Arial", 11), bg="#B2DFDB", bd=2, relief="groove")
        self.result_text.pack(pady=10)

        self.stats_frame = tk.Frame(left_frame, bg="#e0f7fa")
        self.stats_frame.pack(pady=10)

        self.mood_label = tk.Label(left_frame, text="Mood: 🐣 Start by searching a Pokémon!", font=("Arial", 12, "bold"), bg="#e0f7fa", fg="#00796B")
        self.mood_label.pack(pady=5)

        self.image_label = tk.Label(left_frame, bg="#e0f7fa", bd=2, relief="ridge", width=160, height=160)
        self.image_label.pack(pady=10)

        # Right frame: history
        right_frame = tk.Frame(content_frame, bg="#e0f7fa")
        right_frame.pack(side="right", fill="y", padx=10)

        tk.Label(right_frame, text="Search History:", font=("Arial", 11, "bold"), bg="#e0f7fa", fg="#004D40").pack(pady=5)
        self.history_listbox = tk.Listbox(right_frame, height=20, font=("Arial", 11), bd=2, relief="groove", bg="#B2DFDB")
        self.history_listbox.pack(pady=5, fill="y")
        self.history_listbox.bind("<<ListboxSelect>>", self.history_select)

    def history_select(self, event):
        if not self.history_listbox.curselection():
            return
        selection = self.history_listbox.get(self.history_listbox.curselection())
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, selection)
        self.search_pokemon(move_to_top=True)

    def search_pokemon(self, move_to_top=False):
        name = self.search_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a Pokémon name or ID.")
            return

        data = get_pokemon(name)
        if not data:
            messagebox.showerror("Error", "Pokémon not found.")
            return

        # Background color based on primary type
        primary_type = data["types"][0]
        bg_color = TYPE_COLORS.get(primary_type, "#f0f0f0")
        self.root.configure(bg=bg_color)
        self.title_label.configure(bg=bg_color)
        self.mood_label.configure(bg=bg_color)
        self.image_label.configure(bg=bg_color)

        # Type buttons
        if hasattr(self, 'type_buttons_frame'):
            self.type_buttons_frame.destroy()
        self.type_buttons_frame = ttk.Frame(self.root)
        self.type_buttons_frame.pack(pady=5)
        ttk.Label(self.type_buttons_frame, text="Types:", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        for t in data["types"]:
            btn = tk.Button(
                self.type_buttons_frame, text=t, bg=TYPE_COLORS.get(t, "grey"), fg="white",
                command=lambda type_name=t: self.show_type_pokemon(type_name)
            )
            btn.pack(side="left", padx=3)

        # Update search history
        pokemon_name = data["name"].title()
        if pokemon_name in self.history:
            self.history.remove(pokemon_name)
        self.history.insert(0, pokemon_name)
        if len(self.history) > 5:
            self.history = self.history[:5]

        self.history_listbox.delete(0, tk.END)
        for h in self.history:
            self.history_listbox.insert(tk.END, h)

        # Info text
        info = (
            f"Name: {data['name']}\n"
            f"Height: {data['height']}\n"
            f"Weight: {data['weight']}\n"
            f"Types: {', '.join(data['types'])}\n"
            f"Abilities: {', '.join(data['abilities'])}\n"
        )
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, info)

        # Stat bars
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        for stat, value in data["stats"].items():
            ttk.Label(self.stats_frame, text=f"{stat}:", font=("Arial", 11, "bold")).pack(anchor="w")
            bar = ttk.Progressbar(self.stats_frame, length=300, maximum=150)
            bar['value'] = value
            bar.pack(pady=2)
            bar_style = ttk.Style()
            bar_style.theme_use('default')
            bar_style.configure(f"{stat}.Horizontal.TProgressbar", troughcolor='grey', background=stat_color(value))
            bar.config(style=f"{stat}.Horizontal.TProgressbar")

        # Mood
        total_stats = sum(data["stats"].values())
        if total_stats >= 400:
            mood = "😈 Elite Pokémon"
        elif total_stats >= 250:
            mood = "🙂 Well-rounded"
        else:
            mood = "😴 Needs Training"
        self.mood_label.config(text=f"Mood: {mood}  (Total stats: {total_stats})")

        # Pokémon image
        img = load_image_from_url(data["sprite"], size=(160, 160))
        self.image_label.config(image=img)
        self.image_label.image = img

    def random_pokemon(self):
        rand_id = random.randint(1, 1010)
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, str(rand_id))
        self.search_pokemon()

    def show_type_pokemon(self, type_name):
        pokemon_list = get_pokemon_by_type(type_name)
        if not pokemon_list:
            messagebox.showinfo("Type Info", f"No Pokémon found for type {type_name}")
            return

        popup = tk.Toplevel(self.root)
        popup.title(f"{type_name} Pokémon")
        tk.Label(popup, text=f"Pokémon with {type_name} type:", font=("Arial", 12, "bold")).pack(pady=5)
        listbox = tk.Listbox(popup, width=30, height=10, font=("Arial", 11))
        listbox.pack(padx=10, pady=5)
        for p in pokemon_list[:10]:
            listbox.insert(tk.END, p.title())

        def on_select(event):
            selection = listbox.get(listbox.curselection())
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, selection)
            self.search_pokemon(move_to_top=True)
            popup.destroy()

        listbox.bind("<<ListboxSelect>>", on_select)

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)
    root.mainloop()
