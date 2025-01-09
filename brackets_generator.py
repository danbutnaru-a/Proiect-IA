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
            matchups = self.calculate_matchups(self.teams)
            bracket = [(self.teams[i], self.teams[j]) for i, j in matchups]
            self.display_bracket(bracket)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def calculate_matchups(self, teams):
        teams = sorted(teams, key=lambda t: t.coefficient, reverse=True)

        def is_valid_matchup(team1, team2):
            return team1.division != team2.division and abs(team1.coefficient - team2.coefficient) <= 20

        def forward_checking(remaining_teams, matchups):
            if len(matchups) == len(teams) // 2:
                return matchups

            for i in range(len(remaining_teams)):
                for j in range(i + 1, len(remaining_teams)):
                    team1, team2 = remaining_teams[i], remaining_teams[j]
                    if is_valid_matchup(team1, team2):
                        matchups.append((teams.index(team1), teams.index(team2)))
                        next_remaining = [t for k, t in enumerate(remaining_teams) if k not in (i, j)]
                        result = forward_checking(next_remaining, matchups)
                        if result:
                            return result
                        matchups.pop()
            return None

        matchups = forward_checking(teams, [])
        if not matchups:
            raise ValueError("No valid matchups found with the given constraints.")
        return matchups

    def display_bracket(self, bracket):
        bracket_window = tk.Toplevel(self.root)
        bracket_window.title("Tournament Bracket")

        canvas = tk.Canvas(bracket_window, width=800, height=600, bg="white")
        canvas.pack()

        spacing = 50
        line_length = 100
        start_x = 50
        start_y = 20

        positions = []
        for i, (team1, team2) in enumerate(bracket):
            y1 = start_y + i * spacing * 2
            y2 = y1 + spacing

            canvas.create_text(start_x, y1, text=team1.get_name(), anchor="w", font=("Helvetica", 10))
            canvas.create_text(start_x, y2, text=team2.get_name(), anchor="w", font=("Helvetica", 10))

            canvas.create_line(start_x + 50, y1, start_x + 50 + line_length, y1)
            canvas.create_line(start_x + 50, y2, start_x + 50 + line_length, y2)
            canvas.create_line(start_x + 50 + line_length, y1, start_x + 50 + line_length, y2)

            mid_y = (y1 + y2) // 2
            positions.append(mid_y)

        # Restul de nivele
        current_positions = positions
        current_start_x = start_x + 50 + line_length
        while len(current_positions) > 1:
            next_positions = []
            for i in range(0, len(current_positions), 2):
                y1 = current_positions[i]
                y2 = current_positions[i + 1]
                mid_y = (y1 + y2) // 2

                canvas.create_line(current_start_x, y1, current_start_x + line_length, y1)
                canvas.create_line(current_start_x, y2, current_start_x + line_length, y2)
                canvas.create_line(current_start_x + line_length, y1, current_start_x + line_length, y2)

                next_positions.append(mid_y)

            current_positions = next_positions
            current_start_x += line_length

        # Ultima linie
        if current_positions:
            canvas.create_line(current_start_x, current_positions[0], current_start_x + line_length, current_positions[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()
