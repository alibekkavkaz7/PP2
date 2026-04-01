
CREATE OR REPLACE PROCEDURE upsert_contact(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;



CREATE OR REPLACE PROCEDURE insert_many(names TEXT[], phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF length(phones[i]) >= 5 THEN
            INSERT INTO contacts(name, phone)
            VALUES(names[i], phones[i]);
        ELSE
            RAISE NOTICE 'Wrong phone: %', phones[i];
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p OR phone = p;
END;
$$;