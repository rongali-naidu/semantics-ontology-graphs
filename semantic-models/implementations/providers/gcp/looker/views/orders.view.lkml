view: orders {
  sql_table_name: retail.orders ;;

  dimension: order_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.order_id ;;
  }
  dimension: customer_id {
    type: string
    hidden: yes
    sql: ${TABLE}.customer_id ;;
  }
  dimension_group: order {
    type: time
    datatype: date
    timeframes: [date, week, month, quarter, year]
    sql: ${TABLE}.order_date ;;
  }
  dimension: status {
    type: string
    sql: ${TABLE}.status ;;
  }
  dimension: payment_method {
    type: string
    sql: ${TABLE}.payment_method ;;
  }
  measure: buyer_count {
    type: count_distinct
    sql: ${customer_id} ;;
  }
}
