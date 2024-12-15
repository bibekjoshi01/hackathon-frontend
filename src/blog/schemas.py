from drf_spectacular.utils import OpenApiTypes

sub_category_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "slug": {"type": "string"},
            "postCount": {"type": "integer"},
            "subCategories": {"type": "array", "items": {"type": "object"}},
        },
    },
}
