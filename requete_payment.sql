create view payment_exos as
select ood.*, count(distinct ooid.order_item_id) as NB_items, 
			count(distinct oopd.payment_sequential) as payment_count,
			(select sum (oopd2.payment_value) as payment_somme 
			 from olist_order_payments_dataset oopd2 
			 where oopd2.order_id=ood.order_id)
from olist_orders_dataset ood 
left join olist_order_items_dataset ooid 
	using (order_id)
left join olist_order_payments_dataset oopd 
	using (order_id)
group by ood.order_id
order by NB_items desc