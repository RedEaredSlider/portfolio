--temporary staging table
DROP TABLE IF EXISTS tmp_stage;
CREATE TEMP TABLE tmp_stage AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY company) AS record_id,
       *
    FROM my_schema.sample X
);

-- Drop the raw source table with record ID if it exists
DROP TABLE IF EXISTS my_schema.staging_contacts;
CREATE TABLE my_schema.staging_contacts AS (
    SELECT DISTINCT 
        record_id,
        company,
        business_name,
        business_id
    FROM (
        SELECT *
        FROM (
            SELECT 
                X.*,
                CASE 
                    WHEN REGEXP_REPLACE(company, '[^0-9a-zA-Z]', '') = REGEXP_REPLACE(business_name, '[^0-9a-zA-Z]', '') THEN 'Y'
                    WHEN (vendor_name_in_business_name + business_name_in_vendor_name) = 1 THEN 'Y'
                    WHEN UPPER(company) SIMILAR TO '%(INC|LLC|LTD|CORP)%' AND UPPER(business_name) NOT SIMILAR TO '%(INC|LLC|LTD|CORP)%' THEN 'N'
                    WHEN UPPER(company) NOT SIMILAR TO '%(INC|LLC|LTD|CORP)%' AND UPPER(business_name) SIMILAR TO '%(INC|LLC|LTD|CORP)%' THEN 'N'
                    WHEN (edit_distance <= 5 AND percent_match >= 0.75) THEN 'Y'
                    ELSE 'N'
                END AS Match_flg,
                ROW_NUMBER() OVER (PARTITION BY record_id ORDER BY edit_distance ASC, percent_match ASC) AS rn
            FROM (
                SELECT DISTINCT 
                    A.record_id,
                    A.company,
                    LOWER(REGEXP_REPLACE(company, '[^0-9a-zA-Z]', '')) AS vendor_name,
                    B.business_id,
                    B.business_name,
                    LOWER(REGEXP_REPLACE(business_name, '[^0-9a-zA-Z]', '')) AS business_name_cleaned,
                    POSITION(business_name_cleaned IN vendor_name) AS vendor_name_in_business_name,
                    POSITION(vendor_name IN business_name_cleaned) AS business_name_in_vendor_name,
                    LENGTH(REGEXP_REPLACE(company, '[^0-9a-zA-Z]', '')) AS vendor_name_length,
                    LENGTH(REGEXP_REPLACE(business_name, '[^0-9a-zA-Z]', '')) AS business_name_length,
                    udf_edit_distance(vendor_name, business_name_cleaned) AS edit_distance, '''udf_edit_distance function varies on the language being used'''
                    CASE 
                        WHEN vendor_name_length = 0 THEN NULL
                        ELSE (CAST(vendor_name_length AS DECIMAL) - CAST(edit_distance AS DECIMAL)) 
                             / CAST(vendor_name_length AS DECIMAL)
                    END AS percent_match
                FROM tmp_stage A
                LEFT JOIN my_schema.business_detail B
                ON POSITION(REGEXP_REPLACE(A.company, '[^0-9a-z]', '') IN REGEXP_REPLACE(B.business_name, '[^0-9a-z]', '')) > 0 
                   AND POSITION(REGEXP_REPLACE(A.address_text, '[^0-9a-z]', '') IN REGEXP_REPLACE(B.address, '[^0-9a-z]', '')) > 0 
                   AND A.city_name = B.city
                   AND A.state_code = B.state
                   AND A.zip_code = B.zip
            ) x
            WHERE good_business_match = 'Y'
        ) z
    ) staging
);
