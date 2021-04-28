import uvicorn
from ariadne.contrib.federation.schema import make_federated_schema
from ariadne.contrib.federation.objects import FederatedObjectType
from ariadne.objects import QueryType
from ariadne.asgi import GraphQL

payments = [
    {"id": "1", "participantsIDs": ["1", "2"], "amount": 90},
    {"id": "2", "participantsIDs": ["1"], "amount": 40},
    {"id": "3", "participantsIDs": ["2"], "amount": 42},
]

type_defs = """ 
  type Query {
    firstPayment: SplitPayment 
    payments: [SplitPayment]
  }

  type SplitPayment @key(fields: "id") {
    id: ID!
    participants: [User]
    amount: Int 
  }

  type User @key(fields: "id") @extends {
    id: ID! @external
    username: String! @external
    splitPayments: [SplitPayment]
  }
"""

query = QueryType()
user = FederatedObjectType("User")
split_payment = FederatedObjectType("SplitPayment")


@split_payment.reference_resolver
def resolve_split_payment_reference(*_, representation):
    return next(filter(lambda x: x["id"] == representation.get("id"), payments))


@split_payment.field("participants")
def resolve_split_payment_participants(split_payment, *_):
    return list(map(lambda user_id: {"id": user_id}, split_payment["participantsIDs"]))


@user.field("splitPayments")
def resolve_user_split_payments(representation, *_):
    return list(filter(lambda p: representation["id"] in p["participantsIDs"], payments))


@query.field("firstPayment")
def resolve_first_review(*_):
    return payments[0]


@query.field("payments")
def resolve_payments(*_):
    return payments


schema = make_federated_schema(type_defs, query, user, split_payment)
application = GraphQL(schema)

if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=5004)
