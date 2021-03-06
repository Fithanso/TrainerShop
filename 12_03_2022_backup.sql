PGDMP         -                z            newDB    13.2    13.2 $    ?           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            ?           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            ?           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            ?           1262    25939    newDB    DATABASE     d   CREATE DATABASE "newDB" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "newDB";
                postgres    false                        2615    26242    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                postgres    false            ?            1259    26243    admin    TABLE       CREATE TABLE public.admin (
    id bigint NOT NULL,
    login text,
    password text,
    name character varying(30),
    surname character varying(30),
    last_visit timestamp without time zone,
    clearance_level smallint,
    email character varying(30)
);
    DROP TABLE public.admin;
       public         heap    postgres    false    3            ?            1259    26249    category    TABLE     ?   CREATE TABLE public.category (
    id integer NOT NULL,
    name character varying(40),
    short_name character varying(40)
);
    DROP TABLE public.category;
       public         heap    postgres    false    3            ?            1259    26252    characteristic    TABLE     ?   CREATE TABLE public.characteristic (
    id bigint NOT NULL,
    name character varying(40),
    category_id integer,
    type character varying(20)
);
 "   DROP TABLE public.characteristic;
       public         heap    postgres    false    3            ?            1259    26261    courier    TABLE     ?   CREATE TABLE public.courier (
    id smallint NOT NULL,
    name character varying(30),
    surname character varying(30),
    patronymic character varying(30)
);
    DROP TABLE public.courier;
       public         heap    postgres    false    3            ?            1259    26264    customer    TABLE     ?  CREATE TABLE public.customer (
    id bigint NOT NULL,
    login character varying(30),
    password character varying(40) NOT NULL,
    name character varying(30),
    surname character varying(30),
    patronymic character varying(30),
    delivery_address character varying(100),
    last_visit timestamp without time zone,
    register_date timestamp without time zone,
    active_cart text,
    orders text,
    birthday date,
    email character varying(30) NOT NULL,
    phone_number text
);
    DROP TABLE public.customer;
       public         heap    postgres    false    3            ?            1259    26270    global_setting    TABLE     ?   CREATE TABLE public.global_setting (
    id integer NOT NULL,
    name character varying(30),
    value character varying(30)
);
 "   DROP TABLE public.global_setting;
       public         heap    postgres    false    3            ?           0    0    TABLE global_setting    COMMENT     S   COMMENT ON TABLE public.global_setting IS 'A table to store settings of the shop';
          public          postgres    false    205            ?            1259    26273    order    TABLE     ?  CREATE TABLE public."order" (
    id bigint NOT NULL,
    customer_id bigint NOT NULL,
    purchased_products json,
    order_datetime timestamp without time zone,
    received boolean,
    shipment_method smallint,
    boxes_content json,
    courier_id smallint,
    customer_registered boolean,
    recipient_name text,
    recipient_surname text,
    recipient_patronymic text,
    recipient_phone_number text,
    recipient_email text,
    total_price numeric,
    delivery_address text
);
    DROP TABLE public."order";
       public         heap    postgres    false    3            ?            1259    26279    product    TABLE     ?  CREATE TABLE public.product (
    id bigint NOT NULL,
    name character varying(30),
    description text,
    price numeric,
    pieces_left integer,
    category character varying(30),
    characteristics text,
    box_dimensions character varying(20),
    box_weight smallint,
    img_names text,
    creation_date timestamp without time zone,
    last_edited timestamp without time zone
);
    DROP TABLE public.product;
       public         heap    postgres    false    3            ?           0    0    COLUMN product.creation_date    COMMENT     h   COMMENT ON COLUMN public.product.creation_date IS 'stores date and time of when a product was created';
          public          postgres    false    207            ?            1259    26288    shipment_method    TABLE     ?   CREATE TABLE public.shipment_method (
    id smallint NOT NULL,
    cost integer,
    estimated_time smallint,
    name character varying(30)
);
 #   DROP TABLE public.shipment_method;
       public         heap    postgres    false    3            ?          0    26243    admin 
   TABLE DATA           g   COPY public.admin (id, login, password, name, surname, last_visit, clearance_level, email) FROM stdin;
    public          postgres    false    200   ?+       ?          0    26249    category 
   TABLE DATA           8   COPY public.category (id, name, short_name) FROM stdin;
    public          postgres    false    201   ,       ?          0    26252    characteristic 
   TABLE DATA           E   COPY public.characteristic (id, name, category_id, type) FROM stdin;
    public          postgres    false    202   4,       ?          0    26261    courier 
   TABLE DATA           @   COPY public.courier (id, name, surname, patronymic) FROM stdin;
    public          postgres    false    203   Q,       ?          0    26264    customer 
   TABLE DATA           ?   COPY public.customer (id, login, password, name, surname, patronymic, delivery_address, last_visit, register_date, active_cart, orders, birthday, email, phone_number) FROM stdin;
    public          postgres    false    204   ?,       ?          0    26270    global_setting 
   TABLE DATA           9   COPY public.global_setting (id, name, value) FROM stdin;
    public          postgres    false    205   ?,       ?          0    26273    order 
   TABLE DATA           "  COPY public."order" (id, customer_id, purchased_products, order_datetime, received, shipment_method, boxes_content, courier_id, customer_registered, recipient_name, recipient_surname, recipient_patronymic, recipient_phone_number, recipient_email, total_price, delivery_address) FROM stdin;
    public          postgres    false    206   g-       ?          0    26279    product 
   TABLE DATA           ?   COPY public.product (id, name, description, price, pieces_left, category, characteristics, box_dimensions, box_weight, img_names, creation_date, last_edited) FROM stdin;
    public          postgres    false    207   ?-       ?          0    26288    shipment_method 
   TABLE DATA           I   COPY public.shipment_method (id, cost, estimated_time, name) FROM stdin;
    public          postgres    false    208   ?-       E           2606    26292    admin admin_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.admin DROP CONSTRAINT admin_pkey;
       public            postgres    false    200            G           2606    26294    category category_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.category DROP CONSTRAINT category_pkey;
       public            postgres    false    201            I           2606    26296 "   characteristic characteristic_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.characteristic
    ADD CONSTRAINT characteristic_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.characteristic DROP CONSTRAINT characteristic_pkey;
       public            postgres    false    202            K           2606    26300    courier courier_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.courier
    ADD CONSTRAINT courier_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.courier DROP CONSTRAINT courier_pkey;
       public            postgres    false    203            O           2606    26302 "   global_setting global_setting_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.global_setting
    ADD CONSTRAINT global_setting_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.global_setting DROP CONSTRAINT global_setting_pkey;
       public            postgres    false    205            M           2606    26304    customer id 
   CONSTRAINT     I   ALTER TABLE ONLY public.customer
    ADD CONSTRAINT id PRIMARY KEY (id);
 5   ALTER TABLE ONLY public.customer DROP CONSTRAINT id;
       public            postgres    false    204            Q           2606    26306    order order_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public."order" DROP CONSTRAINT order_pkey;
       public            postgres    false    206            S           2606    26308    product product_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.product DROP CONSTRAINT product_pkey;
       public            postgres    false    207            U           2606    26312    shipment_method shipment_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.shipment_method
    ADD CONSTRAINT shipment_pkey PRIMARY KEY (id);
 G   ALTER TABLE ONLY public.shipment_method DROP CONSTRAINT shipment_pkey;
       public            postgres    false    208            V           2606    26313    order courier_id    FK CONSTRAINT     ?   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT courier_id FOREIGN KEY (courier_id) REFERENCES public.courier(id) NOT VALID;
 <   ALTER TABLE ONLY public."order" DROP CONSTRAINT courier_id;
       public          postgres    false    203    206    2891            W           2606    26318    order customer_id    FK CONSTRAINT     y   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT customer_id FOREIGN KEY (customer_id) REFERENCES public.customer(id);
 =   ALTER TABLE ONLY public."order" DROP CONSTRAINT customer_id;
       public          postgres    false    2893    206    204            ?   m   x??;?0 ??9h?O\?N?vee1????Tb@????\s-2?8??????À???<???)f??3,?ھp+??߫??LjG|"? ???vy???^ý!? w(?      ?      x?????? ? ?      ?      x?????? ? ?      ?   .   x?3?*-.I???-??H??ML?t,?I?KJ??/?L??????? ??I      ?      x?????? ? ?      ?   ?   x?]?A
?0Eדst]?8I???a?A??QZo_????}?????Z????4pZ
?u???Q?ځ?Z??b???????!Z?]?}???V????15W֜??1?x????ךK:???a?N?1?Z?G???)c??ZǇ???{*9e??O?R?'O??뮔?^Ge      ?      x?????? ? ?      ?      x?????? ? ?      ?   C   x?3263??440 b???????̔T.NSN#Nϼb O!9???ː??.?_?WRT????? ]?     