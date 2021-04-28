import uvicorn
from ariadne.contrib.federation.schema import make_federated_schema
from ariadne.contrib.federation.objects import FederatedObjectType
from ariadne.objects import QueryType
from ariadne.asgi import GraphQL

reviews = [
    {
        "id": "1",
        "authorUsername": "@ada",
        "product": {"upc": "1"},
        "body": "Love it!",
    },
    {
        "id": "2",
        "authorUsername": "@ada",
        "product": {"upc": "2"},
        "body": "Too expensive.",
    },
    {
        "id": "3",
        "authorUsername": "@ada",
        "product": {"upc": "3"},
        "body": "Could be better.",
    },
    {
        "id": "4",
        "authorUsername": "@complete",
        "product": {"upc": "1"},
        "body": "Prefer something else.",
    },
]

type_defs = """ 
type Query {
   firstReview: Review
}

type Review @key(fields: "id") {
    id: ID!
    body: String
    author: User
    product: Product
  }

  type User @key(fields: "username") @extends {
    id: ID! @external
    username: String! @external
    reviews: [Review]
  }

  type Product @key(fields: "upc") @extends {
    upc: String! @external
    reviews: [Review]
  }
"""

query = QueryType()
user = FederatedObjectType("User")
product = FederatedObjectType("Product")
review = FederatedObjectType("Review")


@review.reference_resolver
def resolve_review_reference(*_, representation):
    return next(filter(lambda x: x["id"] == representation.get("id"), reviews))


@review.field("author")
def resolve_review_author(review, *_):
    return {"username": review["authorUsername"]}


@review.field("product")
def resolve_review_product(review, *_):
    return {"upc": review["product"]["upc"]}


@user.field("reviews")
def resolve_user_reviews(representation, *_):
    return list(
        filter(lambda r: r["authorUsername"] == representation["username"], reviews)
    )


@product.field("reviews")
def resolve_product_reviews(representation, *_):
    return list(filter(lambda r: r["product"]["upc"] == representation["upc"], reviews))


@query.field("firstReview")
def resolve_first_review(*_):
    return reviews[0]


schema = make_federated_schema(type_defs, query, user, product, review)
application = GraphQL(schema)

if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=5003)
