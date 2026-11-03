-- Product dimension with the category tree flattened into levels
select p.product_id, p.sku, p.name as product_name, p.list_price,
       cat.name as category_name, cat.category_level_1, cat.category_level_2, cat.category_level_3,
       s.name as seller_name
from {{ ref('products') }} p
join {{ ref('categories') }} cat on cat.category_id = p.category_id
join {{ ref('sellers') }}    s   on s.seller_id     = p.seller_id
