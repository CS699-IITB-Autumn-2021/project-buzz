DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS rating;
DROP TABLE IF EXISTS user_session;
DROP TABLE IF EXISTS sex;

DROP TABLE IF EXISTS credentials;
<<<<<<< HEAD
DROP TABLE IF EXISTS usersession;
DROP TABLE IF EXISTS products_comments;
=======
>>>>>>> master
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
	contact_no integer NOT NULL,
	sex_id integer,
	roll_no integer NOT NULL,
	valid boolean NOT NULL,
	created_at timestamp default current_timestamp ,
	updated_at timestamp default current_timestamp ,
	deleted_at timestamp  
	
);

CREATE TABLE sex(
<<<<<<< HEAD
	id integer PRIMARY KEY AUTOINCREMENT ,
	name text,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp 
=======
	sex_id integer PRIMARY KEY AUTOINCREMENT ,
	sex_type text
>>>>>>> master

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
<<<<<<< HEAD
	id varchar PRIMARY KEY,
=======
	user_id varchar PRIMARY KEY,
>>>>>>> master
	token varchar NOT NULL,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
<<<<<<< HEAD
	FOREIGN KEY(id) REFERENCES USER(user_id)
);

CREATE TABLE credentials (
	id varchar PRIMARY KEY,
=======
	FOREIGN KEY(user_id) REFERENCES USER(user_id)
);

CREATE TABLE credentials (
	user_id varchar PRIMARY KEY,
>>>>>>> master
	refresh_token varchar NOT NULL,
	access_token varchar NOT NULL,
	valid boolean NOT NULL default 1,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
<<<<<<< HEAD
	FOREIGN KEY(id) REFERENCES USER(user_id)
);

CREATE TABLE products (
	id integer  PRIMARY KEY AUTOINCREMENT,
=======
	FOREIGN KEY(user_id) REFERENCES USER(user_id)
);

CREATE TABLE products (
	product_id integer  PRIMARY KEY AUTOINCREMENT,
>>>>>>> master
	category_id integer default 1, 
	user_id varchar, 
	product_description text,
	title text NOT NULL,
	product_availability integer,
	spam integer DEFAULT 0 ,
	selling_option integer,
	bid_id integer,
	bid_inc integer,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
	FOREIGN KEY(user_id) REFERENCES USER(user_id) ,
<<<<<<< HEAD
	FOREIGN KEY(category_id) REFERENCES CATEGORIES(id)
	FOREIGN KEY(bid_id) REFERENCES BID(id)
	FOREIGN KEY(selling_option) REFERENCES selling_opt(id)
=======
	FOREIGN KEY(category_id) REFERENCES CATEGORIES(category_id)
	FOREIGN KEY(bid_id) REFERENCES BID(bid_id)
>>>>>>> master
);
CREATE TABLE product_tags (
	product_id integer ,
	tag_id integer,
<<<<<<< HEAD
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
=======
>>>>>>> master
	PRIMARY KEY(product_id , tag_id)
);

CREATE TABLE tags (
<<<<<<< HEAD
	id integer PRIMARY KEY AUTOINCREMENT,
	name text
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp 
);

CREATE TABLE categories ( 
	id integer PRIMARY KEY AUTOINCREMENT ,
	name text ,
=======
	tag_id integer PRIMARY KEY AUTOINCREMENT,
	tag_name text
);

CREATE TABLE categories ( 
	category_id integer PRIMARY KEY AUTOINCREMENT ,
	category_name text ,
>>>>>>> master
	valid boolean default 1, 
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp 
);

CREATE TABLE bid (
	product_id integer  ,
<<<<<<< HEAD
	id integer PRIMARY KEY AUTOINCREMENT,
=======
	bid_id integer PRIMARY KEY AUTOINCREMENT,
>>>>>>> master
	user_id varchar,
	bid_price integer,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
	FOREIGN KEY(user_id) REFERENCES USER(user_id),
<<<<<<< HEAD
	FOREIGN KEY(product_id) REFERENCES PRODUCT(id)
);

CREATE TABLE images (
	id varchar PRIMARY KEY,
=======
	FOREIGN KEY(product_id) REFERENCES PRODUCT(product_id)
);

CREATE TABLE images (
	image_id varchar PRIMARY KEY,
>>>>>>> master
	product_id integer ,
	image_url varchar,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp ,
<<<<<<< HEAD
	FOREIGN KEY(product_id) REFERENCES PRODUCT(id)
);

CREATE TABLE selling_opt ( 
	id integer PRIMARY KEY AUTOINCREMENT,
	name text,
=======
	FOREIGN KEY(product_id) REFERENCES PRODUCT(product_id)
);

CREATE TABLE selling_opt ( 
	selling_option integer PRIMARY KEY AUTOINCREMENT,
	selling_type text,
>>>>>>> master
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
<<<<<<< HEAD
	FOREIGN KEY(product_id) REFERENCES PRODUCT(id)
=======
	FOREIGN KEY(product_id) REFERENCES PRODUCT(product_id)
>>>>>>> master
);

CREATE TABLE product_comments (
	product_id integer ,
<<<<<<< HEAD
	id varchar PRIMARY KEY,
=======
	comment_id varchar PRIMARY KEY,
>>>>>>> master
	visibility boolean default 0,
	likes integer DEFAULT 0,
	dislikes integer DEFAULT 0,
	spam integer DEFAULT 0,
	
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,
	deleted_at timestamp  ,
<<<<<<< HEAD
	FOREIGN KEY(product_id) REFERENCES PRODUCT(id) 
=======
	FOREIGN KEY(product_id) REFERENCES PRODUCT(product_id) 
>>>>>>> master
);












