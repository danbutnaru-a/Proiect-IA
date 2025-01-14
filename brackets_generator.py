import tkinter as tk
from tkinter import messagebox, filedialog
import csv

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
        self.root.geometry("800x600")  # Dimensiunea fixă a ferestrei principale
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

        self.upload_button = tk.Button(root, text="Upload Teams from File", command=self.upload_teams)
        self.upload_button.pack(pady=10)

        self.generate_button = tk.Button(root, text="Generate Bracket", command=self.generate_bracket)
        self.generate_button.pack(pady=10)

        self.teams_label = tk.Label(root, text="Teams Added:", font=("Helvetica", 14))
        self.teams_label.pack(pady=5)

        # Scrollable frame for teams
        self.teams_frame_container = tk.Frame(root)
        self.teams_frame_container.pack(fill=tk.BOTH, expand=True)

        self.teams_canvas = tk.Canvas(self.teams_frame_container)
        self.teams_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.teams_frame_container, orient="vertical", command=self.teams_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.teams_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.teams_canvas.bind('<Configure>', lambda e: self.teams_canvas.configure(scrollregion=self.teams_canvas.bbox("all")))

        self.teams_frame = tk.Frame(self.teams_canvas)
        self.teams_canvas.create_window((0, 0), window=self.teams_frame, anchor="nw")

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
        self.display_team(team)

        self.name_entry.delete(0, tk.END)
        self.division_entry.delete(0, tk.END)
        self.coefficient_entry.delete(0, tk.END)

    def display_team(self, team):
        team_frame = tk.Frame(self.teams_frame)
        team_frame.pack(fill=tk.X, pady=2)

        team_label = tk.Label(team_frame, text=repr(team), anchor="w")
        team_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

        edit_button = tk.Button(team_frame, text="Edit", command=lambda: self.edit_team(team, team_frame, team_label))
        edit_button.pack(side=tk.RIGHT, padx=5)

        remove_button = tk.Button(team_frame, text="Remove", command=lambda: self.remove_team(team, team_frame))
        remove_button.pack(side=tk.RIGHT, padx=5)

        # Update the scrollbar to accommodate new content
        self.teams_canvas.update_idletasks()
        self.teams_canvas.configure(scrollregion=self.teams_canvas.bbox("all"))

    def edit_team(self, team, team_frame, team_label):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Team")

        tk.Label(edit_window, text="Team Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(edit_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, team.name)

        tk.Label(edit_window, text="Division:").grid(row=1, column=0, padx=5, pady=5)
        division_entry = tk.Entry(edit_window)
        division_entry.grid(row=1, column=1, padx=5, pady=5)
        division_entry.insert(0, team.division)

        tk.Label(edit_window, text="Performance Coefficient:").grid(row=2, column=0, padx=5, pady=5)
        coefficient_entry = tk.Entry(edit_window)
        coefficient_entry.grid(row=2, column=1, padx=5, pady=5)
        coefficient_entry.insert(0, str(team.coefficient))

        def save_changes():
            name = name_entry.get().strip()
            division = division_entry.get().strip()
            try:
                coefficient = int(coefficient_entry.get().strip())
            except ValueError:
                messagebox.showerror("Invalid Input", "Performance Coefficient must be an integer.")
                return

            if not name or not division or coefficient <= 0:
                messagebox.showerror("Invalid Input", "All fields are required and coefficient must be positive.")
                return

            team.name = name
            team.division = division
            team.coefficient = coefficient

            team_label.config(text=repr(team))
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def remove_team(self, team, team_frame):
        self.teams.remove(team)
        team_frame.destroy()

        # Update the scrollbar to accommodate removed content
        self.teams_canvas.update_idletasks()
        self.teams_canvas.configure(scrollregion=self.teams_canvas.bbox("all"))

    def upload_teams(self):
        file_path = filedialog.askopenfilename(title="Select File", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader, None)  # Omit the header row
                for row in reader:
                    if len(row) != 3:
                        messagebox.showerror("Invalid Format", "Each line must have exactly 3 values: Name, Division, Coefficient.")
                        return
                    name, division, coefficient = row
                    try:
                        coefficient = int(coefficient)
                    except ValueError:
                        messagebox.showerror("Invalid Input", f"Invalid coefficient for team {name}. Must be an integer.")
                        return
                    if not name or not division or coefficient <= 0:
                        messagebox.showerror("Invalid Input", f"Invalid data for team {name}. All fields are required, and coefficient must be positive.")
                        return
                    team = Team(name, division, coefficient)
                    self.teams.append(team)
                    self.display_team(team)  # Use display_team to show in the scrollable area
            messagebox.showinfo("Success", "Teams successfully loaded from file.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load teams from file: {str(e)}")

    def generate_bracket(self):
        if len(self.teams) < 2:
            messagebox.showerror("Invalid Teams", "You need at least 2 teams to generate a bracket.")
            return

        num_teams = len(self.teams)
        if (num_teams & (num_teams - 1)) != 0:
            messagebox.showerror("Invalid Teams", "Number of teams must be a power of 2 (e.g., 2, 4, 8, 16).")
            return

        try:
            self.teams = sorted(self.teams, key=lambda t: t.coefficient, reverse=True)
            matchups = self.calculate_matchups(self.teams)
            bracket = [(self.teams[i], self.teams[j]) for i, j in matchups]
            self.display_bracket(bracket)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def calculate_matchups(self, teams):
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

        if current_positions:
            canvas.create_line(current_start_x, current_positions[0], current_start_x + line_length, current_positions[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()
