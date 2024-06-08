import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


from src.utils.utils import PROJECT_DIR

class NetflixAnalysis:
    def __init__(self):
        self.netflix_df = None

    def main(self):
        self.netflix_df = self._load_data()
        self.plot_dashboard()

    def plot_dashboard(self):
        plt.style.use("default")
        fig, axs = plt.subplots(2, 1, figsize = (10, 5), facecolor = "pink")
        self.plot_top_reviewed_movies(axs[0])
        self.plot_top_genres_movies(axs[1])
        plt.tight_layout()
        plt.subplots_adjust(hspace=0.5)
        plt.show()
        

    def plot_top_reviewed_movies(self, ax):
        top_reviewed = self.netflix_df.nlargest(10, "rating")[["title", "rating"]]
        sns.barplot(x="rating", y="title", hue="title", dodge=False, data=top_reviewed, ax=ax, palette="spring", legend = False)
        ax.set_title("Top 10 Best Reviewed Movies")
        ax.set_xlabel("Scale")
        ax.set_ylabel("Movie Title")

    def plot_top_genres_movies(self, ax):
       
        dictionary = {}

        for genre in self.netflix_df["genre"]:
            
            if type(genre) is not str:
                continue

            if ',' not in genre:
                if genre in dictionary:
                    dictionary[genre] = dictionary[genre] + 1
                else:
                    dictionary[genre] = 1
            else:
                for element in genre.split(', '):
                    if element in dictionary:
                        dictionary[element] = dictionary[element] + 1
                    else:
                        dictionary[element] = 1
        # for genre in self.netflix_df["genre"]:
        #     dictionary ={f"keys: {genre}"}
        #     print(dictionary)
                          
        genre_counts_df = pd.DataFrame.from_dict(data=dictionary, orient='index', columns=['counts'])
        genre_counts = genre_counts_df['counts'].sort_values(ascending=False).head(5)
        labels = genre_counts.index
        sizes = genre_counts.values
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=sns.color_palette("spring", len(labels)))
        ax.set_title("Top 10 Popular Genres")

        # genre_counts = self.netflix_df["genre"].value_counts().head(5)
        # labels = genre_counts.index
        # sizes = genre_counts.values
        # ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=sns.color_palette("spring", len(labels)))
        # ax.set_title("Top 10 Popular Genres")

    @staticmethod
    def _load_data():
        file_path = os.path.join(PROJECT_DIR, "src", "data", "n_movies.csv")
        return pd.read_csv(file_path)


if __name__ == "__main__":
    NetflixAnalysis().main()



