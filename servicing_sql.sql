SELECT * FROM public.employees
ORDER BY employee_id ASC LIMIT 100


ALTER TABLE public.employees
ALTER COLUMN first_name TYPE TEXT;

ALTER TABLE public.employees
ALTER COLUMN last_name TYPE TEXT;

CREATE TABLE AES_Key_Store (table_name CHARACTER VARYING, aes_key TEXT)

select * from AES_Key_Store

select aes_key::TEXT from AES_Key_Store

drop table AES_Key_Store;

CREATE TABLE AES_Key_Store (
    id SERIAL PRIMARY KEY,
    table_name CHARACTER VARYING,
    aes_key BYTEA
);