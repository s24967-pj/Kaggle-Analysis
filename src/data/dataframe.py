import os
import pandas as pd

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

class DataFrame:
    
    def __init__(self):
        self.df = self._load_data() # załadowanie danych
        self._clean_df() # funkcja do czyszczenia danych w pliku
    
    def get(self):
        return self.df # przekazanie DataFrame
           
    @staticmethod
    def _load_data():
        """Funkcja wczytujaca dane."""
        file_path = os.path.join(PROJECT_DIR, "src", "data", "n_movies.csv")
        return pd.read_csv(file_path)
    
    def _clean_df(self):
        """Oczyszczanie pliku csv"""
        self.df.drop_duplicates(
            'title', keep='first', inplace=True)  # usuniecie duplikatow z df
        # roroznienie danych zapisanych po przecinku w kolumnie genre
        self.df['genre'] = self.df['genre'].str.split(', ')