CREATE OR REPLACE FUNCTION "Create tables"()
    RETURNS void
    LANGUAGE 'sql'
    
    
AS $BODY$CREATE TABLE IF NOT EXISTS "Assortment"
(
    name character varying,
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    stock integer,
    price money,
    PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS name ON "Assortment" (name);
    
CREATE TABLE IF NOT EXISTS "Orders"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    item integer,
    quantity integer,
    creation_time timestamptz DEFAULT CURRENT_TIMESTAMP,
    last_modification_time timestamptz,
    PRIMARY KEY (id)
);$BODY$;

SELECT "Create tables"();

CREATE OR REPLACE FUNCTION set_mod_time()
RETURNS TRIGGER AS $$
BEGIN
   NEW.last_modification_time = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ language 'plpgsql';


DROP TRIGGER IF EXISTS update_Orders_settotal on "Orders";

CREATE TRIGGER update_Orders_settotal BEFORE UPDATE
    ON "Orders" FOR EACH ROW EXECUTE PROCEDURE 
    set_mod_time();


CREATE OR REPLACE FUNCTION add_item (IN name character varying, IN stock integer, IN price money)
    RETURNS void
    LANGUAGE 'sql'
    
    
AS $BODY$INSERT INTO "Assortment"(
	name, stock, price)
	VALUES (name, stock, price);$BODY$;
	
CREATE OR REPLACE FUNCTION add_order (IN item int, IN quantity int)
    RETURNS void
    LANGUAGE 'sql'
    
    
AS $BODY$INSERT INTO "Orders"(
	item, quantity)
	VALUES (item, quantity);$BODY$;
	
	
CREATE OR REPLACE FUNCTION get_assortment()
RETURNS JSON AS
$$
BEGIN
  RETURN (SELECT json_agg(json_build_object(
  'id', "Assortment".id,
  'name',"Assortment".name,
  'stock',"Assortment".stock,
  'price',"Assortment".price
  )) FROM "Assortment");
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_orders()
RETURNS JSON AS
$$
BEGIN
  RETURN (SELECT json_agg(json_build_object(
  'id', "Orders".id,
  'item', "Orders".item,
  'quantity', "Orders".quantity,
  'creation_time', "Orders".creation_time,
  'last_modification_time', coalesce("Orders".last_modification_time, "Orders".creation_time)
  )) FROM "Orders");
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION clear_assortment()
RETURNS void AS
$$
BEGIN
  TRUNCATE "Assortment";
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION clear_orders()
RETURNS void AS
$$
BEGIN
  TRUNCATE "Orders";
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION clear_all()
RETURNS void AS
$$
BEGIN
  TRUNCATE "Orders";
  TRUNCATE "Assortment";
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search(search_query character varying)
RETURNS JSON AS
$$
BEGIN
  RETURN (SELECT json_agg(json_build_object(
  'id', "Assortment".id,
  'name',"Assortment".name,
  'stock',"Assortment".stock,
  'price',"Assortment".price
  )) FROM "Assortment" WHERE "Assortment".name LIKE CONCAT('%', search_query, '%'));
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_by_name(target character varying)
RETURNS void AS
$$
BEGIN
	DELETE FROM "Orders" WHERE "Orders"."item" IN 
	(SELECT "Assortment".id FROM "Assortment" WHERE "Assortment".name=target);
	DELETE FROM "Assortment" WHERE "Assortment".name = target;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_order(target int)
RETURNS void AS
$$
BEGIN
	DELETE FROM "Orders" WHERE "Orders"."id" = target;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_item(target int)
RETURNS void AS
$$
BEGIN
	DELETE FROM "Orders" WHERE "Orders"."item" = target;
	DELETE FROM "Assortment" WHERE "Assortment"."id" = target;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_item_name(target int, newname character varying)
RETURNS void AS
$$
BEGIN
	UPDATE "Assortment" SET "name" = newname WHERE "Assortment"."id" = target;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_item_stock(target int, newstock int)
RETURNS void AS
$$
BEGIN
	UPDATE "Assortment" SET "stock" = newstock WHERE "Assortment"."id" = target;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_item_price(target int, newprice money)
RETURNS void AS
$$
BEGIN
	UPDATE "Assortment" SET "price" = newprice WHERE "Assortment"."id" = target;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_order_item(target int, newitem int)
RETURNS void AS
$$
BEGIN
	UPDATE "Orders" SET "item" = newitem WHERE "Orders"."id" = target;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_order_quantity(target int, newquantity int)
RETURNS void AS
$$
BEGIN
	UPDATE "Orders" SET "quantity" = newquantity WHERE "Orders"."id" = target;
END
$$ LANGUAGE plpgsql;

