import unittest
import pandas as pd
import os, sys
import plotly.graph_objs as go

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main


class TestTestowy(unittest.TestCase):
    def setUp(self):
        self.netflix = main.NetflixAnalysis()

    def test_file_not_none(self):
        """Przypadek testowy dla ladowania pliku csv"""
        self.assertIsNotNone(self.netflix.netflix_df)

    def test_file_is_data_frame(self):
        self.assertIsInstance(self.netflix.netflix_df, pd.DataFrame)

    def test_plot_top_genres_movies(self):
        """Przypadek testowy sprawdzajacy czy nie jest zwracana pusta figura"""
        fig = self.netflix.plot_top_genres_movies()
        self.assertIsNotNone(fig)
        self.assertTrue('data' in fig)

    def test_plot_top_rating_movies(self):
        """Przypadek testowy sprawdzajacy czy nie jest zwracana pusta tabela"""
        table = self.netflix.plot_top_reviewed_movies()
        self.assertIsNotNone(table)
        self.assertTrue('data' in table)

    def test_is_figure(self):
        """Przypadek testowy sprawdzajacy czy jest zwracana figura"""
        fig = self.netflix.plot_top_genres_movies()
        self.assertIsInstance(fig, go.Figure)


if __name__ == '__main__':
    unittest.main()