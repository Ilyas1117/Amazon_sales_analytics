CREATE TABLE customers (
	customer_id int PRIMARY KEY,
	customer_name text,
	city text,
	state text,
	country text
)

CREATE TABLE orders (
	order_id int primary key,
	order_date date ,
	customer_id int ,
	constraint fk_customer foreign key(customer_id) 
	references customers(customer_id),
	order_status text , 
	payment_method text ,
	shipping_cost numeric(10,2)
)

CREATE TABLE products (
	product_id int primary key ,
	product_name text ,
	category text ,
	brand text
)

CREATE TABLE order_items (
	order_id int ,
	constraint fk_order foreign key(order_id)
	references orders(order_id),
	product_id int,
	constraint fk_product foreign key(product_id)
	references products(product_id) ,
	quantity int ,
	unit_price numeric(10,2),
	discount numeric(10,2),
	tax numeric(10,2)
)

-- Топ 5 самых прибыльных товаров 

select 
p.product_name, 
p.brand , 
ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount)),2) as total_amount
from order_items oi
join products p 
on oi.product_id = p.product_id
group by p.product_name , p.brand
order by total_amount desc
limit 5

-- Количество людей по методу оплаты 

select o.payment_method , count(c.customer_name) as customer_count
from customers c
join orders o 
on o.customer_id = c.customer_id 
group by o.payment_method
order by customer_count desc

-- Средний чек по месяцам

WITH sum_amount as (
	select 
	DATE_TRUNC('month', o.order_date) AS month ,
	sum(quantity*unit_price*(1-discount)) as total_amount
	from orders o 
	join order_items oi 
	on oi.order_id = o.order_id 
	group by DATE_TRUNC('month', o.order_date) 
)

select 
month ,
round(avg(total_amount),2) as avg_check
FROM sum_amount
GROUP BY month
ORDER BY avg_check desc

-- Прибыль по категориям 

SELECT 
p.category , 
ROUND(sum(oi.quantity*oi.unit_price*(1-oi.discount)),2) as total_sales
FROM order_items oi 
JOIN products p 
ON oi.product_id = p.product_id 
GROUP BY p.category
ORDER BY total_sales DESC

-- Список клиентов, которые не совершали покупок более 3 месяцев 

SELECT c.customer_name  
FROM customers c 
JOIN orders o 
ON o.customer_id = c.customer_id
GROUP BY c.customer_name
HAVING MAX(o.order_date)<CURRENT_DATE - interval '3 months'


