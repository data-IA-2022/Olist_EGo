# Olist_EGo
Exemple projet Olist

![olist - public.png](olist%20-%20public.png)

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