--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4 (Debian 14.4-1.pgdg110+1)
-- Dumped by pg_dump version 16.4

-- Started on 2025-02-04 01:11:13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'WIN1251';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: personauser
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO personauser;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 209 (class 1259 OID 24577)
-- Name: z1frame; Type: TABLE; Schema: public; Owner: personauser
--

CREATE TABLE public.z1frame (
    id bigint NOT NULL,
    frame bytea,
    milliseconds numeric,
    timestr character(40),
    bbox text
);


ALTER TABLE public.z1frame OWNER TO personauser;

--
-- TOC entry 210 (class 1259 OID 24582)
-- Name: z1frame_id_seq; Type: SEQUENCE; Schema: public; Owner: personauser
--

CREATE SEQUENCE public.z1frame_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.z1frame_id_seq OWNER TO personauser;

--
-- TOC entry 3346 (class 0 OID 0)
-- Dependencies: 210
-- Name: z1frame_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: personauser
--

ALTER SEQUENCE public.z1frame_id_seq OWNED BY public.z1frame.id;


--
-- TOC entry 211 (class 1259 OID 24583)
-- Name: zdash; Type: TABLE; Schema: public; Owner: personauser
--

CREATE TABLE public.zdash (
    id bigint NOT NULL,
    milliseconds bigint,
    timestr character(40),
    photo text,
    name text,
    capture text,
    name_id bigint
);


ALTER TABLE public.zdash OWNER TO personauser;

--
-- TOC entry 212 (class 1259 OID 24588)
-- Name: zdash_id_seq; Type: SEQUENCE; Schema: public; Owner: personauser
--

ALTER TABLE public.zdash ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.zdash_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 213 (class 1259 OID 24589)
-- Name: zdata; Type: TABLE; Schema: public; Owner: personauser
--

CREATE TABLE public.zdata (
    id bigint NOT NULL,
    zjson text,
    milliseconds bigint,
    timestr character(40)
);


ALTER TABLE public.zdata OWNER TO personauser;

--
-- TOC entry 214 (class 1259 OID 24594)
-- Name: zdata_id_seq; Type: SEQUENCE; Schema: public; Owner: personauser
--

ALTER TABLE public.zdata ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.zdata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 215 (class 1259 OID 24595)
-- Name: zemb; Type: TABLE; Schema: public; Owner: personauser
--

CREATE TABLE public.zemb (
    id bigint NOT NULL,
    emb text,
    filename text,
    name text,
    "desc" text,
    sound text
);


ALTER TABLE public.zemb OWNER TO personauser;

--
-- TOC entry 216 (class 1259 OID 24600)
-- Name: zemb_id_seq; Type: SEQUENCE; Schema: public; Owner: personauser
--

ALTER TABLE public.zemb ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.zemb_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
    CYCLE
);


--
-- TOC entry 3182 (class 2604 OID 24601)
-- Name: z1frame id; Type: DEFAULT; Schema: public; Owner: personauser
--

ALTER TABLE ONLY public.z1frame ALTER COLUMN id SET DEFAULT nextval('public.z1frame_id_seq'::regclass);


--
-- TOC entry 3332 (class 0 OID 24577)
-- Dependencies: 209
-- Data for Name: z1frame; Type: TABLE DATA; Schema: public; Owner: personauser
--

COPY public.z1frame (id, frame, milliseconds, timestr, bbox) FROM stdin;
\.


--
-- TOC entry 3334 (class 0 OID 24583)
-- Dependencies: 211
-- Data for Name: zdash; Type: TABLE DATA; Schema: public; Owner: personauser
--

COPY public.zdash (id, milliseconds, timestr, photo, name, capture, name_id) FROM stdin;
\.


--
-- TOC entry 3336 (class 0 OID 24589)
-- Dependencies: 213
-- Data for Name: zdata; Type: TABLE DATA; Schema: public; Owner: personauser
--

COPY public.zdata (id, zjson, milliseconds, timestr) FROM stdin;
\.


--
-- TOC entry 3338 (class 0 OID 24595)
-- Dependencies: 215
-- Data for Name: zemb; Type: TABLE DATA; Schema: public; Owner: personauser
--

COPY public.zemb (id, emb, filename, name, "desc", sound) FROM stdin;
\.


--
-- TOC entry 3347 (class 0 OID 0)
-- Dependencies: 210
-- Name: z1frame_id_seq; Type: SEQUENCE SET; Schema: public; Owner: personauser
--

SELECT pg_catalog.setval('public.z1frame_id_seq', 544857, true);


--
-- TOC entry 3348 (class 0 OID 0)
-- Dependencies: 212
-- Name: zdash_id_seq; Type: SEQUENCE SET; Schema: public; Owner: personauser
--

SELECT pg_catalog.setval('public.zdash_id_seq', 9841, true);


--
-- TOC entry 3349 (class 0 OID 0)
-- Dependencies: 214
-- Name: zdata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: personauser
--

SELECT pg_catalog.setval('public.zdata_id_seq', 30680, true);


--
-- TOC entry 3350 (class 0 OID 0)
-- Dependencies: 216
-- Name: zemb_id_seq; Type: SEQUENCE SET; Schema: public; Owner: personauser
--

SELECT pg_catalog.setval('public.zemb_id_seq', 251, true);


--
-- TOC entry 3185 (class 2606 OID 24603)
-- Name: z1frame z1frame_pkey; Type: CONSTRAINT; Schema: public; Owner: personauser
--

ALTER TABLE ONLY public.z1frame
    ADD CONSTRAINT z1frame_pkey PRIMARY KEY (id);


--
-- TOC entry 3187 (class 2606 OID 24605)
-- Name: zdash zdash_pkey; Type: CONSTRAINT; Schema: public; Owner: personauser
--

ALTER TABLE ONLY public.zdash
    ADD CONSTRAINT zdash_pkey PRIMARY KEY (id);


--
-- TOC entry 3189 (class 2606 OID 24607)
-- Name: zdata zdata_pkey; Type: CONSTRAINT; Schema: public; Owner: personauser
--

ALTER TABLE ONLY public.zdata
    ADD CONSTRAINT zdata_pkey PRIMARY KEY (id);


--
-- TOC entry 3192 (class 2606 OID 24609)
-- Name: zemb zemb_pkey; Type: CONSTRAINT; Schema: public; Owner: personauser
--

ALTER TABLE ONLY public.zemb
    ADD CONSTRAINT zemb_pkey PRIMARY KEY (id);


--
-- TOC entry 3183 (class 1259 OID 24610)
-- Name: milisec; Type: INDEX; Schema: public; Owner: personauser
--

CREATE UNIQUE INDEX milisec ON public.z1frame USING btree (milliseconds);


--
-- TOC entry 3190 (class 1259 OID 24611)
-- Name: zmilisec; Type: INDEX; Schema: public; Owner: personauser
--

CREATE INDEX zmilisec ON public.zdata USING btree (milliseconds DESC NULLS LAST);


--
-- TOC entry 3345 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: personauser
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2025-02-04 01:11:13

--
-- PostgreSQL database dump complete
--

