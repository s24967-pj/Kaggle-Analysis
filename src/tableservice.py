import pandas as pd
from dash import html
import dash_ag_grid as dag

class TableService:

    def create_actor_movie_table(self, netflix_df: pd.DataFrame) -> dag.AgGrid:
            """Funkcja zwracajaca tabele z aktorami i filmami."""
            columnDefs = [{
                'field': 'title',
                'headerName': 'Movie Title'
            }, {
                'field': 'stars',
                'headerName': 'Actors'
            }]  # zdefiniowanie kolumn tabeli, nadanie nazw
            table = dag.AgGrid(rowData=netflix_df[['title', 'stars']].to_dict("records"), columnDefs=columnDefs, defaultColDef={
            }, columnSize="sizeToFit", dashGridOptions={
                "animateRows": False
            })  # tworzenie tabeli z danymi z pliku csv
            return table

    def table_top_reviewed(self, netflix_df: pd.DataFrame) -> dag.AgGrid:
        """Funkcja zwracajaca tabelę z najlepiej ocenianymi filmami."""
        review_sort = netflix_df[["title", "rating"]
                                        ]  # z csv bierzemy 2 kolumy -title i rating
        columnDefs = [{
            'field': 'title',
            'sortable': False
        }, {
            'field': 'rating'
        }]  # zdef kolumn
        table = html.Div([dag.AgGrid(id="row-sorting-simple", rowData=review_sort.to_dict("records"), columnDefs=columnDefs, defaultColDef={
            "filter": True
        }, columnSize="sizeToFit", dashGridOptions={
            "animateRows": False
            # tworzymy tabele, todict aby dane byly przekazane w odpowiedni sposob 'records’ : list like [{column -> value},{tytul -> Avatar}] - zwracamy liste slownikow
        })])
        return table