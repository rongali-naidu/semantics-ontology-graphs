view: reviews {
  sql_table_name: retail.reviews ;;
  dimension: review_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.review_id ;;
  }
  dimension: product_id {
    type: string
    hidden: yes
    sql: ${TABLE}.product_id ;;
  }
  dimension: rating {
    type: number
    sql: ${TABLE}.rating ;;
  }
  measure: average_rating {
    type: average
    sql: ${rating} ;;
    value_format_name: decimal_2
  }
  measure: review_count {
    type: count
  }
}
