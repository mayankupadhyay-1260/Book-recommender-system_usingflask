from timeit import default_timer as timer 

start = timer()
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# Load the dataset
books = pd.read_csv(r"database/books_new.csv")


# Drop 'Height' and 'Publisher' columns
books.drop(columns=['Height', 'Publisher',"SubGenre"], inplace=True)

# Drop rows with missing values
books.dropna(inplace=True)

# Convert all columns to lowercase
books = books.apply(lambda x: x.astype(str).str.lower())

# Remove special characters and digits from 'Title' and 'Author' columns
books['Title'] = books['Title'].apply(lambda x: re.sub(r'[^a-zA-Z]', ' ', x))
books['Author'] = books['Author'].apply(lambda x: re.sub(r'[^a-zA-Z]', ' ', x))

# Remove stopwords from 'Genre' and 'SubGenre' columns
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

books['Genre'] = books['Genre'].apply(remove_stopwords)

books['Author'] = books['Author'].apply(remove_stopwords)

# Stem the 'Genre' and 'SubGenre' columns
ps = PorterStemmer()

def stem_text(text):
    tokens = text.split()
    tokens = [ps.stem(word) for word in tokens]
    return ' '.join(tokens)

books['Genre'] = books['Genre'].apply(stem_text)

books['Author'] = books['Author'].apply(stem_text)

# Create a 'Tags' column by combining 'Genre' and 'SubGenre' columns
books['Tags'] = books['Genre'] + ' '  + books['Author'] 

# Save the preprocessed dataset to a new CSV file
books.to_csv(r"database/books_preprocessed.csv", index=False)


# Load the preprocessed dataset
books = pd.read_csv(r"database/books_preprocessed.csv")

# Replace the old genre names with new ones
genre_mapping = {
    'philosophi': 'philosophy',
    'scienc': 'science',
    'nonfict': 'nonfiction',

}

books['Genre'] = books['Genre'].replace(genre_mapping)

# Save the updated dataset to a new CSV file
books.to_csv(r"database/books_new_updated.csv", index=False)

# Load the updated  dataset
books = pd.read_csv(r"database/books_new_updated.csv")

# Create a CountVectorizer object
cv = CountVectorizer(max_features=1000, stop_words='english')

# Fit the vectorizer to the 'Tags' column and transform it into vectors
vectors = cv.fit_transform(books['Tags']).toarray()

# Calculate the cosine similarity between the vectors
similarity = cosine_similarity(vectors)


# Creating the model

def recommend(genre):
    genre = genre.lower()  # convert genre to lowercase
    genre_books = books[books['Genre'].str.lower().str.contains(genre, na=False)]
    num_books = len(genre_books)
    
    
    recommendations = []
    for _, row in genre_books.iterrows():
        book_index = books[books['Title'] == row['Title']].index[0]
        distances = similarity[book_index]
        books_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_books+1]
        for i in books_list:
            book_data = {
                'title': books.iloc[i[0]].Title,
                'author': books.iloc[i[0]].Author
            }
            recommendations.append(book_data)
    
    return recommendations[:12]  # Return only the top 12 recommendations

stop = timer()
print(stop-start)

