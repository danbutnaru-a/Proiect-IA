import tkinter as tk
from tkinter import messagebox


class Team:
    def __init__(self, name, division, coefficient):
        self.name = name
        self.division = division
        self.coefficient = coefficient

    def __repr__(self):
        return f"{self.name} (Div: {self.division}, Coef: {self.coefficient})"


class TournamentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tournament Bracket Generator")
        self.teams = []

        # UI Elements
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
        # Get user input
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

        # Add the team to the list
        team = Team(name, division, coefficient)
        self.teams.append(team)
        self.teams_listbox.insert(tk.END, str(team))

        # Clear input fields
        self.name_entry.delete(0, tk.END)
        self.division_entry.delete(0, tk.END)
        self.coefficient_entry.delete(0, tk.END)

    def generate_bracket(self):
        if len(self.teams) < 2 or len(self.teams) % 2 != 0:
            messagebox.showerror("Invalid Teams", "You need an even number of teams to generate a bracket.")
            return

        try:
            bracket = self.create_bracket(self.teams)
            self.display_bracket(bracket)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def create_bracket(self, teams):
        teams = sorted(teams, key=lambda t: t.coefficient, reverse=True)

        def is_valid_matchup(team1, team2):
            return team1.division != team2.division and abs(team1.coefficient - team2.coefficient) <= 15

        def backtracking(teams, matchups=[]):
            if len(matchups) == len(teams) // 2:
                return matchups

            remaining_teams = [team for team in teams if team not in [t for pair in matchups for t in pair]]
            for i in range(len(remaining_teams)):
                for j in range(i + 1, len(remaining_teams)):
                    team1, team2 = remaining_teams[i], remaining_teams[j]
                    if is_valid_matchup(team1, team2):
                        matchups.append((team1, team2))
                        result = backtracking(teams, matchups)
                        if result:
                            return result
                        matchups.pop()
            return None

        bracket = backtracking(teams)
        if not bracket:
            raise ValueError("No valid tournament bracket can be generated with the given constraints.")
        return bracket

    def display_bracket(self, bracket):
        bracket_window = tk.Toplevel(self.root)
        bracket_window.title("Tournament Bracket")
        label = tk.Label(bracket_window, text="Tournament Bracket", font=("Helvetica", 16))
        label.pack(pady=10)
        for match in bracket:
            match_label = tk.Label(bracket_window, text=f"{match[0]} vs {match[1]}")
            match_label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()
