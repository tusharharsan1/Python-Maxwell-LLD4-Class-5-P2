import copy
import inspect
import os
import sys
import unittest
from unittest.mock import patch

# Lets this file run directly (python tests/test_product_service.py) from any folder.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services import product_service
from app.services.product_service import PRODUCTS, ProductService

# ---------------------------------------------------------------------------
# Test data — the products exactly as they must be at the start (README)
# ---------------------------------------------------------------------------

ORIGINAL_PRODUCTS = {
    1: {"id": 1, "title": "Essence Mascara Lash Princess", "price": 9.99, "stock": 99},
    2: {"id": 2, "title": "Eyeshadow Palette with Mirror", "price": 19.99, "stock": 6},
    3: {"id": 3, "title": "Powder Canister", "price": 14.99, "stock": 10},
    4: {"id": 4, "title": "Red Lipstick", "price": 12.99, "stock": 0},
    5: {"id": 5, "title": "Red Nail Polish", "price": 8.99, "stock": 52},
    6: {"id": 6, "title": "Calvin Klein CK One", "price": 49.99, "stock": 3},
    7: {"id": 7, "title": "Chanel Coco Noir Eau De", "price": 129.99, "stock": 41},
}

# Which products are low stock (stock below 10): ids 2, 4 and 6.
LOW_STOCK_IDS = [2, 4, 6]


# ---------------------------------------------------------------------------
# Helpers — keep the tests short and readable
# ---------------------------------------------------------------------------

def _ids(products):
    """Only the ids of a list of products."""
    return [product["id"] for product in products]


def _expected(product_id):
    """The product as it must come back: the stored data plus the right flag."""
    product = ORIGINAL_PRODUCTS[product_id]
    return {**product, "low_stock": product["stock"] < 10}


def _make_product(product_id, stock):
    """A new product, to add to PRODUCTS during a test."""
    return {"id": product_id, "title": f"Extra {product_id}", "price": 1.0, "stock": stock}


# ===========================================================================
# Test Suite 1 — Task 1: list_products
# ===========================================================================

class TestListProducts(unittest.TestCase):
    """Tests that list_products returns the right page of products."""

    def setUp(self):
        self.service = ProductService()

    # --- Which products are on which page ---

    def test_pages_of_size_3(self):
        """With size 3 the pages are [1,2,3], [4,5,6], [7] and then empty."""
        expected = {0: [1, 2, 3], 1: [4, 5, 6], 2: [7], 3: []}
        for page, ids in expected.items():
            with self.subTest(page=page):
                self.assertEqual(_ids(self.service.list_products(page, 3)), ids)

    def test_pages_of_size_2(self):
        """With size 2 the pages are [1,2], [3,4], [5,6], [7] and then empty."""
        expected = {0: [1, 2], 1: [3, 4], 2: [5, 6], 3: [7], 4: []}
        for page, ids in expected.items():
            with self.subTest(page=page):
                self.assertEqual(_ids(self.service.list_products(page, 2)), ids)

    def test_page_zero_is_the_first_page(self):
        """Page 0 must start at the very first product, not at the second."""
        self.assertEqual(_ids(self.service.list_products(0, 1)), [1])
        self.assertEqual(_ids(self.service.list_products(1, 1)), [2])

    def test_size_1_gives_one_product_per_page_in_order(self):
        """With size 1, page n holds product n + 1, and page 7 is empty."""
        for page in range(7):
            with self.subTest(page=page):
                self.assertEqual(_ids(self.service.list_products(page, 1)), [page + 1])
        self.assertEqual(self.service.list_products(7, 1), [])

    def test_a_size_bigger_than_the_number_of_products_gives_all_of_them(self):
        """Size 10 and size 100 must return all 7 products on page 0, and nothing on page 1."""
        for size in [7, 10, 100]:
            with self.subTest(size=size):
                self.assertEqual(_ids(self.service.list_products(0, size)), [1, 2, 3, 4, 5, 6, 7])
                self.assertEqual(self.service.list_products(1, size), [])

    def test_the_last_page_can_be_shorter(self):
        """The last page only holds what is left: size 4 gives [5, 6, 7] on page 1."""
        self.assertEqual(_ids(self.service.list_products(0, 4)), [1, 2, 3, 4])
        self.assertEqual(_ids(self.service.list_products(1, 4)), [5, 6, 7])

    def test_all_pages_together_give_every_product_once(self):
        """Putting the pages one after the other must give 1..7, with no gaps and no repeats."""
        for size in [1, 2, 3, 4, 5, 6, 7]:
            with self.subTest(size=size):
                collected = []
                for page in range(10):
                    collected.extend(_ids(self.service.list_products(page, size)))
                self.assertEqual(collected, [1, 2, 3, 4, 5, 6, 7])

    # --- What is on the page ---

    def test_every_product_has_all_its_fields_and_the_right_flag(self):
        """Each product must be the stored product plus the correct low_stock flag."""
        result = self.service.list_products(0, 7)
        self.assertEqual(result, [_expected(product_id) for product_id in range(1, 8)])

    def test_the_result_is_a_list_and_an_empty_page_is_an_empty_list(self):
        """Always a list, also when the page is empty (not None, not a tuple)."""
        self.assertIsInstance(self.service.list_products(0, 3), list)
        empty = self.service.list_products(9, 3)
        self.assertIsInstance(empty, list)
        self.assertEqual(empty, [])

    # --- Reads the products as they are now ---

    def test_a_product_added_later_is_on_the_last_page(self):
        """
        A new product added to PRODUCTS must show up, at the end.
        Catches students who copied the data once, or who hard-coded the ids.
        """
        with patch.dict(PRODUCTS, {8: _make_product(8, 2)}):
            self.assertEqual(_ids(self.service.list_products(1, 4)), [5, 6, 7, 8])
            self.assertEqual(_ids(self.service.list_products(2, 4)), [])
            self.assertIs(self.service.list_products(1, 4)[-1]["low_stock"], True)

    def test_the_flag_follows_the_limit(self):
        """When the limit changes, the flags on the page change with it."""
        with patch.object(product_service, "LOW_STOCK_LIMIT", 5):
            flags = {p["id"]: p["low_stock"] for p in self.service.list_products(0, 7)}
        self.assertEqual(flags, {1: False, 2: False, 3: False, 4: True, 5: False, 6: True, 7: False})

    def test_list_products_uses_with_flags_so_the_rule_is_in_one_place(self):
        """
        Every product on the page must come from self._with_flags(...).
        Catches students who copy the rule into a second place.
        """
        fake = lambda self, product: {"marker": product["id"]}
        with patch.object(ProductService, "_with_flags", fake):
            self.assertEqual(self.service.list_products(0, 2), [{"marker": 1}, {"marker": 2}])

    # --- The stored data must stay as it is ---

    def test_list_products_does_not_change_the_stored_products(self):
        """After many calls, PRODUCTS must be exactly as before, with no low_stock key inside."""
        before = copy.deepcopy(PRODUCTS)
        for page in range(5):
            self.service.list_products(page, 2)
        self.assertEqual(PRODUCTS, before)
        for product in PRODUCTS.values():
            self.assertNotIn("low_stock", product)

    def test_changing_a_returned_product_does_not_change_the_stored_one(self):
        """The products on the page must be copies: changing one must not change PRODUCTS."""
        page = self.service.list_products(0, 1)
        self.assertIsNot(page[0], PRODUCTS[1])
        page[0]["title"] = "Changed outside the service"
        self.assertEqual(PRODUCTS[1]["title"], "Essence Mascara Lash Princess")


# ===========================================================================
# Test Suite 2 — Task 2: list_low_stock_products
# ===========================================================================

class TestListLowStockProducts(unittest.TestCase):
    """Tests that list_low_stock_products pages over only the low stock products."""

    def setUp(self):
        self.service = ProductService()

    # --- Which products are on which page ---

    def test_pages_of_size_2(self):
        """Low stock products are 2, 4, 6. With size 2 the pages are [2,4], [6] and then empty."""
        expected = {0: [2, 4], 1: [6], 2: []}
        for page, ids in expected.items():
            with self.subTest(page=page):
                self.assertEqual(_ids(self.service.list_low_stock_products(page, 2)), ids)

    def test_pages_of_size_1(self):
        """With size 1 the pages are [2], [4], [6] and then empty."""
        expected = {0: [2], 1: [4], 2: [6], 3: []}
        for page, ids in expected.items():
            with self.subTest(page=page):
                self.assertEqual(_ids(self.service.list_low_stock_products(page, 1)), ids)

    def test_a_big_size_gives_all_low_stock_products(self):
        """Size 3, 10 and 100 must give all three low stock products on page 0."""
        for size in [3, 10, 100]:
            with self.subTest(size=size):
                self.assertEqual(_ids(self.service.list_low_stock_products(0, size)), LOW_STOCK_IDS)
                self.assertEqual(self.service.list_low_stock_products(1, size), [])

    def test_the_low_stock_products_are_picked_before_the_page_is_cut(self):
        """
        Page 0 of size 2 must be FULL: [2, 4]. Not just [2].
        Catches students who cut the page first and removed the other products after.
        """
        result = self.service.list_low_stock_products(0, 2)
        self.assertEqual(len(result), 2)
        self.assertEqual(_ids(result), [2, 4])

    def test_the_page_is_cut_from_the_low_stock_list_not_from_all_products(self):
        """Page 1 of size 2 must hold product 6 (the third low stock product)."""
        self.assertEqual(_ids(self.service.list_low_stock_products(1, 2)), [6])

    def test_all_pages_together_give_every_low_stock_product_once(self):
        """The pages one after the other must give 2, 4, 6 with no repeats."""
        for size in [1, 2, 3]:
            with self.subTest(size=size):
                collected = []
                for page in range(5):
                    collected.extend(_ids(self.service.list_low_stock_products(page, size)))
                self.assertEqual(collected, LOW_STOCK_IDS)

    # --- What is on the page ---

    def test_every_product_is_low_stock_and_keeps_all_its_fields(self):
        """Each product must be the stored product plus low_stock = True."""
        result = self.service.list_low_stock_products(0, 10)
        self.assertEqual(result, [_expected(product_id) for product_id in LOW_STOCK_IDS])
        for product in result:
            self.assertIs(product["low_stock"], True)

    def test_the_result_is_a_list_and_an_empty_page_is_an_empty_list(self):
        """Always a list, also when the page is empty (not None, not a tuple)."""
        self.assertIsInstance(self.service.list_low_stock_products(0, 2), list)
        empty = self.service.list_low_stock_products(5, 2)
        self.assertIsInstance(empty, list)
        self.assertEqual(empty, [])

    # --- Follows the rule and the data ---

    def test_a_limit_of_zero_means_no_product_is_low_stock(self):
        """With the limit at 0, nothing is below it, so every page is empty."""
        with patch.object(product_service, "LOW_STOCK_LIMIT", 0):
            self.assertEqual(self.service.list_low_stock_products(0, 10), [])

    def test_a_limit_of_100_means_every_product_is_low_stock(self):
        """With the limit at 100, all 7 products are low stock, and the pages cover all of them."""
        with patch.object(product_service, "LOW_STOCK_LIMIT", 100):
            self.assertEqual(_ids(self.service.list_low_stock_products(0, 3)), [1, 2, 3])
            self.assertEqual(_ids(self.service.list_low_stock_products(1, 3)), [4, 5, 6])
            self.assertEqual(_ids(self.service.list_low_stock_products(2, 3)), [7])

    def test_a_product_added_later_is_counted(self):
        """
        A new low stock product must appear, and the pages must shift.
        Catches students who hard-coded the ids 2, 4 and 6.
        """
        with patch.dict(PRODUCTS, {8: _make_product(8, 1)}):
            self.assertEqual(_ids(self.service.list_low_stock_products(0, 2)), [2, 4])
            self.assertEqual(_ids(self.service.list_low_stock_products(1, 2)), [6, 8])

    def test_a_changed_stock_changes_the_list(self):
        """When product 1 runs low, it must appear first in the low stock list."""
        with patch.dict(PRODUCTS[1], {"stock": 2}):
            self.assertEqual(_ids(self.service.list_low_stock_products(0, 10)), [1, 2, 4, 6])

    def test_list_low_stock_products_uses_with_flags_so_the_rule_is_in_one_place(self):
        """
        The 'low stock' decision must come from self._with_flags(...).
        Here _with_flags is replaced by a fake rule: odd ids are low stock.
        Catches students who wrote the rule again (stock < 10) in this method.
        """
        fake = lambda self, product: {**product, "low_stock": product["id"] % 2 == 1}
        with patch.object(ProductService, "_with_flags", fake):
            self.assertEqual(_ids(self.service.list_low_stock_products(0, 10)), [1, 3, 5, 7])
            self.assertEqual(_ids(self.service.list_low_stock_products(1, 2)), [5, 7])

    # --- The stored data must stay as it is ---

    def test_list_low_stock_products_does_not_change_the_stored_products(self):
        """After many calls, PRODUCTS must be exactly as before, with no low_stock key inside."""
        before = copy.deepcopy(PRODUCTS)
        for page in range(4):
            self.service.list_low_stock_products(page, 1)
        self.assertEqual(PRODUCTS, before)
        for product in PRODUCTS.values():
            self.assertNotIn("low_stock", product)

    def test_changing_a_returned_product_does_not_change_the_stored_one(self):
        """The products must be copies: changing one must not change PRODUCTS."""
        result = self.service.list_low_stock_products(0, 1)
        self.assertIsNot(result[0], PRODUCTS[2])
        result[0]["title"] = "Changed outside the service"
        self.assertEqual(PRODUCTS[2]["title"], "Eyeshadow Palette with Mirror")


# ===========================================================================
# Test Suite 3 — The parts that must stay as they were
# ===========================================================================

class TestPartsThatMustStayTheSame(unittest.TestCase):
    """Tests that the finished examples and the given data were not edited."""

    def setUp(self):
        self.service = ProductService()

    def test_with_flags_still_works(self):
        """The finished example must still add the flag and not change the product."""
        product = {"id": 9, "title": "Pen", "price": 1.5, "stock": 3}
        before = copy.deepcopy(product)
        result = self.service._with_flags(product)
        self.assertEqual(result, {**before, "low_stock": True})
        self.assertEqual(product, before)
        self.assertIs(self.service._with_flags({**before, "stock": 10})["low_stock"], False)

    def test_get_by_id_still_works(self):
        """The finished example must still return a flagged product, or None."""
        self.assertEqual(self.service.get_by_id(2), _expected(2))
        self.assertEqual(self.service.get_by_id(1), _expected(1))
        self.assertIsNone(self.service.get_by_id(99))

    def test_method_names_and_parameters_are_unchanged(self):
        """Method names and parameter names must stay as they were given."""
        for name, parameters in [
            ("_with_flags", ["self", "product"]),
            ("get_by_id", ["self", "product_id"]),
            ("list_products", ["self", "page", "size"]),
            ("list_low_stock_products", ["self", "page", "size"]),
        ]:
            with self.subTest(method=name):
                signature = inspect.signature(getattr(ProductService, name))
                self.assertEqual(list(signature.parameters), parameters)

    def test_the_products_dictionary_and_the_limit_were_not_edited(self):
        """PRODUCTS and LOW_STOCK_LIMIT must be exactly as they were given."""
        self.assertEqual(PRODUCTS, ORIGINAL_PRODUCTS)
        self.assertEqual(list(PRODUCTS), [1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(product_service.LOW_STOCK_LIMIT, 10)


# ===========================================================================
# Run all tests
# ===========================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
