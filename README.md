# Gestion Magasin

### GET /products/
Response: JSON Array
```
[
  {
    "id": 796,
    "codeProduit": "X1-0",
    "familleProduit": "Frigos",
    "descriptionProduit": "Frigos:P1-0",
    "prix": 424
  },
  [...]
  {
    "id": 803,
    "codeProduit": "X1-10",
    "familleProduit": "TV",
    "descriptionProduit": "TV:P3-10",
    "prix": 2624
  }
]
```

### GET /customers/
Response: JSON Array
```
[
  {
    "id": 97,
    "firstName": "Jean",
    "lastName": "Eddison-18",
    "fidelityPoint": 0,
    "payment": 0,
    "account": "BKN1CST18"
  },
  [...]
  {
    "id": 99,
    "firstName": "Anne",
    "lastName": "Eddison-53",
    "fidelityPoint": 154,
    "payment": 3,
    "account": "BKN1CST53"
  }
]
```

### GET /customers/?account=<account_id>
Response: JSON Object

##### Example: <br> GET /customers/?account=BKN1CST18
```
{
  "id": 97,
  "firstName": "Jean",
  "lastName": "Eddison-18",
  "fidelityPoint": 0,
  "payment": 0,
  "account": "BKN1CST18"
}
```
