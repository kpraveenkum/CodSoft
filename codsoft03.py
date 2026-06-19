import numpy as np
import pandas as pd
cats = ['books', 'movies']
cur = None
df = None
def load(cat):
    if cat == 'books':
        return pd.DataFrame({
            'id': range(1, 11),
            'title': ['The God of Small Things', 'A Suitable Boy', 'The White Tiger',
                      'Midnight Children', 'The Palace of Illusions', 'Train to Pakistan',
                      'The Guide', 'Interpreter of Maladies', 'The Immortals of Meluha', 'Revolution 2020'],
            'author': ['Arundhati Roy', 'Vikram Seth', 'Aravind Adiga', 'Salman Rushdie',
                       'Chitra Banerjee', 'Khushwant Singh', 'R.K. Narayan', 'Jhumpa Lahiri',
                       'Amish Tripathi', 'Chetan Bhagat'],
            'genre': ['literary', 'classic', 'crime', 'magical realism', 'mythology',
                      'historical', 'philosophical', 'short stories', 'mythology', 'romance'],
            'rating': [4.8, 4.7, 4.5, 4.9, 4.6, 4.7, 4.8, 4.5, 4.4, 4.2],
            'year': [1997, 1993, 2008, 1981, 2008, 1956, 1958, 1999, 2010, 2011],
            'pages': [340, 1349, 321, 647, 360, 201, 220, 198, 410, 290]
        })
    elif cat == 'movies':
        return pd.DataFrame({
            'id': range(1, 11),
            'title': ['3 Idiots', 'Dangal', 'Baahubali 2', 'RRR', 'Lagaan',
                      'Gully Boy', 'Andhadhun', 'Drishyam', 'Zindagi Na Milegi Dobara', 'Hera Pheri'],
            'director': ['Rajkumar Hirani', 'Nitesh Tiwari', 'S.S. Rajamouli', 'S.S. Rajamouli', 'Ashutosh Gowariker',
                         'Zoya Akhtar', 'Sriram Raghavan', 'Nishikant Kamat', 'Zoya Akhtar', 'Priyadarshan'],
            'genre': ['commedy/drama', 'biopic/sports', 'action/drama', 'action/drama', 'sports/drama',
                      'drama/music', 'thriller/mystery', 'thriller/drama', 'comedy/drama', 'comedy'],
            'rating': [8.4, 8.5, 8.2, 8.0, 8.1, 7.9, 8.3, 8.6, 8.2, 8.0],
            'year': [2009, 2016, 2017, 2022, 2001, 2019, 2018, 2015, 2011, 2000],
            'duration': [170, 161, 167, 187, 224, 153, 139, 143, 155, 156]
        })
def menu1():
    print("RECOMMENDATION SYSTEM")
    print("What would you like to discover today?")
    for i, c in enumerate(cats, 1):
        print(f"{i}. {c.upper()}")
    print("3. Exit")
def by_genre(g):
    res = df[df['genre'].str.contains(g, case=False, na=False)]
    if len(res) > 0:
        return res.sort_values('rating', ascending=False).head(5)
    else:
        print(f"sorry, no {g} {cur} found in our database")
        return pd.DataFrame()
def similar(item):
    if item not in df['title'].values:
        print(f"'{item}' nit found in our {cur} database")
        return pd.DataFrame()
    cols = [c for c in df.columns if c not in ['id', 'title', 'author', 'director']]
    minmax = df[cols].copy()
    for c in cols:
        min_val = minmax[c].min()
        maxx_val = minmax[c].max()
        if maxx_val > min_val:
            minmax[c] = (minmax[c] - min_val) / (maxx_val - min_val)
        else:
            minmax[c] = 0
    idx = df[df['title'] == item].index[0]
    vec = minmax.iloc[idx].values.reshape(1, -1)
    dots = np.dot(minmax.values, vec.T).flatten()
    norms1 = np.sqrt(np.sum(minmax.values ** 2, axis=1))
    norms2 = np.sqrt(np.sum(vec ** 2, axis=1))
    sims = dots / (norms1 * norms2[0])
    idxs = np.argsort(sims)[::-1][1:6]
    res = df.iloc[idxs][['title'] + (['author'] if cur == 'books' else ['director'])]
    return res
def top_rated(y=None):
    tmp = df
    if y:
        tmp = tmp[tmp['year'] >= y]
    return tmp.sort_values('rating', ascending=False).head(5)
def menu2():
    global cur, df
    while True:
        print("=" * 40)
        print(f" {cur.upper()} RECOMMENDATIONS")
        print("=" * 40)
        print("how would you like too recommendations?")
        print("1. recommend by genre")
        print("2. find similar items")
        print("3. show top rated items")
        print("4. change category")
        print("5. exit system")
        try:
            opt = int(input("\nyou'r choice: "))
            if opt == 1:
                print(f"\navailable genres in {cur}:")
                all_g = set()
                for g in df['genre']:
                    for gg in str(g).split('/'):
                        all_g.add(gg.strip())
                print(", ".join(sorted(all_g)))
                g = input("\neenter a genre you like: ").strip()
                res = by_genre(g)
                if not res.empty:
                    print(f"\ntop {cur} recommendations in '{g}':")
                    print("-" * 50)
                    for _, r in res.iterrows():
                        if cur == 'books':
                            print(f"{r['title']} by {r['author']} (rating: {r['rating']})")
                        else:
                            print(f"{r['title']} directed by {r['director']} (rating: {r['rating']})")
            elif opt == 2:
                print(f"\navailable {cur}:")
                for t in df['title'].values:
                    print(f"  • {t}")
                item = input("\nenter the title you like: ").strip()
                res = similar(item)
                if not res.empty:
                    print(f"\niif you liked '{item}', you might also enjoy it :")
                    print("-" * 50)
                    for _, r in res.iterrows():
                        if cur == 'books':
                            print(f"{r['title']} by {r['author']}")
                        else:
                            print(f"{r['title']} directed by {r['director']}")
            elif opt == 3:
                fy = input("\nfilter by year? (yep/nope): ").lower()
                if fy == 'y':
                    y = int(input("enter minimum year: "))
                    res = top_rated(y)
                else:
                    res = top_rated()
                print(f"\ntop rated {cur} in our collection:")
                print("-" * 50)
                for _, r in res.iterrows():
                    if cur == 'books':
                        print(f"{r['title']} by {r['author']} - {r['rating']}/5.0")
                        print(f" genre: {r['genre']} | Year: {r['year']} | Pages: {r['pages']}")
                    else:
                        print(f"{r['title']} by {r['director']} - {r['rating']}/10.0")
                        print(f"genre: {r['genre']} | Year: {r['year']} | Duration: {r['duration']} min")
                    print()
            elif opt == 4:
                print("\nreturning to main category selection...")
                break
            elif opt == 5:
                print("\nthank you for using the Recommendation System!")
                print("happy exploring! Goodbye!")
                return None
            else:
                print("invalid option. Please choose 1-5")
        except ValueError:
            print("please enter a valid number")
            continue
def start():
    global cur, df
    while True:
        menu1()
        ch = int(input("\nenter your choice (1-3): "))
        if ch == 3:
            print("\nthank you for using the Recommendation System!")
            print("happy exploring! Goodbye!")
            break
        elif 1 <= ch <= 2:
            cur = cats[ch - 1]
            print(f"\nyou selected: {cur.upper()}")
            df = load(cur)
            print(f"\nloaded {len(df)} {cur} in our database")
            menu2()
        else:
            print("Invalid choice. Please select 1, 2, or 3")

if __name__ == "__main__":
    start()
