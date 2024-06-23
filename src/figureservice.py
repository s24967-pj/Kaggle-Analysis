import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


class FigureService:
    
    def plot_top_reviewed_movies(self, netflix_df: pd.DataFrame) -> go.Figure:
        """Funkcja zwracajaca wykres najlepiej ocenianych filmow."""
        top_reviewed = netflix_df.nlargest(10, "rating")[
        ["title", "rating"]]  # wybor 10 filmow z najwieksza wartoscia w 'rating'
        top_reviewed = top_reviewed.sort_values(
        by="rating", ascending=True)  # sortowanie danych malejaco
        colors = ['#ff0087']
        fig = px.bar(top_reviewed, x='rating', y='title',
                    orientation='h', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='Rating',
                        yaxis_title='Movie Title',
                        title="Top 10 Best Reviewed Movies",
                        title_font=dict(size=20, color='#89CFF0',
                                        family='Arial', weight='bold'),
                        title_x=0.5)
        return fig
    
    def plot_top_genres_movies(self, netflix_df: pd.DataFrame) -> go.Figure:
        """"Funkcja zwracajaca wykres najczesciej wystepujacych gatunkow filmow."""
        df_genres = netflix_df.explode(
            'genre')  # rozdzielenie gatunkow na osobne rzedy - kilka do jednego filmu
        genre_counts = df_genres['genre'].value_counts().head(
            5)  # zliczenie 5 najczestszych
        labels = genre_counts.index  # Etykiety
        values = genre_counts  # Wartosci do wykresu
        colors = ['#ffe0ee', '#ffc2db', '#ffa9c7', '#ff679d', '#ff0087']
        fig = go.Figure(
            data=[go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=colors))])
        fig.update_layout(title_text='Top 5 Popular Genres', title_font=dict(
            size=20, color='#89CFF0', family='Arial', weight='bold'), title_x=0.5)
        return fig