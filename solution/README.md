# Product Pages at ShopNest

## Problem Statement
We have more products than fit on one screen, so the shop app asks for them **one page at a time**: "give me page 0, with 3 products on each page", then "page 1", and so on. In class, the route received `page` and `size` and cut the list into a page. Now that the rules live in the service (as we did in Class 5), the service must do this work. We also want a second list that shows only the products that are almost sold out. Complete the two methods of `ProductService`.

## Requirements
### Pages
A page is a small part of the full list of products.
- Page numbers **start at 0**. Page 0 is the first page.
- `size` is how many products fit on one page.
- Products stay in the same order as in `PRODUCTS` (id 1, 2, 3, and so on).
- The last page can have fewer than `size` products.
- A page that is past the last page is an **empty list**, `[]`. It is not an error.
- The router already checks that `page` is 0 or more and that `size` is between 1 and 100 (as in class), so you can trust the numbers you receive.

There are 7 products. With `size = 3`:

| Page | Ids of the products on the page |
|---|---|
| 0 | 1, 2, 3 |
| 1 | 4, 5, 6 |
| 2 | 7 |
| 3 | (empty list) |

With `size = 2`:

| Page | Ids of the products on the page |
|---|---|
| 0 | 1, 2 |
| 1 | 3, 4 |
| 2 | 5, 6 |
| 3 | 7 |
| 4 | (empty list) |

Where does a page start? Page 0 starts at the first product. Page 1 starts after the first `size` products. So a page starts at position `page * size` in the list, and it holds `size` products.

### Every product carries the flag
Each product in the answer must have the key `"low_stock"`, with the right `True` or `False` (low stock means its stock is below `LOW_STOCK_LIMIT`, as in the last problem).
- The method `_with_flags` already does this for one product. Use it.
- The dictionaries inside `PRODUCTS` must not change.

Example, one product:
```python
{"id": 1, "title": "Essence Mascara Lash Princess", "price": 9.99, "stock": 99, "low_stock": False}
```

### Only the low stock products
The second list shows only the products that are low stock. Pages work in the same way, but **only the low stock products are counted**. First pick the low stock products. Then take the page from them.

The low stock products are the ones with ids 2 (stock 6), 4 (stock 0) and 6 (stock 3). With `size = 2`:

| Page | Ids of the products on the page |
|---|---|
| 0 | 2, 4 |
| 1 | 6 |
| 2 | (empty list) |

If the page was taken first and the low stock products were picked after, page 0 would show only product 2. That is wrong, because a page must be full when there are enough low stock products.

To achieve these requirements we need to do 2 things:
- Complete `list_products`, which returns one page of all the products, each with its flag.
- Complete `list_low_stock_products`, which returns one page of only the low stock products.

## Instructions
1. We need to implement `list_products` inside the `ProductService` class in `app/services/product_service.py`.
2. We need to implement `list_low_stock_products` inside the same class.
3. Use `_with_flags` for every product, so that the low stock rule stays in one place.
4. Do not modify the existing methods `_with_flags` and `get_by_id`, the `PRODUCTS` dictionary, or the names and parameters of the methods. Feel free to add new methods if required.
5. Do not change the dictionaries inside `PRODUCTS`. The products you return must be copies (`_with_flags` already gives you copies).
6. Always return a list. When there is nothing on the page, return an empty list.
7. When a method is finished, delete the `raise NotImplementedError(...)` line inside it.
8. Run `python try_it.py` from this folder (the one that contains `app/` and `try_it.py`) to see what your code does. When both methods are finished, you should see exactly this:
   ```
   Task 1: list_products
     size 3, page 0 : [1, 2, 3]
     size 3, page 1 : [4, 5, 6]
     size 3, page 2 : [7]
     size 3, page 3 : []
     one product    : {'id': 1, 'title': 'Essence Mascara Lash Princess', 'price': 9.99, 'stock': 99, 'low_stock': False}
   Task 2: list_low_stock_products
     size 2, page 0 : [2, 4]
     size 2, page 1 : [6]
     size 2, page 2 : []
     PRODUCTS is unchanged (7 products, no low_stock key): True
   ```
   If you see `not done yet`, one of the methods still has its `raise` line.
9. Your code will be checked with the test file `tests/test_product_service.py`. It checks the cases in the Requirements above, and the rules in instructions 3, 4, 5 and 6. While you write your code, use `python try_it.py` (instruction 8) to check your work.
10. We will be using an in-memory dictionary for this assignment. You do not need FastAPI, a server, or any package to install.
11. Hints (all of these use ideas from class):
    - **Take part of a list with a slice.** `list[start:end]` takes the items from `start` up to, but not including, `end`. A slice that goes past the end does not give an error:
      ```python
      letters = ["a", "b", "c", "d", "e"]
      letters[1:3]     # ["b", "c"]
      letters[3:10]    # ["d", "e"]
      letters[8:10]    # []
      ```
    - **The products as a list, in order:** `list(PRODUCTS.values())`.
    - **Keep only some items with a list comprehension:**
      ```python
      numbers = [1, 2, 3, 4, 5]
      [n for n in numbers if n > 3]    # [4, 5]
      ```
    - **Where a page starts:** `start = page * size`. For page 2 and size 3, that is position 6.
