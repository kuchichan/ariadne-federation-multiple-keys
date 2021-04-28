## Ariadne Federation Demo With multiple keys

This repository is an Ariadne demo, heavily inspired by the [apollo federation-demo](https://github.com/apollographql/federation-demo) extended by multiple primary keys functionality for `User` entity. For the example purposes, additional `split_payment_service.py` was introduced using different `User` primary key in comparison with `review_service.py `

### Installation

To run this demo, [poetry](https://python-poetry.org) is needed. Pull down the repository and run the following commands:

```sh
npm install
poetry install
```

This will install all of the dependencies for the gateway and Ariadne underlying services, respectively. 

**NOTE**: Poetry will install Ariadne's specific branch which is still not merged into master, so following example will fail for Ariadne installed via `pip install ariadne`. 

```sh
poetry run npm run start-services
npm run start-gateway
```

This commands will run all four microservices, and apollo gateway, respectively (should be ran in different terminals). Services will start at the ports 5001 - 5004, gateway will run at
<http://localhost:4000>

## Example Queries (interesting ones)

Ofc, "interesting" is highly subjective here :) 

```qraphql
query{
  me {
    reviews {
      body
      author {
        id
        username
      }
      product {
        price
      }
    }
  }
}
```

```qraphql
query{
  payments {
    participants {
      name
    }
  }
}
```
