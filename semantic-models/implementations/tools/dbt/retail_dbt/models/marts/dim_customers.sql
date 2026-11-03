select c.customer_id, c.name as customer_name, c.email, c.is_premium, c.member_since,
       a.city, a.state, a.country
from {{ ref('customers') }} c
left join {{ ref('addresses') }} a on a.address_id = c.address_id
