# Retail semantic layer - Looker LookML (https://cloud.google.com/looker/docs/what-is-lookml)
# Ossie dataset -> view, field -> dimension, metric -> measure,
# relationship -> explore join (with relationship: many_to_one).
connection: "retail_bigquery"

include: "/views/*.view.lkml"

explore: order_lines {
  label: "Retail orders"
  description: "Revenue, orders and buyers by customer, product and category"

  join: orders {
    type: left_outer
    sql_on: ${order_lines.order_id} = ${orders.order_id} ;;
    relationship: many_to_one
  }
  join: customers {
    type: left_outer
    sql_on: ${orders.customer_id} = ${customers.customer_id} ;;
    relationship: many_to_one
  }
  join: products {
    type: left_outer
    sql_on: ${order_lines.product_id} = ${products.product_id} ;;
    relationship: many_to_one
  }
  join: categories {
    type: left_outer
    sql_on: ${products.category_id} = ${categories.category_id} ;;
    relationship: many_to_one
  }
}

# Reviews are a separate fact at their own grain -> their own explore
explore: reviews {
  join: products {
    sql_on: ${reviews.product_id} = ${products.product_id} ;;
    relationship: many_to_one
  }
}
