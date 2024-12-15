from django.db.models import Count, Q
from sklearn.preprocessing import MinMaxScaler
import numpy as np

from src.product.models import Product, ProductSearch


def calculate_demand_scores():
    click_counts = Product.objects.annotate(click_count=Count("clicks"))

    search_counts = Product.objects.annotate(
        search_count=Count(
            "name",
            filter=Q(
                name__icontains=ProductSearch.objects.values_list("query", flat=True)
            ),
        )
    )

    products = Product.objects.all()
    data = []
    for product in products:
        click_score = (
            click_counts.get(pk=product.id).click_count
            if product.id in click_counts
            else 0
        )
        search_score = (
            search_counts.get(pk=product.id).search_count
            if product.id in search_counts
            else 0
        )
        data.append([product.id, click_score, search_score])

    if data:
        data = np.array(data, dtype=np.float64)
        scaler = MinMaxScaler()
        normalized_scores = scaler.fit_transform(
            data[:, 1:]
        ) 

        scores = [
            {
                "product_id": int(data[i][0]),
                "demand_score": 0.7 * normalized_scores[i][0]
                + 0.3 * normalized_scores[i][1],
            }
            for i in range(len(data))
        ]

        # Sort by demand_score descending
        scores = sorted(scores, key=lambda x: x["demand_score"], reverse=True)
        return scores
    return []
