# Olist_EGo
Exemple projet Olist

![olist - public.png](olist%20-%20public.png)

# Execution Appli

```shell
# Environnement
conda activate dataIA
# Execution locale (BDD docker)
OLIST='postgresql://postgres@docker-postgres/olist' flask --app olist_flask run --port 5099 --debug
```
# Docker Datalab

Utiliser la clé ~/.ssh/id_ed_github qui permet de se connecter sur $DATALAB (user github)  
Copier contenu dans "Env1", secret "SSH_KEY"   
Créer secret "OLIST_DB_URL" avec "postgresql://writer:****@127.0.0.1/olist" (BDD localhost sur VM)

# Table geolocation bis:

```roomsql
CREATE TABLE public.olist_geolocation_bis (
	zip_code varchar(5) NOT NULL,
	geolocation_lat float8 NULL,
	geolocation_lng float8 NULL,
	n int2 NULL,
	CONSTRAINT olist_geolocation_bis_pk PRIMARY KEY (zip_code)
);

insert into olist_geolocation_bis (
  select G.geolocation_zip_code_prefix as zip_code
	, avg(G.geolocation_lat) as lat
	, avg(G.geolocation_lng) as lng
	, count(*) as N
  from olist_geolocation G
  group by G.geolocation_zip_code_prefix
);
```

## Table sellers et customers
Suppression des zip codes inconnus dans geolocation (2 tables):
```roomsql
select S.seller_zip_code_prefix 
from olist_sellers S
left join olist_geolocation_bis G on (S.seller_zip_code_prefix=G.zip_code)
where G.zip_code is null;

update olist_sellers set seller_zip_code_prefix =null 
where seller_zip_code_prefix in (
select S.seller_zip_code_prefix 
from olist_sellers S
left join olist_geolocation_bis G on (S.seller_zip_code_prefix=G.zip_code)
where G.zip_code is null
);
```


## Calcul de distance entre 2 pts

Formule d'Haversine (http://www.movable-type.co.uk/scripts/latlong.html)  
https://stackoverflow.com/questions/10034636/postgresql-latitude-longitude-query  
```roomsql
CREATE OR REPLACE FUNCTION distance(
    lat1 double precision,
    lon1 double precision,
    lat2 double precision,
    lon2 double precision)
  RETURNS double precision AS
$BODY$
DECLARE
    R integer = 6371e3; -- Meters
    rad double precision = 0.01745329252;
    φ1 double precision = lat1 * rad;
    φ2 double precision = lat2 * rad;
    Δφ double precision = (lat2-lat1) * rad;
    Δλ double precision = (lon2-lon1) * rad;
    a double precision = sin(Δφ/2) * sin(Δφ/2) + cos(φ1) * cos(φ2) * sin(Δλ/2) * sin(Δλ/2);
    c double precision = 2 * atan2(sqrt(a), sqrt(1-a));    
BEGIN                                                     
    RETURN R * c;        
END  
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
```

Vue générale:
```roomsql
create OR replace view all_info as 
select O.*
	--, P.*
	--, C.*
	, G1.geolocation_lat as lat_cust, G1.geolocation_lng as lng_cust
	, G2.geolocation_lat as lat_sell, G2.geolocation_lng as lng_sell
from olist_order_items I
left join olist_orders O on (I.order_id=O.order_id)
--left join olist_order_payments P on (O.order_id=P.order_id)
left join olist_products P on (I.product_id=P.product_id)
left join olist_customers C on (O.customer_id=C.customer_id)
left join olist_geolocation_bis G1 on (C.customer_zip_code_prefix=G1.zip_code)
left join olist_sellers S on (I.seller_id=S.seller_id)
left join olist_geolocation_bis G2 on (S.seller_zip_code_prefix=G2.zip_code);
```

Affichage des distances: 
```roomsql
select I.order_id, lat_cust, lng_cust, lat_sell, lng_sell, distance(lat_cust, lng_cust, lat_sell, lng_sell)/1000 as "dist(km)"
from all_info I;
```


Vue globale items

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
