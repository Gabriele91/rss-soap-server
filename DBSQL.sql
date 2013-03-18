
/*
member
  Column  |         Type          | Modifiers 
----------+-----------------------+-----------
 id       | integer               | not null
 name     | character varying(32) | 
 surname  | character varying(32) | 
 nickname | character varying(32) | 
 password | character varying(32) | 
 email    | character varying(32) | 
*/

DROP TABLE IF EXISTS Member;
CREATE TABLE Member (id SERIAL PRIMARY KEY, 
	                 name VARCHAR(32),
	                 surname VARCHAR(32),
	                 nickname VARCHAR(32),
	                 password VARCHAR(32), 
	                 email VARCHAR(32));

/*
rss
  Column  |          Type          | Modifiers 
----------+------------------------+-----------
 id       | integer                | not null
 title    | character varying(128) | 
 message  | text                   | 
 postdate | timestamp              | 
 idmember | integer                | not null
*/

DROP TABLE IF EXISTS Rss;
CREATE TABLE Rss (id SERIAL PRIMARY KEY, 
	              title VARCHAR(128),
	              message TEXT,
	              postdate TIMESTAMP,
	              idmember INTEGER REFERENCES Member(id) 
	              ON UPDATE CASCADE ON DELETE CASCADE);

/*
rsssite
  Column  |          Type          | Modifiers 
----------+------------------------+-----------
 id       | integer                | not null
 link     | character varying(2083)| 
 idmember | integer                | not null
*/

DROP TABLE IF EXISTS RssSite;
CREATE TABLE RssSite (id SERIAL PRIMARY KEY, 
	                  link VARCHAR(2083),
	                  idmember INTEGER REFERENCES Member(id) 
	                  ON UPDATE CASCADE ON DELETE CASCADE);
