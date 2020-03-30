# Shopping Cart API

## Installation
#### Install Python 3:
- Please checkout https://realpython.com/installing-python/
#### Create virtual environment:
- Go to you project directory, then
```shell
> python3 -m venv env
```
```shell
> source env/bin/activate
```
#### Install requirements:
```shell
> pip install -r requirements.txt
```
## Running API Server
```shell
> python manage.py runserver
```
## Postman Collection and Environment
![postman collection](screenshots/postman-collection.png)
- [Shopping Cart API Collection and Environment](https://github.com/hty8/shopping_cart_api/tree/master/postman)

## Tests
```shell
> coverage run --source='.' manage.py test
```
```shell
> coverage report
```
![test](screenshots/test-coverage.png)

## Sample Screenshots
- List | Product
![List | Product](https://github.com/hty8/shopping_cart_api/blob/master/screenshots/2%20-%20List%20%7C%20Product%20.png?raw=true)
- Create New Coupon
![Create New Coupon](https://github.com/hty8/shopping_cart_api/blob/master/screenshots/6%20-%20Create%20New%20Coupon.png?raw=true)
- Update Existing Product
![Update Existing Product](https://github.com/hty8/shopping_cart_api/blob/master/screenshots/8%20-%20Update%20Existing%20Product.png?raw=true)
- Cart Checkout Example 1
![Cart Checkout 1](https://github.com/hty8/shopping_cart_api/blob/master/screenshots/9%20-%20Cart%20Checkout%201.png?raw=true)
- Cart Checkout Example 2
![Cart Checkout 2](https://github.com/hty8/shopping_cart_api/blob/master/screenshots/10%20-%20Cart%20Checkout%202.png?raw=true)
