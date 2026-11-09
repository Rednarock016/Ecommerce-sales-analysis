use ecommerce_create;

select sum(Revenue) as Total_Revenue
from sales;

select count(distinct Invoice) as Total_Orders
from sales;

select count(distinct `Customer ID`) as Total_Customers
from sales;

select sum(Revenue) / count(distinct Invoice) as Average_Order_Value
from sales;

select YearMonth,sum(Revenue) as Monthly_Revenue
from sales
group by YearMonth
order by YearMonth;

Select country, sum(Revenue) as Total_Revenue
from sales
group by Country
order by Total_Revenue DESC
limit 10;

select Description, sum(Revenue) as Total_Revenue, sum(Quantity) as Units_Sold
from sales
group by Description
order by Total_Revenue desc
limit 10;

Select `Customer ID`, sum(Revenue) as Total_Revenue, count(distinct Invoice) as Total_Orders
from  sales where `Customer ID` is not null
group by `Customer ID`
order by Total_Revenue desc
limit 20;

select 
		case 
			when Order_Count > 1
				then 'Repeat Customer'
			else 'one-time Customer'
        end as Customer_Type,
	count(*) as Total_customers
from ( select `Customer ID`, count(distinct Invoice) as Order_count
		from sales
        where `Customer ID` is not null
        group by `Customer ID`
) as Customer_Orders
group by Customer_type;

select Country , sum(Revenue)/count(distinct Invoice) as Average_Order_Value
from sales
group by Country
order by Average_Order_Value desc;