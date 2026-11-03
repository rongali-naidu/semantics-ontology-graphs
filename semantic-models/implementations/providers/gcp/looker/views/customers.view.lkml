view: customers {
  derived_table: {
    sql: SELECT c.*, a.city, a.state, a.country
         FROM retail.customers c LEFT JOIN retail.addresses a ON a.address_id = c.address_id ;;
  }
  dimension: customer_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.customer_id ;;
  }
  dimension: customer_name {
    type: string
    sql: ${TABLE}.name ;;
  }
  dimension: is_premium {
    type: yesno
    sql: ${TABLE}.is_premium ;;
  }
  dimension: city {
    type: string
    sql: ${TABLE}.city ;;
  }
  dimension: state {
    type: string
    map_layer_name: us_states
    sql: ${TABLE}.state ;;
  }
}
