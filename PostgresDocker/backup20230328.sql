PGDMP                         {         	   personadb    14.4 (Debian 14.4-1.pgdg110+1)    14.4                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16384 	   personadb    DATABASE     ]   CREATE DATABASE personadb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';
    DROP DATABASE personadb;
                personauser    false            �            1259    16385    z1frame    TABLE     �   CREATE TABLE public.z1frame (
    id bigint NOT NULL,
    frame bytea,
    milliseconds numeric,
    timestr character(40),
    bbox text
);
    DROP TABLE public.z1frame;
       public         heap    personauser    false            �            1259    16390    z1frame_id_seq    SEQUENCE     w   CREATE SEQUENCE public.z1frame_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.z1frame_id_seq;
       public          personauser    false    209                       0    0    z1frame_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.z1frame_id_seq OWNED BY public.z1frame.id;
          public          personauser    false    210            �            1259    16391    zdash    TABLE     �   CREATE TABLE public.zdash (
    id bigint NOT NULL,
    milliseconds bigint,
    timestr character(40),
    photo text,
    name text,
    capture text,
    name_id bigint
);
    DROP TABLE public.zdash;
       public         heap    personauser    false            �            1259    16396    zdash_id_seq    SEQUENCE     �   ALTER TABLE public.zdash ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.zdash_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          personauser    false    211            �            1259    16397    zdata    TABLE     z   CREATE TABLE public.zdata (
    id bigint NOT NULL,
    zjson text,
    milliseconds bigint,
    timestr character(40)
);
    DROP TABLE public.zdata;
       public         heap    personauser    false            �            1259    16402    zdata_id_seq    SEQUENCE     �   ALTER TABLE public.zdata ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.zdata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          personauser    false    213            �            1259    32769    zemb    TABLE     �   CREATE TABLE public.zemb (
    id bigint NOT NULL,
    emb text,
    filename text,
    name text,
    "desc" text,
    sound text
);
    DROP TABLE public.zemb;
       public         heap    personauser    false            �            1259    40961    zemb_id_seq    SEQUENCE     �   ALTER TABLE public.zemb ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.zemb_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
    CYCLE
);
            public          personauser    false    215            n           2604    16412 
   z1frame id    DEFAULT     h   ALTER TABLE ONLY public.z1frame ALTER COLUMN id SET DEFAULT nextval('public.z1frame_id_seq'::regclass);
 9   ALTER TABLE public.z1frame ALTER COLUMN id DROP DEFAULT;
       public          personauser    false    210    209                      0    16385    z1frame 
   TABLE DATA           I   COPY public.z1frame (id, frame, milliseconds, timestr, bbox) FROM stdin;
    public          personauser    false    209   b                 0    16391    zdash 
   TABLE DATA           Y   COPY public.zdash (id, milliseconds, timestr, photo, name, capture, name_id) FROM stdin;
    public          personauser    false    211                    0    16397    zdata 
   TABLE DATA           A   COPY public.zdata (id, zjson, milliseconds, timestr) FROM stdin;
    public          personauser    false    213   �       
          0    32769    zemb 
   TABLE DATA           F   COPY public.zemb (id, emb, filename, name, "desc", sound) FROM stdin;
    public          personauser    false    215   �                  0    0    z1frame_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.z1frame_id_seq', 544857, true);
          public          personauser    false    210                       0    0    zdash_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.zdash_id_seq', 9841, true);
          public          personauser    false    212                       0    0    zdata_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.zdata_id_seq', 30680, true);
          public          personauser    false    214                       0    0    zemb_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.zemb_id_seq', 251, true);
          public          personauser    false    216            q           2606    16405    z1frame z1frame_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.z1frame
    ADD CONSTRAINT z1frame_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.z1frame DROP CONSTRAINT z1frame_pkey;
       public            personauser    false    209            s           2606    16407    zdash zdash_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.zdash
    ADD CONSTRAINT zdash_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.zdash DROP CONSTRAINT zdash_pkey;
       public            personauser    false    211            u           2606    16409    zdata zdata_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.zdata
    ADD CONSTRAINT zdata_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.zdata DROP CONSTRAINT zdata_pkey;
       public            personauser    false    213            x           2606    32775    zemb zemb_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.zemb
    ADD CONSTRAINT zemb_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.zemb DROP CONSTRAINT zemb_pkey;
       public            personauser    false    215            o           1259    16410    milisec    INDEX     J   CREATE UNIQUE INDEX milisec ON public.z1frame USING btree (milliseconds);
    DROP INDEX public.milisec;
       public            personauser    false    209            v           1259    16411    zmilisec    INDEX     R   CREATE INDEX zmilisec ON public.zdata USING btree (milliseconds DESC NULLS LAST);
    DROP INDEX public.zmilisec;
       public            personauser    false    213                  x������ � �            x������ � �            x������ � �      
      x������ � �     