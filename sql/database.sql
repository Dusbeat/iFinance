CREATE TABLE receitas (
	t_number SERIAL primary key,
	id numeric,
	data date,
	description text,
	valor money	
);

CREATE TABLE despesas (
	t_number SERIAL primary key,
	id numeric,
	data date,
	description text,
	valor money	
);