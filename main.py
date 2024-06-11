import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import dash
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
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        #uklad apki
        # self.app.layout = html.Div([
        #     html.H1("Netflix Data Visualisation",), 
        #     dcc.Graph(id='top-reviewed-movies'),
        #     dcc.Graph(id='top-genres-movies'),
        #     html.Div(id='top-reviewed-table')
        # ])
        self.app.layout = dbc.Container(
            html.Div([
            html.H1("Netflix Data Visualisation",), 
            dcc.Graph(id='top-reviewed-movies'),
            dcc.Graph(id='top-genres-movies'),
            self.table_top_reviewed()])
        )

    def setup_callbacks(self):
        @self.app.callback(
            Output('top-reviewed-movies', 'figure'),
            Output('top-genres-movies', 'figure'),
            #Output('top-reviewed-table', 'child'),
            Input('top-reviewed-movies', 'id')
        )

        def update_dashboard(_):
            # Generowanie wykresów i tabeli
            top_reviewed_fig = self.plot_top_reviewed_movies()
            top_genres_fig = self.plot_top_genres_movies()
            top_reviewed_table = self.table_top_reviewed()
            return top_reviewed_fig, top_genres_fig, top_reviewed_table



    # def plot_dashboard(self):
    #     #Stworzenie dashborda
    #     plt.style.use("default")
    #     fig, axs = plt.subplots(3, 1, figsize = (10, 5), facecolor = "pink") #stworzenie dwoch podwykresow 10x5
    #     self.plot_top_reviewed_movies(axs[0]) #wywolanie w metod w konkretnych miejscach
    #     self.plot_top_genres_movies(axs[1])
    #     self.table_top_reviewed
    #     #plt.text(4, -2, r'Netflix Data Visualisation', fontsize=20)
    #     plt.tight_layout() #automatyczne dopasowanie elementow wykresu
    #     plt.subplots_adjust(hspace=0.5)
    #     plt.show()
        

    def plot_top_reviewed_movies(self):
        #Wykres najlepiej ocenianych filmow
        # top_reviewed = self.netflix_df.nlargest(10, "rating")[["title", "rating"]] #wybor 10 filmow z najwieksza wartoscia w 'rating'
        top_reviewed = self.netflix_df.drop_duplicates('title', keep='first').nlargest(10, "rating")[["title", "rating"]] 
        colors = ['#ff0087']
        fig = px.bar(top_reviewed, x='rating', y='title', orientation='h', title="Top 10 Best Reviewed Movies", color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='Rating', yaxis_title='Movie Title')
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
        fig.update_layout(title_text='Top 5 Popular Genres')
        return fig

    def table_top_reviewed(self):
        # # print(self.netflix_df.sort_values('rating', ascending=False)[["title", "rating"]])
        # review_sort = self.netflix_df.sort_values('rating', ascending=False)[["title", "rating"]].head(100)
        # data_list = [review_sort.columns.tolist()] + review_sort.values.tolist()
        # # print(data_list)
        # plt.table(cellText=data_list)
        

        # # for rating in self.netflix_df["rating"]:
        
        
        # # print(review_sort)
        review_sort = self.netflix_df.drop_duplicates('title', keep='first').sort_values('rating', ascending=False)[["title", "rating"]].head(50)
        # table = html.Table([
        #     html.Thead(html.Tr([html.Th(col) for col in review_sort.columns])),  # Nagłówki tabeli
        #     html.Tbody([
        #         html.Tr([
        #             html.Td(review_sort.iloc[i][col]) for col in review_sort.columns
        #         ]) for i in range(len(review_sort))
        #     ])
        # ])
        table = dash_table.DataTable(
            data=review_sort,
            columns=[{'id':col, 'name':col} for col in review_sort.columns]
        )
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
    



