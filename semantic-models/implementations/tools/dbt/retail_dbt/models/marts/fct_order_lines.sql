-- Main fact at order-line grain, with the order header attributes
-- MetricFlow needs (every measure must have a time dimension: order_date).
select
    ol.order_line_id,
    ol.order_id,
    o.customer_id,
    ol.product_id,
    o.order_date,
    o.status,
    o.payment_method,
    ol.quantity,
    ol.unit_price,
    ol.quantity * ol.unit_price                    as line_amount,
    ol.quantity * (p.list_price - ol.unit_price)   as discount_amount
from {{ ref('order_lines') }} ol
join {{ ref('orders') }}   o on o.order_id   = ol.order_id
join {{ ref('products') }} p on p.product_id = ol.product_id
