import uvicorn

from ariadne.contrib.federation.schema import make_federated_schema
from ariadne.contrib.federation.objects import FederatedObjectType
from ariadne.objects import QueryType
from ariadne.asgi import GraphQL

users = [
    {
        "id": "1",
        "name": "Ada Lovelace",
        "birthDate": "1815-12-10",
        "username": "@ada",
    },
    {
        "id": "2",
        "name": "Alan Turing",
        "birthDate": "1912-06-23",
        "username": "@complete",
    },
]

type_defs = """ 
  type Query {
    me: User
  }

  type User @key(fields: "username") @key(fields: "id") {
    id: ID!
    username: String!
    name: String!
} 
"""

user = FederatedObjectType("User")
query = QueryType()


@user.reference_resolver
def resolve_user_reference(_, info, representation):
    if representation.get("username") is not None:
        return next(
            filter(lambda x: x["username"] == representation.get("username"), users)
        )
    return next(filter(lambda x: x["id"] == representation["id"], users))


@query.field("me")
def resolve_me(*_):
    return users[0]


schema = make_federated_schema(type_defs, user, query)
application = GraphQL(schema)

if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=5001)
