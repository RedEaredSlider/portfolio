CREATE OR REPLACE PROCEDURE my_schema.bulk_load_data_drop(source_schema VARCHAR, source_table VARCHAR, target_schema VARCHAR, target_table VARCHAR)
AS $$
BEGIN
    -- Drop the target table if it exists
    EXECUTE 'DROP TABLE IF EXISTS ' || target_schema || '.' || target_table;

    -- Create the target table based on the structure of the source table
    EXECUTE 'CREATE TABLE ' || target_schema || '.' || target_table || ' (LIKE ' || source_schema || '.' || source_table || ')';

    -- Insert data from source table to target table
    EXECUTE 'INSERT INTO ' || target_schema || '.' || target_table || ' SELECT * FROM ' || source_schema || '.' || source_table;
END;
$$ LANGUAGE plpgsql;
