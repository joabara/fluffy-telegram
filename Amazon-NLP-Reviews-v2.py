#!/usr/bin/env python
# coding: utf-8

# # NLP on Amazon Laptop Reviews
# 
# ### MSCA 31008 - Summer 2021
# * Alessandro Joabar
# * Adam Schuller
# * Bogdan Constantinescu
# * Bryan E Duff
# 
# ## Objective
# We would like to leverage Amazon customer review and rating data to understand three key things:
# 
# * What do customers want in a product that would yield a high rating? 
# * Does brand actually matter?
# * What are some of the key trends in reviews and rating by brand?

# 
# ## Data
# We are going to import the Amazon laptop review data. This data was generated by taking the various Laptop brands in our initial dataset, and pulling the top 10 SKUs on Amazon and their respective reviews and ratings via a RapidAPI subscription. We chose to aggregate the laptop reviews by brand rather than product for a few reasons:
# 
# * Products can have slight differences in specs but be categorized as different products, and they can create a lot of unecessary granularity in our data
# 
# * Overall, a brand's products will all share similiar traits, and we would expect this to show in the data (i.e, Apple: expensive but beautiful; Asus: extremely reliable, high quality; etc.)
# 

# In[162]:


import pandas as pd
import numpy as np
import scipy as scp
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

reviews = pd.read_csv('reviews.csv')
reviews = reviews.drop(columns='Unnamed: 0')
reviews.head()


# Starting from the top, here are the highest rated brands based on average rating.

# In[163]:


top = reviews.groupby('Company').mean()
top['Number of Reviews'] = reviews.groupby('Company').sum()
top.sort_values(by='Rating', ascending=False).head(10)


# ## Methodology
# 
# In NLP, reducing dimensionality is crucial. We will use `TfidfVectorizer` to break apart the review terms. From there, we can apply PCA to reduce dimensionality.

# In[164]:


# Import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
text = reviews['Review']

# Create a TfidfVectorizer: tfidf
tfidf = TfidfVectorizer() 

# Apply fit_transform to csr matrix
review_vector = tfidf.fit_transform(text)
review_vector.shape


# Looking at the initial terms we vectorized, we are seeing a lot of individual terms which are not really relevant. In the next step we will do two things:
# * Remove terms with numbers (tentative)
# * We will do language checks to remove random typos (for this exercise, English, Spanish, French)

# In[165]:


words = tfidf.get_feature_names()
words[0:20]


# In[166]:


rev_array = review_vector.toarray()
words_df = pd.DataFrame(rev_array, columns = words)
words_df.head()


# There are two important filters we need to use when parsing through the unique words in these reviews:
# * We should remove strings with numbers since they seem to be irrelevant outside a specific context. We also notice a large boost in model score when we add this filter.
# * To remove typo's, we will leverage the `enchant` library to check that these terms are in the dictionary. This will help us remove words that might not be helpful.
# 
# We noticed that some words being filtered out had a negative impact on model score, so we only check a few different languages. This can be improved upon in future versions.
# 
# Note: We can implement an autocorrect feature to send typo's to their intended term.

# In[167]:


import enchant
eng = enchant.Dict("en")
span = enchant.Dict('es')
fre = enchant.Dict('fr')
de = enchant.Dict('de')
it = enchant.Dict('it')
# nl = enchant.Dict('nl')
# pt = enchant.Dict('pt_PT')
# tk = enchant.Dict('tk')
drops = []
for column in words_df.columns:
    english = eng.check(column)
    spanish = span.check(column)
    french = fre.check(column)
    german  = de.check(column)
    italian = it.check(column)
    dutch = nl.check(column)
    portug = pt.check(column)
    turkish = tk.check(column)
    if any(map(str.isdigit, column)): 
        drops.append(column)
    if not(english | spanish | french | german | italian):
        drops.append(column)

words_df = words_df.drop(columns = drops)
words_df.head()


# Through this filtering we've removed almost 2K words. This will help reduce dimensionality when we create models to predict rating score.

# In[168]:


# Apply fit_transform to csr matrix
review_vector = scp.sparse.csr_matrix(words_df.values)
review_vector.shape


# In[169]:


from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
svd = TruncatedSVD(n_components=1000)
svd.fit(review_vector)
features = range(svd.n_components) 
fig, ax = plt.subplots(figsize=(10,6))
ax.set_title("Fraction of Explained Variance")
ax.set_xlabel("Dimension #")
ax.set_ylabel("Explained Variance Ratio")
plt.plot(features, svd.explained_variance_ratio_)
ax


# We have 6985 distinct terms in our review data. By using TruncatedSVD, we can reduce dimensionality down to 777 components to explain ~85% in variance.

# In[170]:


n_comps = 0
ev = 0
for comp in svd.explained_variance_ratio_:
    if ev + comp <= 0.85:
        n_comps = n_comps + 1
        ev = ev + comp

print("Optimal N Components: " + str(n_comps))
print("Explained Variance: " + str(ev))


# In[171]:


svd2 = TruncatedSVD(n_components = n_comps)
t = svd2.fit_transform(review_vector)
t = pd.DataFrame(t)
t.shape


# We can fit that data back to a data frame and list the columns accordingly.

# In[172]:


for column in t:
        col = t[column]
        col_name = t[column].name
        new_name = "Component_" + str(col_name)
        t = t.rename(columns={col_name: new_name})
t['Rating'] = reviews['Rating']
t.head()


# In[173]:


words_df['Rating'] = reviews['Rating']
words_df.head()


# Here we are going to write functions that will help us classify how a customer might rate a laptop based on the words used in their review. Now, you might ask, "Why do you want to create a model that predicts the rating of a product after it has already launched and reviewed? Where is the value in that?"
# 
# If this model is effective, a business will be able use this model and other text data to better predict how a product might be received in the marketplace. Furthermore, if a company is designing a new product, they can predict whether or not it will be recieved well based on consumer insight data they collect pre-launch.
# 
# For example, if Asus is testing a brand new laptop for 2023, and they have collected surveys and reviews from a test audience, they can actually run those reviews through the model and predict the customer reaction to the product quantitatively.

# In[181]:


from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

def build_models_on_train(df, model, X_train, X_test, y_train, y_test):   
    classifier = model()
    classifier.fit(X_train, y_train)
    return classifier

def select_best_model_score(df):
    # Partition data into features and labels
    feature_cols = df.columns[df.columns != 'Rating']
    X = df[feature_cols] # Features
    y = df.Rating # Label
    
    # Create train and test segments
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=0)
    
    models_to_run = [LogisticRegression, LinearSVC, KNeighborsClassifier, 
                 DecisionTreeClassifier, RandomForestClassifier, GaussianNB,
                Perceptron, SGDClassifier]
    
    # Score tracking
    max_score = 0
    max_build = 0
    max_RMSE = 999
    
    for algo in models_to_run:
        build = build_models_on_train(df, algo, X_train, X_test, y_train, y_test)
        pred = build.predict(X_test)
        RMSE = np.sqrt(metrics.mean_squared_error(y_test, pred))

        if RMSE < max_RMSE:
            max_score = build.score(X_test, y_test)
            max_build = build
            max_RMSE = RMSE
            
    predicted = max_build.predict(X_test)
    print()
    print("Best build model is: ")
    print(max_build)
    print("Build model score (Accuracy): " + str(max_score))
    print("MAE = {:5.4f}".format(metrics.mean_absolute_error(y_test, predicted)))
    print("MSE = {:5.4f}".format(metrics.mean_squared_error(y_test, predicted)))
    print("RMSE = {:5.4f}".format(np.sqrt(metrics.mean_squared_error(y_test, predicted))))
    output = pd.DataFrame()
    inp = pd.DataFrame()
    inp['Ratings'] = y_test
    output['Ratings'] = predicted
    # sns.distplot(inp['Ratings'])
    # sns.distplot(output['Ratings']).set_title(str(max_build) + " Test vs. Predicted")
    
    return max_build, predicted


# We are going to build two models: 
# * Mark 1 will be with all the words found in the reviews predicting on Rating
# * Mark 2 will be the truncated SVD dataset predicting on Rating

# In[182]:


# Run on original text dimensions
mk1 = select_best_model_score(words_df)


# In[183]:


# Run on truncatedSVD
mk2 = select_best_model_score(t)


# ## Conclusion
# 
# It seems that the Mark I model is better at predicting customer rating based on the text found in the review. One of the things it seems to do very well is rate products accurately on overall positive or negative. It classifies the majority of  reviews in 1,2 star or 4,5 stars. It does have a little trouble with more nuanced reviews at 3 stars. Three stars can often mean there are some good or bad parts of a review so the model likely gets confused with those nuances.
# 
# In conclusion, we would want to export the Perceptron model to help laptop / reviewing companies. In the next steps below I will highlight how we can implement this model into production to drive business value.

# ## Next Steps & Business Implementation
# 
# There are two key improvments we will make to improve our model's effectiveness for enterprise level servicing.
# 
# Firstly, we will expand our Amazon API subscription / develop web scraping to increase a) the number of API calls for products we can look at and b) the number of reviews we can pull per product. In our implementation above, we used ~ 400 calls and we're only getting a depth of 10 reviews. We would like to remove these limits to improve review volume.
# 
# As for the implementation, there are three key steps.
# 
# First, the model must be stored and run on an Azure/AWS server. This is important because it allows for secure and scalable storage and performance for our model. We would also be able to create a load balancer for security and availability.
# 
# Secondly, we must develop an API that can 1) receive reviews data from clients, 2) store client subscription keys and 3) send back predictive outputs in a timely manner. 
# 
# Lastly, we can monetize this API by publishing it to RapidAPI and selling tiered subscriptions. This way, we can have a consistent revenue stream to upkeep to server costs. Due to customer likely to be larger firms, we can charge a premium for unlimited use at a high markup. This would allow us to have a high revenue stream and scale the server instance and model to accomodate demand.
