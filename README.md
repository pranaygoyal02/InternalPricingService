How to see the list of orders?

curl -i http://localhost:5000/todo/api/v1.0/tasks
```{
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

End point in GBP:
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

End Point for using currency converter:
curl -i http://localhost:5000/todo/api/v1.0/tasks/12345/GBP_EUR

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