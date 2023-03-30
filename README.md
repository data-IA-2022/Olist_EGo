# Olist_EGo
Exemple projet Olist

```sql
create view items_info as
  select
    oi.*,
    p.product_category_name,
    s.seller_zip_code_prefix,
    gs.lat as seller_lat,
    gs.lng as seller_lng,
    c.customer_zip_code_prefix,
    gc.lat as customer_lat,
    gc.lng as customer_lng
  from olist_order_items_dataset oi
  left join olist_products_dataset p
    using (product_id)
  left join olist_orders_dataset o
    using (order_id)
  left join olist_customers_dataset c
    using (customer_id)
  left join olist_sellers_dataset s
    using (seller_id)
  left join olist_order_reviews_dataset ord
    using (order_id)
  join avg_geo gc
    on c.customer_zip_code_prefix = gc.zip_code 
  join avg_geo gs
    on s.seller_zip_code_prefix = gs.zip_code  
  group by
    oi.order_id,
    oi.order_item_id,
    p.product_id,
    s.seller_id,
    c.customer_id,
    gs.zip_code,
    gc.zip_code
;
```
