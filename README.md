The code builds a backend service for internal pricing service:

Assumptions:
1) We have the pricing json to look at the prices of the product and corresponding VAT
2) The same VAT rates apply to all countries and currencies.
3) We have calculated total price(includes vat) ,total vat, and  a json of product, total price,quantity, currency

TechStack:
The app uses Flask and python 3.6. 
The service can be tested with any of the tools. I have used curl to demo the service.


Installation instructions:
1) Create your virtual environment in python and activate it
   virtualenv -p python 3.6 <yourenvname>
2) pip install -r requirements.txt
3) Run python priceapp.py

**How to see the list of orders?**
```curl -i http://localhost:5000/todo/api/v1.0/tasks```

```
Sample Result:
{
       "id": 12345,
       "customer": {},
       "items": [
           {
               "product_id": 1,
               "quantity": 1
           },
           {
               "product_id": 2,
               "quantity": 5
           },
           {
               "product_id": 3,
               "quantity": 1
           }
       ]
   }```

Total for the order_id: 12345
curl -i http://localhost:5000/todo/api/v1.0/tasks/12345

```{
     "order": {
       "Total_Price": 2218.8, 
       "Total_vat": 119.8, 
       "currency": "GBP", 
       "particulars": [
         {
           "product_id": 1, 
           "total_price_per_product": 599, 
           "vat_total": 119.8
         }, 
         {
           "product_id": 2, 
           "total_price_per_product": 1250, 
           "vat_total": 0
         }, 
         {
           "product_id": 3, 
           "total_price_per_product": 250, 
           "vat_total": 0
         }
       ]
     }
   }```

**To convert to different currency just suffix the currency to GBP_XXX
e.g for EURO 
     GBP_EUR
     GBP_USD
     GBP_PHP**

**Endpoint when tails.com decides to go overseas. End Point in EURO's :** 

```curl -i http://localhost:5000/todo/api/v1.0/tasks/12345/GBP_EUR```

```
{
  "order": {
    "Total_Price": 2662.56, 
    "Total_vat": 119.8, 
    "currency": "EUR", 
    "particulars": [
      {
        "product_id": 1, 
        "total_price_per_product": 599, 
        "vat_total": 119.8
      }, 
      {
        "product_id": 2, 
        "total_price_per_product": 1250, 
        "vat_total": 0
      }, 
      {
        "product_id": 3, 
        "total_price_per_product": 250, 
        "vat_total": 0
      }
    ]
  }
}
```


#How to add an order?

#curl -i -H "Content-Type: application/json" -X POST -d '{"items":[{\"product_id\": 1,\"quantity\":1}]}' http://localhost:5000/todo/api/v1.0/tasks