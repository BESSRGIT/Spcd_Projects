--- SECTION I: Create tables
--- CREATE SCHEMA public AUTHORIZATION postgres;
--- COMMENT ON SCHEMA public IS 'standard public schema';
 create
	table
		if not exists public.categories ( category_id serial not null ,
		category_name varchar(255) not null,
		description varchar(255) ,
		picture varchar(500) );

create
	table
		if not exists public.customers ( customerid varchar(5) not null ,
		companyname varchar(255) not null,
		contactname varchar(255) not null,
		contacttitle varchar(255) ,
		address varchar(255) ,
		city varchar(255) ,
		region varchar(255),
		postalcode varchar(255),
		country varchar(255) ,
		phone varchar(255) ,
		fax varchar(255) );

create
	table
		if not exists public.employee_territories ( employee_id int4 not null ,
		territory_id int4 not null );

create
	table
		if not exists public.employees ( employee_id int4 not null ,
		last_name varchar(255) not null ,
		first_name varchar(255) not null ,
		title varchar(255) ,
		title_oc varchar(255) ,
		birth_date timestamp ,
		hire_date timestamp ,
		address varchar(255) ,
		city varchar(255) ,
		region varchar(255) ,
		postal_code varchar(255) ,
		country varchar(255) ,
		home_phone varchar(255) ,
		"extension" varchar(255) ,
		photo varchar(500) ,
		notes varchar(500) ,
		reports_to int4 ,
		photo_path varchar(255) );


create
	table
		if not exists public.order_details ( order_id int4 not null ,
		product_id int4 not null ,
		unit_price float4 ,
		quantity int4 ,
		discount float4 );

create
	table
		if not exists public.orders ( orderid int4 not null ,
		customerid varchar(255) not null ,
		employeeid int4 not null ,
		orderdate timestamp not null ,
		requireddate timestamp ,
		shippeddate_str varchar(255) ,
		shipvia int4 ,
		freight float4 ,
		shipname varchar(255) ,
		shipadress varchar(255) ,
		shipcity varchar(255) ,
		shipregion varchar(255) ,
		shippostalcode varchar(255) ,
		shipcountry varchar(255)
		) ;

create
	table
		if not exists public.products ( product_id int4 not null ,
		product_name varchar(255) not null ,
		supplier_id int4 not null ,
		category_id int4 not null ,
		quantity_per_unit varchar(255) ,
		unit_price float4 ,
		units_in_stock int4 ,
		units_on_order int4 ,
		reorder_level int4 ,
		discontinued int4 );

create
	table
		if not exists public.regions ( region_id int4 not null ,
		region_description varchar(255) );

create
	table
		if not exists public.shippers ( shipper_id serial not null ,
		company_name varchar(255) ,
		phone_number varchar(255) );

create
	table
		if not exists public.suppliers ( supplierid int4 not null ,
		companyname varchar(255) not null,
		contactname varchar(255) null ,
		contacttitle varchar(255) ,
		address varchar(255) ,
		city varchar(255) ,
		region varchar(255) ,
		postalcode varchar(255) ,
		country varchar(255) ,
		phone varchar(255) ,
		fax varchar(255) ,
		homepage varchar(255) );

create
	table
		if not exists public.territories ( id serial not null ,
		description varchar(255) ,
		region_id int4 not null );


ALTER TABLE orders ADD COLUMN shippeddate TIMESTAMP ;
UPDATE orders SET shippeddate =( CASE WHEN shippeddate_str = 'NULL' THEN NULL ELSE shippeddate_str::timestamp END);



--- SECTION II: Adding constraints and relations
ALTER TABLE public.categories ADD CONSTRAINT categories_pk PRIMARY KEY (category_id);
ALTER TABLE public.customers ADD CONSTRAINT customers_pk PRIMARY KEY (customerid);
ALTER TABLE public.employee_territories ADD CONSTRAINT employee_territories_pk PRIMARY KEY (employee_id,territory_id);
ALTER TABLE public.employees ADD CONSTRAINT employees_pk PRIMARY KEY (employee_id);
ALTER TABLE public.order_details ADD CONSTRAINT order_details_pk PRIMARY KEY (order_id,product_id);
ALTER TABLE public.orders ADD CONSTRAINT orders_pk PRIMARY KEY (orderid);
ALTER TABLE public.products ADD CONSTRAINT products_pk PRIMARY KEY (product_id);
ALTER TABLE public.regions ADD CONSTRAINT regions_pk PRIMARY KEY (region_id);
ALTER TABLE public.shippers ADD CONSTRAINT shippers_pk PRIMARY KEY (shipper_id);
ALTER TABLE public.suppliers ADD CONSTRAINT suppliers_pk PRIMARY KEY (supplierid);
ALTER TABLE public.territories ADD CONSTRAINT territories_pk PRIMARY KEY (id);


ALTER TABLE public.products ADD CONSTRAINT products_suppliers_fk FOREIGN KEY (supplier_id) REFERENCES public.suppliers(supplierid);
ALTER TABLE public.products ADD CONSTRAINT products_categories_fk FOREIGN KEY (category_id) REFERENCES public.categories(category_id);
ALTER TABLE public.order_details ADD CONSTRAINT order_details_products_fk FOREIGN KEY (product_id) REFERENCES public.products(product_id);
ALTER TABLE public.order_details ADD CONSTRAINT order_details_orders_fk FOREIGN KEY (order_id) REFERENCES public.orders(orderid);
ALTER TABLE public.orders ADD CONSTRAINT orders_customers_fk FOREIGN KEY (customerid) REFERENCES public.customers(customerid);
ALTER TABLE public.orders ADD CONSTRAINT orders_shippers_fk FOREIGN KEY (shipvia) REFERENCES public.shippers(shipper_id);
ALTER TABLE public.orders ADD CONSTRAINT orders_employees_fk FOREIGN KEY (employeeid) REFERENCES public.employees(employee_id);
ALTER TABLE public.employees ADD CONSTRAINT employees_employees_fk FOREIGN KEY (reports_to) REFERENCES public.employees(employee_id);
ALTER TABLE public.territories ADD CONSTRAINT territories_regions_fk FOREIGN KEY (region_id) REFERENCES public.regions(region_id);
ALTER TABLE public.employee_territories ADD CONSTRAINT employee_territories_employees_fk FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id);
ALTER TABLE public.employee_territories ADD CONSTRAINT employee_territories_territories_fk FOREIGN KEY (territory_id) REFERENCES public.territories(id);


--- SECTION III: Tasks and Queries
-- Get product name and quantity/unit
select product_name, quantity_per_unit
from products;

-- Get a list of current products (Product ID and name)
select product_id, product_name
from products
where discontinued = 0;

-- Get a list of discontinued products (Product ID and name)
select product_id, product_name
from products
where discontinued = 1;

-- Get a list of the most and least expensive products (name and unit price)
select product_name, unit_price
from products
where unit_price = (
	select max(unit_price)
	from products
	);

select product_name, unit_price
from products
where unit_price = (
	select min(unit_price)
	from products
	);

-- Get products that cost less than $20
select product_name, unit_price
from products
where unit_price <= 20;

-- Get products that cost between $15 and $25
select product_name, unit_price
from products
where unit_price >= 15 and unit_price <= 20;

-- Get products above average price
select product_name, unit_price
from products
where unit_price > (
	select avg(unit_price)
	from products
	);

-- Find the ten most expensive products
select product_name, unit_price
from products
order by unit_price desc
limit 10;

-- Count current and discontinued products
select count(discontinued)
from products
where discontinued = 0;

select count(discontinued)
from products
where discontinued = 1;


-- Find products with less units in stock than the quantity on order
select product_name, units_in_stock, units_on_order
from products
where units_in_stock < units_on_order

-- Find the customer who had the highest order amount
select
 customerid,
 SUM(freight)
from
 orders
group by
 customerid
order by sum(freight) desc
limit 10;

-- Get orders for a given employee and the according customer
select orders.employeeid, orders.customerid,
	employees.last_name, employees.first_name
from orders
inner join employees on orders .employeeid = employees.employee_id
order by employeeid asc ;

-- Display the names of customers who ordered the same set of products as customers from Brazil

/*
Version with nested query didn't work
   select order_details.order_id, order_details.product_id
   from orders
   inner join order_details on orders .orderid = order_details.order_id
   where orderid = (
   		select customers.customerid, customers.country,
   		orders.orderid
		from customers
		inner join orders on customers .customerid = orders.customerid
		where country = 'Brazil');
  order by employeeid asc ;
*/

create view brazil as
	(select customers.customerid, customers.country,
		orders.orderid
	from customers
	inner join orders on customers .customerid = orders.customerid
	where country = 'Brazil');
select * from brazil  -- table, which contains all customers from brazil with according order_id

create view product_customers_i as
	(select order_details.order_id, order_details.product_id
	from order_details
	inner join brazil on order_details .order_id = brazil.orderid);
select * from product_customers_I  -- table, which contains the order_id's from "brazil" with according product_id

create view product_customers_ii as
	(select order_details.order_id, product_customers_i.product_id
	 from order_details, product_customers_i
	 where order_details.product_id = product_customers_i.product_id);
select * from product_customers_ii  -- table, which contains ALL order_id's from the determined product_id's from the table "product_customers_i"

create view product_customers_iii as
	(select orders.orderid, orders.customerid
	from orders, product_customers_ii
	where orders.orderid = product_customers_ii.order_id);
select * from product_customers_iii -- table, which connects the determined orderid's with the customerid's

create view product_customers_iv as
	(select distinct customers.customerid, customers.companyname, customers.country
	from customers, product_customers_iii
	where customers.customerid = product_customers_iii.customerid)
	order by customerid asc;
select * from product_customers_iv  -- table, which connects the determined customerid's with companie names

-- Find the hiring age of each employee
select employee_id, last_name, first_name, age(date_trunc('year', employees.birth_date), date_trunc('year', employees.hire_date))
from employees
