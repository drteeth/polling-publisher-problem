create table if not exists outbox (
  sequence INT GENERATED ALWAYS AS IDENTITY,
  event_id varchar(64) primary key,
  event_type varchar(64) not null,
  event_data jsonb not null,
  metadata jsonb not null default '{}',
  inserted_at timestamp without time zone not null
);

create table if not exists products (
  product_id varchar(64) primary key,
  name varchar(64) not null
);

create table if not exists licenses (
  license_id varchar(64) primary key,
  name varchar(64) not null
);

create table if not exists active_product_licenses (
  customer_id varchar(64) not null,
  product_id varchar(64) not null,
  license_id varchar(64) not null
);
