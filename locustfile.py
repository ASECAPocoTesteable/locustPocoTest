import json
from locust import HttpUser, task, between
import random
import string


class ShopUser(HttpUser):
    host = 'http://localhost:8080'
    wait_time = between(1, 5)

    @task
    def get_items(self):
        self.client.get("/shop")

    @task
    def add_product(self):
        name = ''.join(random.choices(string.ascii_letters, k=10))
        price = random.randint(1, 1000)
        self.client.post("/shop/product/add", json={"name": name, "price": price})

    @task
    def checkout(self):
        products = [{"productId": 1, "quantity": random.randint(1, 10)} for _ in range(5)]
        direction = "North"
        create_order_request = {"products": products, "direction": direction}
        self.client.post("/order/checkout", json=create_order_request, headers={"Content-Type": "application/json"})


class BrowseUser(HttpUser):
    host = 'http://localhost:8080'
    wait_time = between(1, 5)

    @task
    def view_products(self):
        self.client.get("/shop")

    @task
    def view_single_product(self):
        product_id = random.randint(1, 100)
        self.client.get(f"/product/getById?id={product_id}")


class CheckoutUser(HttpUser):
    host = 'http://localhost:8080'
    wait_time = between(1, 5)

    @task
    def checkout_process(self):
        products = [{"productId": 1, "quantity": random.randint(1, 10)} for _ in range(5)]
        direction = "South"
        create_order_request = {"products": products, "direction": direction}
        self.client.post("/order/checkout", json=create_order_request, headers={"Content-Type": "application/json"})
