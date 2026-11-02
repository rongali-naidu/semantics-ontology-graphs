view: order_lines {
  sql_table_name: retail.order_lines ;;

  dimension: order_line_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.order_line_id ;;
  }
  dimension: order_id {
    type: string
    sql: ${TABLE}.order_id ;;
  }
  dimension: product_id {
    type: string
    hidden: yes
    sql: ${TABLE}.product_id ;;
  }
  dimension: quantity {
    type: number
    sql: ${TABLE}.quantity ;;
  }
  dimension: unit_price {
    type: number
    value_format_name: usd
    sql: ${TABLE}.unit_price ;;
  }
  dimension: line_amount {
    type: number
    value_format_name: usd
    sql: ${quantity} * ${unit_price} ;;
  }

  measure: revenue {
    description: "Sum of quantity * unit price paid"
    type: sum
    sql: ${line_amount} ;;
    value_format_name: usd
    drill_fields: [orders.order_id, customers.customer_name, products.product_name, revenue]
  }
  measure: units_sold {
    type: sum
    sql: ${quantity} ;;
  }
  measure: order_count {
    type: count_distinct
    sql: ${order_id} ;;
  }
  measure: average_order_value {
    type: number
    sql: ${revenue} / NULLIF(${order_count}, 0) ;;
    value_format_name: usd
  }
  measure: discount_amount {
    type: sum
    sql: ${quantity} * (${products.list_price} - ${unit_price}) ;;
    value_format_name: usd
  }
}
