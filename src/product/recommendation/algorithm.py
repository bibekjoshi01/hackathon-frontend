from sklearn.neighbors import NearestNeighbors
import numpy as np

from src.product.recommendation.product_matrix import get_user_product_matrix

# we've built a basic Collaborative Filtering recommendation system using the K-Nearest Neighbors (KNN) algorithm with Django and exposed the recommendations via a REST API using Django REST Framework.

# Step 1: Collect interaction data from user clicks and purchases.
# Step 2: Build a user-product interaction matrix.
# Step 3: Train a KNN model to find similar users and recommend products.
# Step 4: Expose the recommendations via a REST API.


def get_product_recommendations(user_id, num_recommendations=5):
    user_product_matrix = get_user_product_matrix()

    model = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=10)
    model.fit(user_product_matrix.values)

    user_index = user_product_matrix.index.get_loc(user_id)
    distances, indices = model.kneighbors(
        user_product_matrix.iloc[user_index, :].values.reshape(1, -1)
    )

    recommended_products = set()
    for idx in indices[0]:
        similar_user_products = user_product_matrix.iloc[idx, :]
        similar_user_products = similar_user_products[similar_user_products > 0].index
        recommended_products.update(similar_user_products)

    recommended_products = list(recommended_products)[:num_recommendations]

    return recommended_products
