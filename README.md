The code builds a backend service for internal pricing service:

Assumptions:
1) We have the pricing json to look at the prices of the product and corresponding VAT
2) The same VAT rates apply to all countries and currencies.
3) We have calculated total price (including VAT) ,total VAT, and a json of product, total price,quantity, currency

TechStack:
The app uses Flask and python 3.6. 
The service can be tested with any of the tools. I have used curl to demo the service.


Installation instructions:
1) Create your virtual environment in python and activate it
   virtualenv -p python 3.6 <yourenvname>
2) pip install -r requirements.txt
3) Run  the Flask Application:
```python priceapp.py ```

4) Run the following curl commands to see different results at the end point.

**How to see the list of orders?**
```curl -i http://localhost:5000/todo/api/v1.0/tasks```

**Response for the order_id: 12345**
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

Testing for the pricing logic : 

I have not been able to complete the testing because of the limited time: 

1) Unit Testing of each of the method. In this app, we shall have tested 
  a) get_currency_converter_value()
  b) get_product_price(product_id)
  c) get_task_currency()

Since the method interacts with an external API we need to use mocks to test the API

2) Integration testing. It has to entail end to end testing 
e,g. when we grep the product_price of a product with get_product_price(product_id) method and get_task_currency(order,curr,total_price,total_vat)


Enhancements :( If I  had more time, what improvements would you make if any?)
1) I wanted to use memcache to implement a resource which can share data between two requests.
2) Reduce the time taken by API and also introduce a logic to retry if the API doesn't give a response in a particular 
   amount of time.
3) Add Unit Test and Integration Testing.
4) Update on order json with API POST call

Q) What bits did you find the toughest? What bit are you most proud of? In both cases, why?

Difficult bits: 
1) Implementation of Memcache. I want to replace SimpleCache with Memcache so that multiple request can share the same resource.
2) I received Proxy Error while calling the currency converter API. I couldn't resolve the proxy error at my end.

Q) What one thing could we do to improve this test?
More clear expectations around from the test might really help determine the level of details required

Work in progress:
#How to add an order?

#curl -i -H "Content-Type: application/json" -X POST -d '{"items":[{\"product_id\": 1,\"quantity\":1}]}' http://localhost:5000/todo/api/v1.0/tasks

