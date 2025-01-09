import tkinter as tk
from tkinter import messagebox

class Team:
    def __init__(self, name, division, coefficient):
        self.name = name
        self.division = division
        self.coefficient = coefficient

    def __repr__(self):
        return f"{self.name} (Div: {self.division}, Coef: {self.coefficient})"

    def get_name(self):
        return self.name

class TournamentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tournament Bracket Generator")
        self.teams = []

        self.title_label = tk.Label(root, text="Add Teams to the Tournament", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.form_frame = tk.Frame(root)
        self.form_frame.pack()

        self.name_label = tk.Label(self.form_frame, text="Team Name:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.division_label = tk.Label(self.form_frame, text="Division:")
        self.division_label.grid(row=1, column=0, padx=5, pady=5)
        self.division_entry = tk.Entry(self.form_frame)
        self.division_entry.grid(row=1, column=1, padx=5, pady=5)

        self.coefficient_label = tk.Label(self.form_frame, text="Performance Coefficient:")
        self.coefficient_label.grid(row=2, column=0, padx=5, pady=5)
        self.coefficient_entry = tk.Entry(self.form_frame)
        self.coefficient_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = tk.Button(root, text="Add Team", command=self.add_team)
        self.add_button.pack(pady=10)

        self.generate_button = tk.Button(root, text="Generate Bracket", command=self.generate_bracket)
        self.generate_button.pack(pady=10)

        self.teams_label = tk.Label(root, text="Teams Added:", font=("Helvetica", 14))
        self.teams_label.pack(pady=5)
        self.teams_listbox = tk.Listbox(root, width=50, height=10)
        self.teams_listbox.pack()

    def add_team(self):
        name = self.name_entry.get().strip()
        division = self.division_entry.get().strip()
        try:
            coefficient = int(self.coefficient_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Performance Coefficient must be an integer.")
            return

        if not name or not division or coefficient <= 0:
            messagebox.showerror("Invalid Input", "All fields are required and coefficient must be positive.")
            return

        team = Team(name, division, coefficient)
        self.teams.append(team)
        self.teams_listbox.insert(tk.END, repr(team))

        self.name_entry.delete(0, tk.END)
        self.division_entry.delete(0, tk.END)
        self.coefficient_entry.delete(0, tk.END)

    def generate_bracket(self):
        if len(self.teams) < 2:
            messagebox.showerror("Invalid Teams", "You need at least 2 teams to generate a bracket.")
            return

        num_teams = len(self.teams)
        if (num_teams & (num_teams - 1)) != 0:
            messagebox.showerror("Invalid Teams", "Number of teams must be a power of 2 (e.g., 2, 4, 8, 16).")
            return

        try:
            bracket = self.create_bracket(self.teams)
            self.display_bracket(bracket)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def create_bracket(self, teams):
        teams = sorted(teams, key=lambda t: t.coefficient, reverse=True)
        return [[team] for team in teams]

    def display_bracket(self, bracket):
        bracket_window = tk.Toplevel(self.root)
        bracket_window.title("Tournament Bracket")

        canvas = tk.Canvas(bracket_window, width=800, height=600, bg="white")
        canvas.pack()

        spacing = 50
        line_length = 100
        short_line_length = 50
        start_x = 50
        start_y = 20

        current_level = bracket
        positions = []
        while len(current_level) > 1:
            next_level = []
            new_positions = []

            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    y1 = positions[i] if positions else start_y + i * spacing
                    y2 = positions[i + 1] if positions else start_y + (i + 1) * spacing
                    mid_y = (y1 + y2) // 2

                    if not positions:  # First pass, add team names
                        team1 = current_level[i][0].get_name()
                        team2 = current_level[i + 1][0].get_name()

                        canvas.create_text(start_x, y1, text=team1, anchor="w", font=("Helvetica", 10))
                        canvas.create_text(start_x, y2, text=team2, anchor="w", font=("Helvetica", 10))

                    canvas.create_line(start_x + 50, y1, start_x + 50 + line_length, y1)
                    canvas.create_line(start_x + 50, y2, start_x + 50 + line_length, y2)
                    canvas.create_line(start_x + 50 + line_length, y1, start_x + 50 + line_length, y2)

                    if len(current_level) > 2:
                        canvas.create_line(start_x + 50 + line_length, mid_y, start_x + 50 + line_length + short_line_length, mid_y)

                    next_level.append([current_level[i][0]])
                    new_positions.append(mid_y)

            current_level = next_level
            positions = new_positions
            start_x += line_length + short_line_length

        canvas.create_line(start_x, positions[0], start_x + line_length, positions[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()
