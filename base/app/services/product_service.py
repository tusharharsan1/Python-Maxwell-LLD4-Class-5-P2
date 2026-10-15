"""The ProductService: the business rules for products.

Read README.md first. Your job is to finish the two methods marked TODO.
Do not rename the methods or their parameters.
"""

# A product is "low stock" when its stock is below this number.
LOW_STOCK_LIMIT = 10

# The "database" for this problem: a dictionary that lives in memory.
# The products are kept in this order (by id). Do NOT change it.
PRODUCTS = {
    1: {"id": 1, "title": "Essence Mascara Lash Princess", "price": 9.99, "stock": 99},
    2: {"id": 2, "title": "Eyeshadow Palette with Mirror", "price": 19.99, "stock": 6},
    3: {"id": 3, "title": "Powder Canister", "price": 14.99, "stock": 10},
    4: {"id": 4, "title": "Red Lipstick", "price": 12.99, "stock": 0},
    5: {"id": 5, "title": "Red Nail Polish", "price": 8.99, "stock": 52},
    6: {"id": 6, "title": "Calvin Klein CK One", "price": 49.99, "stock": 3},
    7: {"id": 7, "title": "Chanel Coco Noir Eau De", "price": 129.99, "stock": 41},
}


class ProductService:
    def _with_flags(self, product: dict) -> dict:
        """EXAMPLE, already finished. Returns a NEW dictionary: the product plus "low_stock"."""
        return {**product, "low_stock": product["stock"] < LOW_STOCK_LIMIT}

    def get_by_id(self, product_id: int) -> dict | None:
        """EXAMPLE, already finished. Returns one product with its flag, or None."""
        product = PRODUCTS.get(product_id)
        if product is None:
            return None
        return self._with_flags(product)

    def list_products(self, page: int, size: int) -> list[dict]:
        """TASK 1: return ONE page of products, each one with the "low_stock" flag.

        Page numbers start at 0. `size` is how many products are on a page.
        Keep the products in the same order as in PRODUCTS.
        Use self._with_flags(...) for every product.
        """
        # TODO 1: write the code here, then delete the line that starts with "raise".
        raise NotImplementedError("TODO 1 is not done yet")

    def list_low_stock_products(self, page: int, size: int) -> list[dict]:
        """TASK 2: return ONE page of the products that are low stock.

        Pages work exactly as in Task 1 (page 0 is the first page), but only
        the low stock products are counted. First pick the low stock products,
        then take the page from them.
        Use self._with_flags(...) so that the rule is written in only one place.
        """
        # TODO 2: write the code here, then delete the line that starts with "raise".
        raise NotImplementedError("TODO 2 is not done yet")
