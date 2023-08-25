PGDMP         	                {            sportbd    15.3    15.3      
           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            
           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            
           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            
           1262    32971    sportbd    DATABASE     {   CREATE DATABASE sportbd WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE sportbd;
                postgres    false            �            1259    32972 
   activities    TABLE     �   CREATE TABLE public.activities (
    id integer NOT NULL,
    gid character varying(255),
    activity_type character varying(255) NOT NULL,
    sp_id character varying(255),
    thread_id bigint NOT NULL,
    str_id integer
);
    DROP TABLE public.activities;
       public         heap    postgres    false            �            1259    32977    activities_id_seq    SEQUENCE     �   CREATE SEQUENCE public.activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.activities_id_seq;
       public          postgres    false    214            
           0    0    activities_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.activities_id_seq OWNED BY public.activities.id;
          public          postgres    false    215            �            1259    32978 	   tech_info    TABLE     ]   CREATE TABLE public.tech_info (
    str_id integer,
    date date,
    id bigint NOT NULL
);
    DROP TABLE public.tech_info;
       public         heap    postgres    false            �            1259    32981    user_activities    TABLE     �   CREATE TABLE public.user_activities (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    activity character varying(255) NOT NULL,
    gs_id character varying(255)
);
 #   DROP TABLE public.user_activities;
       public         heap    postgres    false            �            1259    32986    user_activities_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.user_activities_id_seq;
       public          postgres    false    217             
           0    0    user_activities_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.user_activities_id_seq OWNED BY public.user_activities.id;
          public          postgres    false    218            �            1259    32987    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    tg_id bigint NOT NULL,
    name text,
    timezone text,
    nickname text,
    tg_url text,
    date_start date
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    32992    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    219            !
           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    220            s           2604    32993 
   activities id    DEFAULT     n   ALTER TABLE ONLY public.activities ALTER COLUMN id SET DEFAULT nextval('public.activities_id_seq'::regclass);
 <   ALTER TABLE public.activities ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214            t           2604    32994    user_activities id    DEFAULT     x   ALTER TABLE ONLY public.user_activities ALTER COLUMN id SET DEFAULT nextval('public.user_activities_id_seq'::regclass);
 A   ALTER TABLE public.user_activities ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217            u           2604    32995    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    219            
          0    32972 
   activities 
   TABLE DATA                 public          postgres    false    214   E"       
          0    32978 	   tech_info 
   TABLE DATA                 public          postgres    false    216   U#       
          0    32981    user_activities 
   TABLE DATA                 public          postgres    false    217   �#       
          0    32987    users 
   TABLE DATA                 public          postgres    false    219   r$       "
           0    0    activities_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.activities_id_seq', 18, true);
          public          postgres    false    215            #
           0    0    user_activities_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.user_activities_id_seq', 4, true);
          public          postgres    false    218            $
           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 5, true);
          public          postgres    false    220            w           2606    32997 '   activities activities_activity_type_key 
   CONSTRAINT     k   ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_activity_type_key UNIQUE (activity_type);
 Q   ALTER TABLE ONLY public.activities DROP CONSTRAINT activities_activity_type_key;
       public            postgres    false    214            y           2606    32999    activities activities_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.activities DROP CONSTRAINT activities_pkey;
       public            postgres    false    214            {           2606    33001    tech_info tech_info_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.tech_info
    ADD CONSTRAINT tech_info_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.tech_info DROP CONSTRAINT tech_info_pkey;
       public            postgres    false    216                       2606    33003    users tg_id_constraint 
   CONSTRAINT     R   ALTER TABLE ONLY public.users
    ADD CONSTRAINT tg_id_constraint UNIQUE (tg_id);
 @   ALTER TABLE ONLY public.users DROP CONSTRAINT tg_id_constraint;
       public            postgres    false    219            }           2606    33005 $   user_activities user_activities_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.user_activities
    ADD CONSTRAINT user_activities_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.user_activities DROP CONSTRAINT user_activities_pkey;
       public            postgres    false    217            �           2606    33007    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    219            �           2606    33008 -   user_activities user_activities_activity_fkey 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.user_activities
    ADD CONSTRAINT user_activities_activity_fkey FOREIGN KEY (activity) REFERENCES public.activities(activity_type);
 W   ALTER TABLE ONLY public.user_activities DROP CONSTRAINT user_activities_activity_fkey;
       public          postgres    false    214    3191    217            �           2606    33013 ,   user_activities user_activities_user_id_fkey 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.user_activities
    ADD CONSTRAINT user_activities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(tg_id);
 V   ALTER TABLE ONLY public.user_activities DROP CONSTRAINT user_activities_user_id_fkey;
       public          postgres    false    217    219    3199            
      x���v
Q���W((M��L�KL.�,�,�L-V��L�QHP����ʂT��x�hIFQjb
�Y\R�5�}B]�4�u�-��M-L�MՁ��.6]�vaǅ=6\�{a��~����c��q��wq���n��IV@P�c���g�i�g��e�_v��kA�Aa6P���������5�'�\nt����/컰�b������ބ����ҨL�r�ʜ4�0��H3��ʒǲ\3������<sG��M���� ��g      
   W   x���v
Q���W((M��L�+IMΈ��K�W�(.)��L�QHI,I�Q�L�Ts�	u
Vа�QP7202�5��52Q�Q0Դ��� ڣ�      
   �   x���v
Q���W((M��L�+-N-�OL.�,�,�L-V��L�Q �P�J��b���B��O�k�������������������y�.l���.콰�b�:P�Y]Ӛ˓jv�(�Y����Ӊ�v���s��}�\l��a3��M4��)�o���3 u�      
   �   x���v
Q���W((M��L�+-N-*V��L�Q(I�Qy���@NfnjU~�����
K�/-��QHI,I�/.I,*�Ts�	u
V�0�Q01�047041�QP��I�JT2�MA�{f:�����u
@H]Ӛ˓v�2�Q050���41 :P�{/l��pa녝 w��vaP`ǅ� vFIIA���~�^n�~Qb�aJfI%���F� sq #g�     