CREATE TABLE public.z1frame (
    id bigint NOT NULL,
    frame bytea,
    milliseconds numeric,
    timestr character(40),
    bbox text
);
CREATE TABLE public.zdash (
    id bigint NOT NULL,
    milliseconds bigint,
    timestr character(40),
    photo text,
    name text,
    capture text,
    name_id bigint
);
CREATE TABLE public.zdata (
    id bigint NOT NULL,
    zjson text,
    milliseconds bigint,
    timestr character(40)
);
CREATE TABLE public.zemb (
    id bigint NOT NULL,
    emb text,
    filename text,
    name text,
    "desc" text,
    sound text
);
