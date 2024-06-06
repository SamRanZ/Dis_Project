-- Revoke all privileges on all tables in the public schema from testuser
DO $$
BEGIN
    IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'testuser') THEN
        REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM testuser;
        REVOKE ALL PRIVILEGES ON SCHEMA public FROM testuser;
        REVOKE ALL PRIVILEGES ON DATABASE "DISProject" FROM testuser;
        DROP ROLE testuser;
    END IF;
END $$;

-- Create the user
CREATE ROLE testuser WITH LOGIN PASSWORD '123';

-- Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON DATABASE "DISProject" TO testuser;

-- Grant all necessary privileges on the public schema to testuser
GRANT USAGE ON SCHEMA public TO testuser;

-- Start transaction
BEGIN;

-- Drop the existing table if it exists
DROP TABLE IF EXISTS public."School";

-- Create the School table with the correct column names
CREATE TABLE public."School"
(
    "DBN" VARCHAR(20) PRIMARY KEY,
    "School Name" VARCHAR(255),
    "Number of Test Takers" INTEGER,
    "Critical Reading Mean" INTEGER,
    "Mathematics Mean" INTEGER,
    "Writing Mean" INTEGER
);

-- Commit transaction
END;

-- Grant all necessary privileges on the School table to testuser
GRANT SELECT, INSERT, UPDATE, DELETE ON public."School" TO testuser;

-- Load data from the CSV file into the School table
COPY public."School" ("DBN", "School Name", "Number of Test Takers", "Critical Reading Mean", "Mathematics Mean", "Writing Mean")
FROM '/Users/s/Desktop/Dis/Dis_Project/schools.csv' DELIMITER ',' CSV HEADER;

-- Check privileges for testuser on the School table
SELECT grantee, privilege_type 
FROM information_schema.role_table_grants 
WHERE table_name='School';
