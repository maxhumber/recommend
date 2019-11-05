import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
import pytest

from recommend import AdjacentNeighbors, ThingVectorizer
from recommend import Recommend

@pytest.fixture
def X():
    X = np.array([
        [0, 0, 1, 0, 1, 0, 1],
        [1, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 1],
        [0, 1, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 1, 1, 0, 1],
    ])
    return X

def test_an_works_like_cdist(X):
    an = AdjacentNeighbors(n=3)
    an.fit(X)
    dist, _ = an.kneighbors(X, return_distance=True)
    result = (dist == cdist(X, X))
    assert result.all()

def test_nearest_neighbors(X):
    an = AdjacentNeighbors(n=3)
    an.fit(X)
    r = an.kneighbors(X[0].reshape(1, -1))
    assert (r == np.array([[0, 2, 3]])).all()

# Ryan -> write a test that will make sure it's returning the right number of neighbours
# write here

@pytest.fixture
def df():
    df = pd.DataFrame([
        [1, 'a,b,c,d'],
        [2, 'a,c,d,e'],
        [3, 'f,g,h,i'],
        [4, 'b,c,h,i'],
        [5, 'j,k,l'],
        [6, 'k,l'],
    ], columns=['user', 'items'])
    return df

def test_thing_vectorizer(df):
    tv = ThingVectorizer()
    tv.fit(df['items'])
    r = tv.transform(['c,h'])
    assert (r == np.array([[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]])).all()

# Kavitha -> write a test for different delimiters like ' '
# write here

# Hock -> write a test for max_features, make sure it picks up the right number
# write here

@pytest.fixture
def food():
    food = pd.DataFrame([
        ['Ryan', 'thai,mexican,indian,hawaiian'],
        ['Kavitha', 'thai,mexican,indian'],
        ['Hock', 'thai,sushi,ethiopian'],
        ['Benoit', 'thai,french,italian,ethiopian']
    ], columns=['name', 'food'])
    return food

def test_nn_recommender(food):
    r = Recommend(n=2)
    r.fit(food['food'])
    anika = ['ethiopian,italian']
    results = r.predict(anika)
    assert set(results[0]) == {'french', 'sushi', 'thai'}

# Benoit -> write a test that will fail or return no neighbours
# write here

# Anika -> write a test that can accept two new users and see their results
# write here
@pytest.fixture
def food():
    food = pd.DataFrame([
        ['Ryan', 'thai,mexican,indian,hawaiian'],
        ['Kavitha', 'thai,mexican,indian'],
        ['Hock', 'thai,sushi,ethiopian'],
        ['Benoit', 'thai,french,italian,ethiopian']
    ], columns=['name', 'food'])
    return food
def test_new_user(food):
    r = Recommend(n = 1)
    r.fit(food['food'])
    predictions = {}
    new_users = pd.DataFrame([
        ['Rowena', ['thai,viet,french']],
        ['Melissa', ['thai,korean,sushi']]
    ], columns = ['name', 'food'])
    i = 0
    for user in new_users['food']:
        prediction = r.predict(user)
        predictions.update({new_users['name'][i]: set(prediction[0])})
        i+= 1
    assert predictions == {'Rowena' : set(['italian','ethiopian']), 'Melissa' : set(['ethiopian'])}
