-- ===========================================================================
-- Retail warehouse - physical tables under every semantic model in this repo
-- Generated data: data/*.csv (python scripts/rdf_to_tables.py)
-- Schema name used by the vendor models: retail   (e.g. retail.order_lines)
-- Portable SQL: runs on SQLite, DuckDB, PostgreSQL, Snowflake, BigQuery,
-- Databricks with at most type-name tweaks.
-- ===========================================================================

-- Dimensions -----------------------------------------------------------------
CREATE TABLE addresses (
  address_id   VARCHAR(20) PRIMARY KEY,
  city         VARCHAR(100),
  state        VARCHAR(10),
  postal_code  VARCHAR(20),
  country      VARCHAR(2)
);

CREATE TABLE customers (
  customer_id  VARCHAR(20) PRIMARY KEY,
  name         VARCHAR(200) NOT NULL,
  email        VARCHAR(200) NOT NULL UNIQUE,
  is_premium   BOOLEAN NOT NULL,
  member_since DATE,                       -- only for premium customers
  address_id   VARCHAR(20) REFERENCES addresses(address_id)
);

CREATE TABLE sellers (
  seller_id    VARCHAR(20) PRIMARY KEY,
  name         VARCHAR(200) NOT NULL
);

-- The ontology's recursive subCategoryOf tree, flattened to fixed levels
-- (BI tools model hierarchies as levels, not recursion)
CREATE TABLE categories (
  category_id         VARCHAR(30) PRIMARY KEY,
  name                VARCHAR(100) NOT NULL,
  parent_category_id  VARCHAR(30) REFERENCES categories(category_id),
  category_level_1    VARCHAR(100),        -- e.g. Electronics
  category_level_2    VARCHAR(100),        -- e.g. Computers
  category_level_3    VARCHAR(100)         -- e.g. Laptops
);

CREATE TABLE products (
  product_id   VARCHAR(20) PRIMARY KEY,
  sku          VARCHAR(30) NOT NULL UNIQUE,
  name         VARCHAR(200) NOT NULL,
  list_price   DECIMAL(10,2) NOT NULL,
  category_id  VARCHAR(30) REFERENCES categories(category_id),
  seller_id    VARCHAR(20) REFERENCES sellers(seller_id)
);

-- Facts ----------------------------------------------------------------------
CREATE TABLE orders (                      -- grain: one row per order
  order_id         VARCHAR(20) PRIMARY KEY,
  customer_id      VARCHAR(20) NOT NULL REFERENCES customers(customer_id),
  order_date       DATE NOT NULL,
  status           VARCHAR(20) NOT NULL,   -- PLACED | SHIPPED | DELIVERED | CANCELLED
  payment_method   VARCHAR(20),
  ship_address_id  VARCHAR(20) REFERENCES addresses(address_id)
);

CREATE TABLE order_lines (                 -- grain: one row per order line  <- main fact
  order_line_id  VARCHAR(30) PRIMARY KEY,
  order_id       VARCHAR(20) NOT NULL REFERENCES orders(order_id),
  product_id     VARCHAR(20) NOT NULL REFERENCES products(product_id),
  quantity       INTEGER NOT NULL CHECK (quantity > 0),
  unit_price     DECIMAL(10,2) NOT NULL    -- price actually paid
);

CREATE TABLE reviews (                     -- grain: one row per review
  review_id    VARCHAR(20) PRIMARY KEY,
  customer_id  VARCHAR(20) NOT NULL REFERENCES customers(customer_id),
  product_id   VARCHAR(20) NOT NULL REFERENCES products(product_id),
  rating       INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
  review_text  VARCHAR(2000)
);
