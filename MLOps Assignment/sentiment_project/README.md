##### Project Overview



This project focuses on classifying customer reviews as positive or negative and identifying key pain points from negative reviews.

The dataset contains real Flipkart customer reviews for the product YONEX MAVIS 350 Nylon Shuttle.



The project applies Natural Language Processing (NLP) and Machine Learning techniques to analyze customer sentiment and deploys the trained model using a Streamlit web application.



##### Objective



* Classify customer reviews into positive and negative
* Analyze negative reviews to understand customer dissatisfaction
* Build a web application for real-time sentiment prediction



##### Dataset



* Source: Flipkart (scraped by Data Engineering team)
* Total Reviews: 8,518
* Features include:
* Review Text
* Rating
* Review Title
* Place of Review
* Votes, Date, etc.





##### Technologies Used



* Python
* Pandas, NumPy
* NLTK (Text Preprocessing)
* Scikit-learn
* TF-IDF Vectorizer
* Logistic Regression
* Streamlit





##### Data Preprocessing



* Removed missing values
* Removed neutral reviews (rating = 3)
* Text cleaning (lowercasing, punctuation removal)
* Stopword removal
* Lemmatization





##### Modeling



* Feature Extraction: TF-IDF



* Models Trained:

1. Logistic Regression (Best Model)
2. Naive Bayes



* Evaluation Metric:

1. F1-Score



* Best Model Performance:

1. F1-Score ≈ 0.95





##### Insights from Negative Reviews



Common pain points identified:

* Poor quality
* Bad
* Low durability
* Waste of money
* Don’t buy





##### Web Application



* Built using Streamlit
* Takes user input (review text)
* Predicts sentiment (Positive / Negative) in real time





##### Project Structure



sentiment\_project/

│

├── app.py

├── sentiment\_model.pkl

├── tfidf\_vectorizer.pkl

├── notebooks/

│   └── sentiment\_notebook.ipynb

├── data/

│   └── data.csv

└── README.md

