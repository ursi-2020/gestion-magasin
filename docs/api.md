[Sommaire SI](https://ursi-2020.github.io/Documentation/) <br/>
[Sommaire Magasin](https://ursi-2020.github.io/gestion-magasin/)

Go to: [Endpoints](#i---endpoints), [Models](#ii---models).

## I - ENDPOINTS

### GET `/products`

---

#### *Description:*
Get all products and their information

---

#### *Query Parameters:*

No parameters

---

#### *Responses:*

Code | Content Type | Value | Parameter
---- | ------------ | ----- | ---------
`200 OK` | `application/json` |  Array of [Product](#product) | *none*

---

#### *Usages:*

`GET /product`
```json
[
  {
    "id": 796,
    "codeProduit": "X1-0",
    "familleProduit": "Frigos",
    "descriptionProduit": "Frigos:P1-0",
    "prix": 424
  },
  {
    "id": 803,
    "codeProduit": "X1-10",
    "familleProduit": "TV",
    "descriptionProduit": "TV:P3-10",
    "prix": 2624
  }
]
```
<br/>

### GET `/customers`

---

#### *Description:*
Get one or all customers information

---

#### *Query Parameters:*

Name | Type | Required | Description
---- | ---- | ---- | ----
account | String | No | Account ID of the requested client

---

#### *Responses:*

Code | Content Type | Value | Parameter
--- | --- | --- | ---
`200 OK` | `application/json` | Array of [Customer](#customer) | *none*
`200 OK` | `application/json` | [Customer](#customer) | account
`404 Not Found` | `text/html` | Error message "Customer not found" | account

---

#### *Usages:*

`GET /customers`
```json
[
  {
    "id": 97,
    "firstName": "Jean",
    "lastName": "Eddison-18",
    "fidelityPoint": 0,
    "payment": 0,
    "account": "BKN1CST18"
  },
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

---


`GET /customers?account=BKN1CST18`
```json
{
  "id": 97,
  "firstName": "Jean",
  "lastName": "Eddison-18",
  "fidelityPoint": 0,
  "payment": 0,
  "account": "BKN1CST18"
}
```

---

`GET /customers?account=LOL`
```
Customer 'LOL' does not exist.
```

<br/>

## II - MODELS 


### `Product`
```
{
  "id": <INTEGER>,
  "codeProduit": <STRING>,
  "familleProduit": <STRING>,
  "descriptionProduit": <STRING>,
  "prix": <INTEGER>
}
```

---

### `Customer`
```
{
  "id": <INTEGER>,
  "firstName": <STRING>,
  "lastName": <STRING>,
  "fidelityPoint": <INTEGER>,
  "payment": <INTEGER>,
  "account": <STRING>
}
```
