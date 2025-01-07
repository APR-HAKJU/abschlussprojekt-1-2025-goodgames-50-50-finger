# backend.py

from datetime import datetime
import csv

class Game:
    """Represents a single game in the collection"""

    def __init__(self, id, title, platform, status="Want to Play"):
        """Initialize a new game"""
        self.id = id
        self.title = title
        self.platform = platform
        self.status = status
        self.rating = None
        self.review = None
        self.date_added = datetime.now().date()
        self.completion_date = None

    def update(self, status=None, rating=None, review=None):
        """Update game information"""
        if status:
            self.status = status
            self.completion_date = datetime.now().date() if status == "Completed" else None
        if rating is not None:  # Allow 0 as a rating
            self.rating = rating
        if review is not None:
            self.review = review

    def to_dict(self):
        """Convert game object to dictionary for frontend use"""
        return {
            'id': self.id,
            'title': self.title,
            'platform': self.platform,
            'status': self.status,
            'rating': self.rating,
            'review': self.review,
            'date_added': self.date_added,
            'completion_date': self.completion_date
        }


class GameLibrary:
    """Manages the in-memory game collection"""

    def __init__(self):
        """Initialize empty game library"""
        self.games = []
        self.next_id = 1
        self.csv_path = "./games.csv"

    def save_to_csv(self, game):
        """Speichert ein Spielobjekt als Zeile in der CSV-Datei"""
        try:
            # Überprüfen, ob die CSV-Datei bereits existiert
            file_exists = False
            try:
                with open(self.csv_path, mode='r', newline='', encoding='utf-8') as file:
                    file_exists = True
            except FileNotFoundError:
                pass

            # Spiel in die CSV-Datei schreiben
            with open(self.csv_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=game.to_dict().keys())

                # Kopfzeile nur schreiben, wenn die Datei neu erstellt wird
                if not file_exists:
                    writer.writeheader()

                # Spiel als Zeile hinzufügen
                writer.writerow(game.to_dict())
            print(f"Spiel '{game.title}' erfolgreich gespeichert.")
        except Exception as e:
            print(f"Fehler beim Speichern des Spiels: {e}")


        #TODO: Impement this method.
        # It should take a game object and save it as a row to a csv
        # the path of the csv is found in self.csv_path.

        #TODO: Add a try except block to handle the case where the file does not exist

    def load_from_csv(self):
        """Lädt alle Spiele aus der CSV-Datei und fügt sie zu self.games hinzu"""
        try:
            with open(self.csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Alle Spiele aus der Datei laden und in self.games einfügen
                self.games = [
                    Game(
                        id=int(row['id']),
                        title=row['title'],
                        platform=row['platform'],
                        status=row['status'],
                        # Zusätzliche Felder wie rating und review einfügen
                    )
                    for row in reader
                ]
                print(f"{len(self.games)} Spiele erfolgreich aus der CSV-Datei geladen.")
        except FileNotFoundError:
            print(f"Die Datei {self.csv_path} wurde nicht gefunden. Es wurden keine Spiele geladen.")
        except Exception as e:
            print(f"Fehler beim Laden der Spiele: {e}")

        # TODO Implement this method.
        # It should load all objects from a csv file and return put the games into self.games
        # the path of the csv is found in self.csv_path

        # TODO: Add a try except block to handle the case where the file does not exist

        def update_game_in_csv(self, game):
            """Aktualisiert eine vorhandene Zeile in der CSV-Datei basierend auf der Spiel-ID"""
            try:
                updated = False
                temp_file_path = self.csv_path + ".tmp"

                with open(self.csv_path, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    fieldnames = reader.fieldnames

                    with open(temp_file_path, mode='w', newline='', encoding='utf-8') as temp_file:
                        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
                        writer.writeheader()

                        for row in reader:
                            # Prüfen, ob die aktuelle Zeile aktualisiert werden muss
                            if int(row['id']) == game.id:
                                writer.writerow(game.to_dict())
                                updated = True
                            else:
                                writer.writerow(row)

                # Originaldatei durch die temporäre Datei ersetzen
                if updated:
                    import os
                    os.replace(temp_file_path, self.csv_path)
                    print(f"Spiel mit ID {game.id} erfolgreich aktualisiert.")
                else:
                    # Temporäre Datei entfernen, wenn kein Update durchgeführt wurde
                    import os
                    os.remove(temp_file_path)
                    print(f"Spiel mit ID {game.id} wurde nicht in der CSV-Datei gefunden.")
            except FileNotFoundError:
                print(f"Die Datei {self.csv_path} wurde nicht gefunden. Es konnte kein Spiel aktualisiert werden.")
            except Exception as e:
                print(f"Fehler beim Aktualisieren des Spiels: {e}")


        # TODO Implement this method.
        # It should take a game object and update the corresponding row in the csv
        # the path of the csv is found in self.csv_path

        # TODO: Add a try except block to handle the case where the file does not exist

    def add_game(self, title, platform, status="Want to Play"):
        """Add a new game to the library"""
        # TODO Add try/except block to handle duplicate games and raise a ValueError if it happens
        game = Game(
            id=self.next_id,
            title=title,
            platform=platform,
            status=status,
        )
        self.save_to_csv(game)
        self.games.append(game)
        self.next_id += 1
        return game.to_dict()

    def update_game(self, game_id, status, rating=None, review=None):
        """Update an existing game's information"""
        for game in self.games:
            if game.id == game_id:  # Use object attribute
                game.update(status, rating, review)
                self.update_game_in_csv(game)
                return game.to_dict()
        return None

    def get_games(self, status=None):
        """Get games, optionally filtered by status"""
        if status and status != "All":
            filtered_games = [game for game in self.games if game.status == status]  # Use object attribute
        else:
            filtered_games = self.games
        return [game.to_dict() for game in filtered_games]

    def get_game_by_id(self, game_id):
        """Get a specific game by its ID"""
        #TODO: Add try/except block to handle the case where the game is not found
        for game in self.games:
            if game.id == game_id:  # Use object attribute
                return game.to_dict()
        return None