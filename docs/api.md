[Sommaire SI](https://ursi-2020.github.io/Documentation/) <br/>
[Sommaire Magasin](https://ursi-2020.github.io/gestion-magasin/)

Go to: [Endpoints](#i---endpoints), [Models](#ii---models).

## I - ENDPOINTS

### GET `/products`


#### *Description:*
Get all products and their information


#### *Query Parameters:*

No parameters

#### *Responses:*

Code | Content Type | Value | Parameter
---- | ------------ | ----- | ---------
`200 OK` | `application/json` |  Array of [Product](#product) | *none*

#### *Usages:*

### GET `/api/product`
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

---

### GET `/api/customers`

#### *Description:*
Get one or all customers information

#### *Query Parameters:*

Name | Type | Required | Description
---- | ---- | ---- | ----
carteFid | String | No | Account ID of the requested client
prenom| String | No | Firstname of the requested client
nom | String | No | Lastname of the requested client


#### *Responses:*

Code | Content Type | Value | Parameter
--- | --- | --- | ---
`200 OK` | `application/json` | Array of [Customer](#customer) | *none*
`200 OK` | `application/json` | [Customer](#customer) | account
`404 Not Found` | `text/html` | Error message "Customer not found" | account


#### *Usages:*

`GET /api/customers`
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


`GET /customers?carteFid=BKN1CST18`
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

`GET /customers?carteFid=LOL`
```
Customer 'LOL' does not exist.
```

---
`GET /customers?prenom=Jean&nom=Eddison-33`
```json
[{
  "id": 97,
  "firstName": "Jean",
  "lastName": "Eddison-18",
  "fidelityPoint": 0,
  "payment": 0,
  "account": "BKN1CST18"
}]
```
---

`GET /customers?prenom=Jean&nom=Smith`
```json
[{
  "id": 97,
  "idClient": "DFF3",
  "prenom" : "Jean",
  "nom": "Smith",
  "ptsFidelite": 0,
  "paiement": 0,
  "compte": "BKN1CST18"
},
{
  "id": 982,
  "idClient": "23FF",
  "prenom": "Jean",
  "nom": "Smith",
  "ptsFidelite": 34,
  "paiement": 0,
  "compte": "BKN1CSR18"
}]
```
---
### GET `/api/sales`

#### *Description:*
Get all sales and their information

#### *Query Parameters:*

No parameters

#### *Responses:*

Code | Content Type | Value | Parameter
---- | ------------ | ----- | ---------
`200 OK` | `application/json` |  Array of [Sales](#sales) | *none*

#### *Usages:*

`GET /api/sales`
```json
[
  {
    "id": 140, 
    "date": "2019-10-23T21:07:53.809", 
    "prix": 154, "client": "", 
    "pointsFidelite": 0, 
    "modePaiement": "CASH", 
    "articles": 
      [
        {
          "codeProduit": "X1-1", 
          "familleProduit": "Console", 
          "descriptionProduit": 
          "Console:P3-1", 
          "quantiteMin": 5, 
          "packaging": 1, 
          "prix": 154, 
          "exclusivite": "0", 
          "stock": 0
         }
       ]
     }
]
```
---

### POST `/api/sendOrder`


#### *Description:*
Route to deliver an order to Magasin app

#### *Query Parameters:*

No parameters

#### *Responses:*

Code | Content Type | Value | Parameter
---- | ------------ | ----- | ---------
`200 OK` | `application/json` | Object command | *none*

#### *Usages:*

`POST /api/sendOrder`

body:
```json
{
  "idCommande": 140,
  "Produits": [
              {
                  "codeProduit": 3291,
                  "quantite": 1,
              },
              {
                  "codeProduit": 32,
                  "quantite": 11,
              },
          ]
   }
```

---
### GET `/api/stocks`

#### *Description:*
Get the stocks of all the products in the shop

#### *Query Parameters:*

No parameters

#### *Responses:*

Code | Content Type | Value | Parameter
---- | ------------ | ----- | ---------
`200 OK` | `application/json` |  Array of [Products](#products) | *none*

#### *Usages:*

`GET /api/stocks`
```json

stocks : 
[
     	{
		"codeProduit" : "Y2-7",
		"numeroFournisseur" : 1,
		"codeFournisseur" : "Y2-7",
		"stockDisponible" : 57,
	}
]
```
---

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
---
### `Sale`
```
{
  "date" : <DATE>,
  "prix" : <INTEGER>,
  "client" : <STRING>,
  "pointsFidelite" : <INTEGER>,
  "modePaiement" : <STRING>,
  "articles" : <LIST(Produit)>
}
```
