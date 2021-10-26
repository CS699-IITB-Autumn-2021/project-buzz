DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS rating;
DROP TABLE IF EXISTS user_session;
DROP TABLE IF EXISTS sex;

DROP TABLE IF EXISTS credentials;
DROP TABLE IF EXISTS usersession;
DROP TABLE IF EXISTS products_comments;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS product_tags;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS bid;
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS selling_opt;
DROP TABLE IF EXISTS sold_to;
DROP TABLE IF EXISTS product_comments;









CREATE TABLE user (
	user_id varchar PRIMARY KEY,
	first_name text,
	last_name text,
	email varchar NOT NULL,
	contact_no varchar NOT NULL,
	sex_id integer,
	roll_no integer NOT NULL,
	valid boolean NOT NULL,
	created_at timestamp default current_timestamp ,
	updated_at timestamp default current_timestamp ,
	deleted_at timestamp  
	
);

CREATE TABLE sex(
	id integer PRIMARY KEY AUTOINCREMENT ,
	name text,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp 

);

CREATE TABLE rating (
	user_id varchar,
	rating integer CHECK (rating <=10),
	comments varchar,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
	FOREIGN KEY(user_id) REFERENCES USER(user_id)
);

CREATE TABLE user_session (
	id varchar PRIMARY KEY,
	token varchar NOT NULL,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
	FOREIGN KEY(id) REFERENCES USER(user_id)
);

CREATE TABLE credentials (
	id varchar PRIMARY KEY,
	refresh_token varchar NOT NULL,
	access_token varchar NOT NULL,
	valid boolean NOT NULL default 1,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
	FOREIGN KEY(id) REFERENCES USER(user_id)
);

CREATE TABLE products (
	id varchar  PRIMARY KEY ,
	category_id integer default 1, 
	user_id varchar, 
	product_description text,
	price integer default 0,
	title text NOT NULL,
	product_availability integer,
	likes integer DEFAULT 0,
	dislikes integer DEFAULT 0,
	spam integer DEFAULT 0 ,
	selling_option integer,
	bid_base integer,
	bid_inc integer,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
	FOREIGN KEY(id) REFERENCES USER(user_id) ,
	FOREIGN KEY(category_id) REFERENCES CATEGORIES(id)
	FOREIGN KEY(bid_base) REFERENCES BID(id)
	FOREIGN KEY(selling_option) REFERENCES selling_opt(id)
);
CREATE TABLE product_tags (
	product_id integer ,
	tag_id integer,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
	PRIMARY KEY(product_id , tag_id)
);

CREATE TABLE tags (
	id integer PRIMARY KEY AUTOINCREMENT,
	name text
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp 
);

CREATE TABLE categories ( 
	id integer PRIMARY KEY AUTOINCREMENT ,
	name text ,
	valid boolean default 1, 
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp 
);

CREATE TABLE bid (
	product_id integer  ,
	id integer PRIMARY KEY AUTOINCREMENT,
	user_id varchar,
	bid_price integer,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
	FOREIGN KEY(user_id) REFERENCES USER(user_id),
	FOREIGN KEY(product_id) REFERENCES PRODUCT(id)
);

CREATE TABLE images (
	id integer PRIMARY KEY AUTOINCREMENT DEFAULT 0,
	product_id varchar ,
	image_url varchar,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
	FOREIGN KEY(product_id) REFERENCES PRODUCT(id)
);

CREATE TABLE selling_opt ( 
	id integer PRIMARY KEY AUTOINCREMENT,
	name text,
	created_at timestamp default current_timestamp ,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp 
	
);

CREATE TABLE sold_to (
	product_id integer ,
	user_id varchar,
	quantity integer,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
	FOREIGN KEY(user_id) REFERENCES USER(user_id) ,
	FOREIGN KEY(product_id) REFERENCES PRODUCT(id)
);

CREATE TABLE product_comments (
	product_id integer ,
	id varchar PRIMARY KEY,
	visibility boolean default 0,
	likes integer DEFAULT 0,
	dislikes integer DEFAULT 0,
	spam integer DEFAULT 0,
	
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp  ,
	FOREIGN KEY(product_id) REFERENCES PRODUCT(id) 
);












