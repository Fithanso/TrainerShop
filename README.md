**Important notes**

1. I use PostgreSQL.
2. There must be a customer with id = 0 in your database, because when a customer places an order
without being logged in, customer_id for the order is set to 0. A constraint should be followed.
3. In clean_backup you can find a DB backup containing only some global settings and admin's account.
Use mail@gmail.com and 'admin' as login and password.
4. Parts of system that were planned: couriers subsystem, subsystem of distribution of goods by delivery boxes. 
Just have no more interest in implementing them. Decided to move on to Django. 