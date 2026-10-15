"""Run this file to see what your code does:   python try_it.py

You do not need to change anything in this file.
"""
from app.services.product_service import PRODUCTS, ProductService

service = ProductService()


def ids(products):
    """Only the ids of a list of products, so the output is short to read."""
    return [product["id"] for product in products]


print("Task 1: list_products")
try:
    print("  size 3, page 0 :", ids(service.list_products(0, 3)))
    print("  size 3, page 1 :", ids(service.list_products(1, 3)))
    print("  size 3, page 2 :", ids(service.list_products(2, 3)))
    print("  size 3, page 3 :", ids(service.list_products(3, 3)))
    print("  one product    :", service.list_products(0, 1)[0])
except NotImplementedError as error:
    print("  not done yet ->", error)

print("Task 2: list_low_stock_products")
try:
    print("  size 2, page 0 :", ids(service.list_low_stock_products(0, 2)))
    print("  size 2, page 1 :", ids(service.list_low_stock_products(1, 2)))
    print("  size 2, page 2 :", ids(service.list_low_stock_products(2, 2)))
    no_flag = all("low_stock" not in product for product in PRODUCTS.values())
    print("  PRODUCTS is unchanged (7 products, no low_stock key):", len(PRODUCTS) == 7 and no_flag)
except NotImplementedError as error:
    print("  not done yet ->", error)
