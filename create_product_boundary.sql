-- Table: public.product_boundary

-- DROP TABLE public.product_boundary;

CREATE TABLE public.product_boundary
(
    id integer NOT NULL DEFAULT nextval('product_boundary_id_seq'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    boundary geometry NOT NULL,
    CONSTRAINT product_boundary_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.product_boundary
    OWNER to postgres;