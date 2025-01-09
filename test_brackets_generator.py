import unittest
from tkinter import Tk
from unittest.mock import patch
from brackets_generator import Team, TournamentApp

class TestTournamentApp(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = TournamentApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_add_team_valid(self):
        self.app.name_entry.insert(0, "Team A")
        self.app.division_entry.insert(0, "Division 1")
        self.app.coefficient_entry.insert(0, "10")

        self.app.add_team()

        self.assertEqual(len(self.app.teams), 1)
        self.assertEqual(self.app.teams[0].name, "Team A")
        self.assertEqual(self.app.teams[0].division, "Division 1")
        self.assertEqual(self.app.teams[0].coefficient, 10)

    def test_add_team_invalid_coefficient(self):
        self.app.name_entry.insert(0, "Team A")
        self.app.division_entry.insert(0, "Division 1")
        self.app.coefficient_entry.insert(0, "invalid")

        self.app.add_team()

        self.assertEqual(len(self.app.teams), 0)

    @patch("brackets_generator.messagebox.showerror")
    def test_generate_bracket_with_insufficient_teams(self, mock_showerror):
        # Add only one team to make the number insufficient
        self.app.teams.append(Team("Team A", "Division 1", 10))

        # Call the method
        self.app.generate_bracket()

        # Verify that messagebox.showerror was called
        mock_showerror.assert_called_once_with(
            "Invalid Teams", "You need at least 2 teams to generate a bracket."
        )

    @patch("brackets_generator.messagebox.showerror")
    def test_generate_bracket_with_invalid_team_count(self, mock_showerror):
        # Add an invalid number of teams (not a power of 2)
        self.app.teams.append(Team("Team A", "Division 1", 10))
        self.app.teams.append(Team("Team B", "Division 2", 20))
        self.app.teams.append(Team("Team C", "Division 3", 30))

        # Call the method
        self.app.generate_bracket()

        # Verify that messagebox.showerror was called
        mock_showerror.assert_called_once_with(
            "Invalid Teams", "Number of teams must be a power of 2 (e.g., 2, 4, 8, 16)."
        )

    def test_generate_bracket_valid(self):
        self.app.teams = [
            Team("Team A", "Division 1", 10),
            Team("Team B", "Division 2", 15),
            Team("Team C", "Division 3", 20),
            Team("Team D", "Division 4", 25)
        ]

        matchups = self.app.calculate_matchups(self.app.teams)
        self.assertIsNotNone(matchups)
        self.assertEqual(len(matchups), 2)  # 4 teams -> 2 matchups

    @patch("brackets_generator.messagebox.showerror")
    def test_no_valid_matchups(self, mock_showerror):
        # All teams are in the same division to violate constraints
        self.app.teams = [
            Team("Team A", "Division 1", 10),
            Team("Team B", "Division 1", 15),
            Team("Team C", "Division 1", 20),
            Team("Team D", "Division 1", 25),
        ]

        self.app.generate_bracket()

        # Ensure the error message is displayed
        mock_showerror.assert_called_once_with("Error", "No valid matchups found with the given constraints.")
    def test_large_number_of_teams(self):
        for i in range(1, 65):  # Adding 64 teams
            self.app.teams.append(Team(f"Team {i}", f"Division {i%5}", i))

        matchups = self.app.calculate_matchups(self.app.teams)
        self.assertIsNotNone(matchups)
        self.assertEqual(len(matchups), 32)


if __name__ == "__main__":
    unittest.main()
