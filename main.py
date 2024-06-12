from dash import Dash, html, dcc, Input, Output

import os
import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('agg')
import pandas as pd
import seaborn as sns
import dash
import dash_ag_grid as dag
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from src.utils.utils import PROJECT_DIR


class NetflixAnalysis:
    #Analiza Netflix dataset ladowanie danych i init dash app
    def __init__(self):
        self.netflix_df = self._load_data()
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.setup_layout()
    
    def setup_layout(self):

        # self.app.layout = dbc.Container([
        #     html.Div([
        #     html.H1("Netflix Data Visualisation"), 
        #     dcc.Graph(id='top-reviewed-movies', figure=self.plot_top_reviewed_movies()),
        #     dcc.Graph(id='top-genres-movies', figure=self.plot_top_genres_movies())             
        #     ]), 
        #     self.table_top_reviewed()],   
        # )

        self.app.layout = dbc.Container([
                dbc.Row(
                        dbc.Col(
                            [html.H1("Netflix Data Visualisation", style={'fontSize': 60, 'textAlign': 'center', 'color': '#800080'})],
                            width={'size': 6, 'offset': 3},
                        ),
                ),
                dbc.Row(
                    # [
                        dbc.Col(
                            dcc.Graph(id='top-reviewed-movies', figure=self.plot_top_reviewed_movies())
                        )
                    #     dbc.Col(
                    #         [self.table_top_reviewed()],
                    #         width={'size': 5, 'order': 2, 'offset': 1},
                    #     )
                    # ]
                ),
                dbc.Row(
                        dbc.Col(
                            dcc.Graph(id='top-genres-movies', figure=self.plot_top_genres_movies())
                        )
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [self.table_top_reviewed()],
                            width={'size': 6, 'offset': 3},
                        )
                    ]
                )
        ])
       

    def setup_callbacks(self):
        return
       
        

    def plot_top_reviewed_movies(self):
        #Wykres najlepiej ocenianych filmow
        top_reviewed = self.netflix_df.drop_duplicates('title', keep='first').nlargest(10, "rating")[["title", "rating"]] #wybor 10 filmow z najwieksza wartoscia w 'rating' zapisujac 1 wynik, aby nie bylo powtorek
        colors = ['#ff0087']
        fig = px.bar(top_reviewed, x='rating', y='title', orientation='h',  color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='Rating', yaxis_title='Movie Title', title="Top 10 Best Reviewed Movies", title_font=dict(size=20, color='black', family='Arial', weight='bold'), title_x=0.5)
        return fig

    def plot_top_genres_movies(self):
       #Wykres najczesciej wystepowanych gatunkow
        dictionary = {} #stworzenie slownika

        for genre in self.netflix_df["genre"]: #przzechodzimy przez cala koumne genre        
            if type(genre) is not str: #rozwiaznie problemu zle wprowadzonych danych w jednym z filmow
                continue
            if ',' not in genre: #jezeli w 'genre' nie ma kilku gatunkow przypisanych do jednego filmu
               self._update_dictionary(dictionary, genre)
            else: #jezeli mamy przypisane wiecej niz jeden gatunek do filmu
                for element in genre.split(', '): #rozdzielanie gatunkow po przecinku
                    self._update_dictionary(dictionary, element)
                          
        genre_counts_df = pd.DataFrame.from_dict(data=dictionary, orient='index', columns=['counts']) #zmiana typu z listy na dataframe
        genre_counts = genre_counts_df['counts'].sort_values(ascending=False).head(5) #sortowanie wartosci malejaco i wybranie 5
        labels = genre_counts.index #etykiety
        values = genre_counts.values #wartosci do wykresu
        colors = ['#ffe0ee', '#ffc2db', '#ffa9c7', '#ff679d', '#ff0087']
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=colors))])
        fig.update_layout(title_text='Top 5 Popular Genres', title_font=dict(size=20, color='black', family='Arial', weight='bold'), title_x=0.5)
        return fig

    def table_top_reviewed(self):
       
        #review_sort = self.netflix_df.drop_duplicates('title', keep='first').sort_values('rating', ascending=False)[["title", "rating"]] #sortowanie danych z ratings
      
        review_sort = self.netflix_df.drop_duplicates('title', keep='first')[["title", "rating"]]
        columnDefs = [
            {'field': 'title', 'sortable': False},
            {'field': 'rating'}
            # {"name": "Rating", "id": "rating", "type": "numeric"}
        ]
        
        table = html.Div(
            [
                dag.AgGrid(
                    id="row-sorting-simple",
                    rowData=review_sort.to_dict("records"),
                    columnDefs=columnDefs,
                    defaultColDef={"filter": True},
                    columnSize="sizeToFit",
                    dashGridOptions={"animateRows": False}
                ),
            ],
        )
        #table = dash_table.DataTable(review_sort.to_dict('records'),
        # table = dash_table.DataTable(
        #     review_sort.to_dict('records'),
        #     columnDefs=columnDefs,
        #     defaultColDef={"filter": True},
        #     # sort_action="native", #umozliwia sortowanie
        #     style_header={
        #         'backgroundColor': 'pink',
        #         'fontWeight': 'bold'
        #     },
        #     style_data={
        #         'whiteSpace': 'auto',
        #         'height': 'auto'
        #     },
        #     style_table={
        #         'height': '300px', 
        #         'overflowY': 'auto'
        #     },
        #     style_cell={
        #         'textAlign': 'left'
        #     },
        #     style_cell_conditional=[
        #         {'if': {'column_id': 'title'},
        #          'width': 'auto'},
        #         {'if': {'column_id': 'rating'},
        #           'width': '90px'}
        #     ],     
        # ) #zapisanie posortowanych danych do tabeli
        return table

    def _update_dictionary(self, dictionary, genre):
        if genre in dictionary: #jezeli gatunek jest juz zapisany w slowniczku dodajemy licznik +1, w przeciwnym przypadku zapisujemy w slowniku i ustawiamy licznik na 1
            dictionary[genre] = dictionary[genre] + 1
        else:
            dictionary[genre] = 1

    @staticmethod
    #Zaladowanie datasetu
    def _load_data():
        file_path = os.path.join(PROJECT_DIR, "src", "data", "n_movies.csv")
        return pd.read_csv(file_path)
    
    def run_server(self):
        # Uruchomienie serwera Dash
        self.app.run_server(debug=True)



if __name__ == "__main__":
    analysis = NetflixAnalysis()
    analysis.run_server()
    



