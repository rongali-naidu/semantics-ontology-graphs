view: products {
  derived_table: {
    sql: SELECT p.*, s.name AS seller_name
         FROM retail.products p JOIN retail.sellers s ON s.seller_id = p.seller_id ;;
  }
  dimension: product_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.product_id ;;
  }
  dimension: category_id {
    type: string
    hidden: yes
    sql: ${TABLE}.category_id ;;
  }
  dimension: sku {
    type: string
    sql: ${TABLE}.sku ;;
  }
  dimension: product_name {
    type: string
    sql: ${TABLE}.name ;;
  }
  dimension: list_price {
    type: number
    value_format_name: usd
    sql: ${TABLE}.list_price ;;
  }
  dimension: seller_name {
    type: string
    sql: ${TABLE}.seller_name ;;
  }
}
