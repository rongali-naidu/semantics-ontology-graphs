view: categories {
  sql_table_name: retail.categories ;;
  dimension: category_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.category_id ;;
  }
  # The ontology's recursive tree, flattened into drillable levels
  dimension: category_level_1 {
    label: "Department"
    type: string
    sql: ${TABLE}.category_level_1 ;;
    drill_fields: [category_level_2]
  }
  dimension: category_level_2 {
    type: string
    sql: ${TABLE}.category_level_2 ;;
    drill_fields: [category_level_3]
  }
  dimension: category_level_3 {
    type: string
    sql: ${TABLE}.category_level_3 ;;
    drill_fields: [products.product_name]
  }
}
