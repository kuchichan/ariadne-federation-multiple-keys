import uvicorn
from ariadne.contrib.federation.schema import make_federated_schema
from ariadne.contrib.federation.objects import FederatedObjectType
from ariadne.objects import QueryType
from ariadne.asgi import GraphQL

products = [
    {"upc": "1", "name": "Table", "price": 899, "weight": 100},
    {"upc": "2", "name": "Couch", "price": 1299, "weight": 1000},
    {"upc": "3", "name": "Chair", "price": 54, "weight": 50},
]

type_defs = """ 
  type Query {
    topProducts(first: Int = 5): [Product]
  }

  type Product @key(fields: "upc") {
    upc: String!
    name: String
    price: Int
    weight: Int
  }
"""

product = FederatedObjectType("Product")
query = QueryType()


@product.reference_resolver
def resolve_product_reference(_, info, representation):
    return next(filter(lambda x: x["upc"] == representation.get("upc"), products))


@query.field("topProducts")
def resolve_top_products(query, info, **args):
    return products[: args["first"]]


schema = make_federated_schema(type_defs, product, query)
application = GraphQL(schema)

if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=5002)
