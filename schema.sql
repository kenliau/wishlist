drop table if exists wishlist;
create table wishlist (   
  id integer not null auto_increment,   
  userid varchar(100) not null,   
  item text not null,   
  url text null,   
  imageUrl text null, 
  priority integer not null,
  PRIMARY KEY (id) 
);
