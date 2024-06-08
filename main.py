import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


from src.utils.utils import PROJECT_DIR

class NetflixAnalysis:
    #Analiza Netflix dataset
    def __init__(self):
        self.netflix_df = None

    def main(self):
        #Glowna metoda do uruchomienia analizy
        self.netflix_df = self._load_data()
        self.plot_dashboard()

    def plot_dashboard(self):
        #Stworzenie dashborda
        plt.style.use("default")
        fig, axs = plt.subplots(3, 1, figsize = (10, 5), facecolor = "pink") #stworzenie dwoch podwykresow 10x5
        self.plot_top_reviewed_movies(axs[0]) #wywolanie w metod w konkretnych miejscach
        self.plot_top_genres_movies(axs[1])
        self.table_top_reviewed(axs[2])
        #plt.text(4, -2, r'Netflix Data Visualisation', fontsize=20)
        plt.tight_layout() #automatyczne dopasowanie elementow wykresu
        plt.subplots_adjust(hspace=0.5)
        plt.show()
        

    def plot_top_reviewed_movies(self, ax):
        #Wykres najlepiej ocenianych filmow
        top_reviewed = self.netflix_df.nlargest(10, "rating")[["title", "rating"]] #wybor 10 filmow z najwieksza wartoscia w 'rating'
        sns.barplot(x="rating", y="title", data=top_reviewed, hue="title", ax=ax, palette="spring", legend = False) #wykres slupkowy z danymi z top_reviewed
        ax.set_title("Top 10 Best Reviewed Movies")
        ax.set_xlabel("Scale")
        ax.set_ylabel("Movie Title")

    def plot_top_genres_movies(self, ax):
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
        sizes = genre_counts.values #wartosci do wykresu
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=sns.color_palette("spring", len(labels))) #wykres kolowy
        ax.set_title("Top 10 Popular Genres")

    def table_top_reviewed(self, ax):
        # print(self.netflix_df.sort_values('rating', ascending=False)[["title", "rating"]])
        review_sort = self.netflix_df.sort_values('rating', ascending=False)[["title", "rating"]].head(100)
        data_list = [review_sort.columns.tolist()] + review_sort.values.tolist()
        # print(data_list)
        plt.table(cellText=data_list, cellLoc="center")
        # for rating in self.netflix_df["rating"]:
        
        # print(review_sort)

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


if __name__ == "__main__":
    NetflixAnalysis().main()



