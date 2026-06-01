create database event_management;
use event_management;

create table students (
student_id int auto_increment primary key,
name varchar(200) not null,
email varchar(200) unique not null,
phone varchar(50),
password varchar(200) not null
);

create table venues (
venue_id int auto_increment primary key,
venue_name varchar(200) not null,
location varchar(300) not null,
capacity int not null
);

create table events (
event_id int auto_increment primary key,
title varchar(200) not null,
event_date date not null,
ticket_price decimal(10,2) not null,
venue_id int,

foreign key(venue_id)
references venues(venue_id)
on delete set null
);

create table tickets (
ticket_id int auto_increment primary key,
student_id int not null,
event_id int not null,
quantity int not null,
booking_date date not null,

foreign key(student_id)
references students(student_id),
foreign key (event_id)
references events(event_id)
);

create table payments (
payment_id int auto_increment primary key,
ticket_id int not null,
amount decimal(10,2) not null,
payment_method varchar(50) default("cash"),
payment_date date not null,

foreign key(ticket_id)
references tickets(ticket_id)
);

delimiter //
create procedure add_student(
in p_name varchar(100),
in p_email varchar(100),
in p_phone varchar(20),
in p_password varchar(255))
begin
insert into students(name,email,phone,password)values(
p_name,p_email,p_phone,p_password);
end //
delimiter;

delimiter //
create procedure get_student(
in s_id  int)
begin
select*
from students
where student_id=s_id;
end //
delimiter;

delimiter //
create procedure update_student(
in s_id int,
in s_name varchar(200),
in s_email varchar(200),
in s_phone varchar(20),
in s_password varchar(255))
begin
update students
set
name = s_name,
email = s_email,
phone = s_phone,
password = s_password
where student_id = s_id;
end //
delimiter ;

delimiter //
create procedure delete_student(
in s_id int)
begin
delete from students
where student_id = s_id;
end //
delimiter ;

delimiter //
create procedure add_venue(
in p_venue_name varchar(100),
in p_location varchar(255),
in p_capacity int)
begin
insert into venues(venue_name,location,capacity)values(
p_venue_name,
p_location,
p_capacity);
end //
delimiter ;

delimiter //
create procedure get_venue(
in p_venue_id int)
begin
select *
from venues
where venue_id=p_venue_id;
end //
delimiter ;

delimiter //

create procedure update_venue(
in p_venue_id int,
in p_venue_name varchar(100),
in p_location varchar(255),
in p_capacity int)
begin
update venues
set
venue_name = p_venue_name,
location = p_location,
capacity = p_capacity
where venue_id = p_venue_id;
end //
delimiter ;

delimiter //
create procedure delete_venue(
in p_venue_id int)
begin
delete from venues
where venue_id = p_venue_id;
end //
delimiter ;

delimiter //
create procedure add_event(
in p_title varchar(100),
in p_event_date date,
in p_ticket_price decimal(10,2),
in p_venue_id int)
begin
insert into events(title,event_date,ticket_price,venue_id)values(
p_title,
p_event_date,
p_ticket_price,
p_venue_id);
end //
delimiter ;

delimiter //
create procedure get_event(
in p_event_id int)
begin
select e.event_id,e.title,e.event_date,e.ticket_price,v.venue_name
from events e
join venues v
on e.venue_id = v.venue_id
where e.event_id=p_event_id;
end //
delimiter ;

delimiter //
create procedure update_event(
in p_event_id int,
in p_title varchar(100),
in p_event_date date,
in p_ticket_price decimal(10,2),
in p_venue_id int)
begin
update events
set
title = p_title,
event_date = p_event_date,
ticket_price = p_ticket_price,
venue_id = p_venue_id
where event_id = p_event_id;
end //
delimiter ;

delimiter //
create procedure delete_event(in p_event_id int)
begin
delete from events
where event_id = p_event_id;
end //
delimiter ;

delimiter //
create procedure add_ticket(
in p_s_id int,
in p_event_id int,
in p_quantity int,
in p_booking_date date)
begin
insert into tickets(student_id,event_id,quantity,booking_date)values(
p_s_id,
p_event_id,
p_quantity,
p_booking_date);
end //
delimiter ;

delimiter //
create procedure get_tickets(in p_ticket_id int)
begin
select t.student_id,s.name,e.title,t.quantity,t.booking_date
from tickets t
join students s
on t.student_id = s.student_id
join events e
on t.event_id = e.event_id
where t.ticket_id=p_ticket_id;
end //
delimiter ;

delimiter //
create procedure update_ticket(
in p_ticket_id int,
in p_quantity int)
begin
update tickets
set
quantity = p_quantity
where ticket_id = p_ticket_id;
end //
delimiter ;

delimiter //
create procedure delete_ticket(in p_ticket_id int)
begin
delete from tickets
where ticket_id = p_ticket_id;
end //
delimiter ;

delimiter //
create procedure add_payment(
in p_ticket_id int,
in p_amount decimal(10,2),
in p_payment_method varchar(50),
in p_payment_date date)
begin
insert into payments(ticket_id,amount,payment_method,payment_date)values(
p_ticket_id,
p_amount,
p_payment_method,
p_payment_date);
end //
delimiter ;

delimiter //
create procedure get_payments(in p_payment_id int)
begin
select p.payment_id,s.name,e.title,p.amount,p.payment_method,p.payment_date
from payments p
join tickets t
on p.ticket_id= t.ticket_id
join students s
on t.student_id= s.student_id
join events e
on t.event_id= e.event_id
where p.payment_id=p_payment_id;
end //
delimiter ;

delimiter //
create procedure update_payment(
in p_payment_id int,
in p_amount decimal(10,2),
in p_payment_method varchar(50))
begin
update payments
set
amount = p_amount,
payment_method = p_payment_method
where payment_id = p_payment_id;
end //
delimiter ;

delimiter //
create procedure delete_payment(in p_payment_id int)
begin
delete from payments
where payment_id = p_payment_id;
end //
delimiter ;