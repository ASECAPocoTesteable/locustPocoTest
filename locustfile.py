import json
from locust import HttpUser, task, between
import random
import string


# class ShopUser(HttpUser):
#     host = 'http://localhost:8080'
#     wait_time = between(1, 5)
#
#     @task
#     def get_items(self):
#         self.client.get("/shop")
#
#     @task
#     def add_product(self):
#         name = ''.join(random.choices(string.ascii_letters, k=10))
#         price = random.randint(1, 1000)
#         self.client.post("/shop/product/add", json={"name": name, "price": price})
#
#     @task
#     def checkout(self):
#         products = [{"productId": 1, "quantity": random.randint(1, 10)} for _ in range(5)]
#         direction = "North"
#         create_order_request = {"products": products, "direction": direction}
#         self.client.post("/order/checkout", json=create_order_request, headers={"Content-Type": "application/json"})
#
#
# class BrowseUser(HttpUser):
#     host = 'http://localhost:8080'
#     wait_time = between(1, 5)
#
#     @task
#     def view_products(self):
#         self.client.get("/shop")
#
#     @task
#     def view_single_product(self):
#         product_id = random.randint(1, 100)
#         self.client.get(f"/product/getById?id={product_id}")
#

class CheckoutUser(HttpUser):
    host = 'http://localhost:8080'
    wait_time = between(1, 5)

    @task
    def checkout_process(self):
        productId = random.randint(1, 1000)
        products = [{"productId": productId, "quantity": random.randint(1, 10)} for _ in range(5)]
        direction = "South"
        create_order_request = {"products": products, "direction": direction}
        response = self.client.post("/order/checkout", json=create_order_request,
                                    headers={"Content-Type": "application/json"})

        if response.status_code != 200:
            self.on_failure()

    def on_failure(self):
        self.add_products()

    def add_products(self):
        name = ''.join(random.choices(string.ascii_letters, k=10))
        price = random.randint(1, 1000)
        response = self.client.post("/shop/product/add", json={"name": name, "price": price})
        if response.status_code == 200:
            response_data = response.json()
            product_id = response_data.get("id")
            if product_id:  # Ensure the response contains an 'id'
                self.add_stock(product_id)

    def add_stock(self, product_id):
        self.client.base_url = 'http://localhost:8081'
        response = self.client.put(f"/product/{product_id}",
                                   json={"id": product_id, "addedQuantity": random.randint(1, 20)},
                                   headers={"Content-Type": "application/json"})
        self.client.base_url = self.host
        if response.status_code == 200:
            self.retry_checkout(product_id)

    def retry_checkout(self, product_id):
        products = [{"productId": product_id, "quantity": random.randint(1, 10)} for _ in range(5)]
        direction = "South"
        create_order_request = {"products": products, "direction": direction}
        self.client.post("/order/checkout", json=create_order_request,
                         headers={"Content-Type": "application/json"})