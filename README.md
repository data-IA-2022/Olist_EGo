# Olist_EGo
Exemple projet Olist

```sql
drop view items_info;

create or replace view items_info as
  select
    oi.*,
    p.product_category_name,
    s.seller_zip_code_prefix,
    gs.lat as seller_lat,
    gs.lng as seller_lng,
    c.customer_zip_code_prefix,
    gc.lat as customer_lat,
    gc.lng as customer_lng,
    distance(gs.lat, gs.lng, gc.lat, gc.lng) / 1000 as distance,
    avg(r.review_score) as score_moy
  from olist_order_items_dataset oi
  left join olist_products_dataset p
    using (product_id)
  left join olist_orders_dataset o
    using (order_id)
  left join olist_customers_dataset c
    using (customer_id)
  left join olist_sellers_dataset s
    using (seller_id)
  left join olist_order_reviews_dataset r
    using (order_id)
  left join avg_geo gc
    on c.customer_zip_code_prefix = gc.zip_code 
  left join avg_geo gs
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

select count(*) from items_info;
select count(*) from olist_order_items_dataset ooid;

select count(*) from items_info where distance <= 50;
```
