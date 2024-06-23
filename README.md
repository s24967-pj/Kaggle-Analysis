# Kaggle-Analysis

## Opis

Projekt to webowy dashboard do wizualizacji danych z Netflixa. Dashboard zawiera analizy najpopularniejszych gatunków filmowych, najlepiej ocenianych filmów oraz interaktywne tabele w których można wyszukać filmy w których występuje dany aktor, lub posortować filmy wg. rankingu. Stworzony w Pythonie z wykorzystaniem m.in. bibliotek Dash, Plotly i Pandas.

## Objaśnienie użytych bibliotek

W projekcie użyłam biblioteki Plotly, Dash, ponieważ, pozwalały na ładniejsze zobrazowanie danych oraz umożliwiały ułożenie dashborda w odpowiedni dla mnie sposób. Zawierały one funkcje, których brakowało mi w matplotlib m.in. interaktywność i scrollbar. Uważam, że dzięki nim, prezentacja danych jest bardziej atrakcyjna i funkcjonalna.

## Funkcje jakie posiada projekt

- Wizualizacja najlepiej ocenianych filmów
- Tabela z tytułem i oceną filmu
  - umożliwiająca filtrowanie tytułów
  - umożliwiająca sortowanie filmów wg. ocen
  - umożliwiająca filtrowanie ocen
- Wizualizacja najczęstszych gatunków filmowych za pomocą wykresu kołowego
  - z możliwością zmiany typu wartości, z procentowego na liczbowy
- Tabela z tytułami filmów oraz występującymi w nich aktorami
  - z możliwością filtrowania filmów w których występuje podany aktor
- Testy jednostkowe dot. kilku konkretnych funkcji

## Instalacja pliku requirements.txt

pip install -r requirements.txt

## Struktura i relacja klas

Klasa main.py - służy do uruchomienia całego projektu

Klasa dataframe.py - pozwala załadować dane z pliku csv oraz oczyścić dataframe'a z duplikatów

Klasa netflixanalysis.py - główna klasa projektowa, zdefiniowane są w niej serwisy, służy do załadowania całej wizualizacji projektu

Klasa figureservice.py oraz tableservice.py - tworzą grafy i tabele

Klasa unittest.py - Zawiera testy jednostkowe funkcjonalności z klasy 'NetflixAnalysis', za pomocą unittest. Weryfikują m.in. poprawność wczytania danych, pokazania danych w wykresach oraz odpowiednie wczytanie wykresów.

## Wyjaśnienie dobranych metod obrazowania danych

- Tabela aktorów i filmów:
  - Umożliwia to szybki przegląd dostępnych filmów z wybranym aktorem. Tabela jest prostym, ale skutecznym sposobem na przeglądanie dużej ilości danych w sposób uporządkowany i zrozumiały. Szczególnie w przypadku możliwości wyszukiwania danych, gdzie pokazywane są tylko filmy w których dany aktor występuje.
- Wykres kołowy popularnych gatunków
  - Wykres kołowy, wydaje się jednym z najlepszych typów do przedstawienia danych procentowych. Jest to bardzo dobry sposób do przedstawienia procentowego podziału najczęściej występujących gatunków, co pozwala na łatwe porównanie i identyfikację dominujących trendów wśród gatunków filmowych.
- Wykres liniowy najlepiej ocenianych filmów
  - Taki wykres umożliwia zobaczenie jak wysoko oceniany jest film w konkretnej skali (w tym przypadku 0-10). W prosty i skuteczny sposób pokazuje praktycznie maxymalnie osiągnięte wartości w ocenach.
- Tabela rankingu filmów
  - Umożliwia użytkownikowi wyszukanie wszystkich filmów w interesującym go przedziale. Z racji, że może być dużo wysoko ocenianych filmów użytkownik ma możliwość zobaczenia wszystkich dostępnych filmów. Dzięki sortowaniu jest także możliwość znalezienia filmów których nie warto oglądać, przez ich niskie oceny.
