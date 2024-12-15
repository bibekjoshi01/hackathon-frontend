import pandas as pd
from django.db.models import Count
from src.product.models import ProductClick, Product


def get_user_product_matrix():
    # Get all user-product interactions (clicks and purchases)
    click_data = ProductClick.objects.values("user", "product").annotate(
        clicks=Count("id")
    )
    # purchase_data = ProductPurchase.objects.values("user", "product").annotate(
    #     purchases=Count("id")
    # )

    click_df = pd.DataFrame(click_data)
    purchase_df = pd.DataFrame(purchase_data)
    data_df = pd.concat(
        [   
            click_df[["user", "product", "clicks"]],
            purchase_df[["user", "product", "purchases"]],
        ]
    )

    data_df["clicks"] = data_df["clicks"].fillna(0)
    data_df["purchases"] = data_df["purchases"].fillna(0)
    data_df["interaction_score"] = data_df["clicks"] + data_df["purchases"]

    user_product_matrix = data_df.pivot_table(
        index="user", columns="product", values="interaction_score", fill_value=0
    )
    return user_product_matrix
