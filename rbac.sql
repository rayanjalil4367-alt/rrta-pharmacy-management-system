USE PharmacyManagementSystem;

DROP USER IF EXISTS 'rayan_admin'@'localhost';
DROP USER IF EXISTS 'taha_pharm'@'localhost';
DROP USER IF EXISTS 'ali_pharm'@'localhost';
DROP USER IF EXISTS 'rafay_analyst'@'localhost';

CREATE USER 'rayan_admin'@'localhost' IDENTIFIED BY 'rayan123';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON PharmacyManagementSystem.Customer        TO 'rayan_admin'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON PharmacyManagementSystem.Pharmacist      TO 'rayan_admin'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON PharmacyManagementSystem.Category        TO 'rayan_admin'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON PharmacyManagementSystem.Medicine        TO 'rayan_admin'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON PharmacyManagementSystem.Supplier        TO 'rayan_admin'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON PharmacyManagementSystem.Inventory       TO 'rayan_admin'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON PharmacyManagementSystem.Product_Sales   TO 'rayan_admin'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON PharmacyManagementSystem.Sale_Items      TO 'rayan_admin'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON PharmacyManagementSystem.Payment         TO 'rayan_admin'@'localhost';

CREATE USER 'taha_pharm'@'localhost' IDENTIFIED BY 'taha456';
CREATE USER 'ali_pharm'@'localhost'  IDENTIFIED BY 'ali789';

GRANT SELECT, INSERT, UPDATE
    ON PharmacyManagementSystem.Customer        TO 'taha_pharm'@'localhost';
GRANT SELECT, INSERT, UPDATE
    ON PharmacyManagementSystem.Customer        TO 'ali_pharm'@'localhost';

GRANT SELECT, INSERT
    ON PharmacyManagementSystem.Product_Sales   TO 'taha_pharm'@'localhost';
GRANT SELECT, INSERT
    ON PharmacyManagementSystem.Product_Sales   TO 'ali_pharm'@'localhost';

GRANT SELECT, INSERT
    ON PharmacyManagementSystem.Sale_Items      TO 'taha_pharm'@'localhost';
GRANT SELECT, INSERT
    ON PharmacyManagementSystem.Sale_Items      TO 'ali_pharm'@'localhost';

GRANT SELECT, INSERT
    ON PharmacyManagementSystem.Payment         TO 'taha_pharm'@'localhost';
GRANT SELECT, INSERT
    ON PharmacyManagementSystem.Payment         TO 'ali_pharm'@'localhost';


GRANT SELECT
    ON PharmacyManagementSystem.Medicine        TO 'taha_pharm'@'localhost';
GRANT SELECT
    ON PharmacyManagementSystem.Medicine        TO 'ali_pharm'@'localhost';

GRANT SELECT
    ON PharmacyManagementSystem.Inventory       TO 'taha_pharm'@'localhost';
GRANT SELECT
    ON PharmacyManagementSystem.Inventory       TO 'ali_pharm'@'localhost';

GRANT SELECT
    ON PharmacyManagementSystem.Category        TO 'taha_pharm'@'localhost';
GRANT SELECT
    ON PharmacyManagementSystem.Category        TO 'ali_pharm'@'localhost';


CREATE USER 'rafay_analyst'@'localhost' IDENTIFIED BY 'rafay321';

GRANT SELECT
    ON PharmacyManagementSystem.Customer        TO 'rafay_analyst'@'localhost';

GRANT SELECT
    ON PharmacyManagementSystem.Medicine        TO 'rafay_analyst'@'localhost';

GRANT SELECT
    ON PharmacyManagementSystem.Inventory       TO 'rafay_analyst'@'localhost';

GRANT SELECT
    ON PharmacyManagementSystem.Product_Sales   TO 'rafay_analyst'@'localhost';

GRANT SELECT
    ON PharmacyManagementSystem.Payment         TO 'rafay_analyst'@'localhost';

GRANT SELECT
    ON PharmacyManagementSystem.Category        TO 'rafay_analyst'@'localhost';

GRANT INSERT ON PharmacyManagementSystem.Payment TO 'ali_pharm'@'localhost';
REVOKE INSERT ON PharmacyManagementSystem.Payment FROM 'ali_pharm'@'localhost';
FLUSH PRIVILEGES;

SHOW GRANTS FOR 'rayan_admin'@'localhost';
SHOW GRANTS FOR 'taha_pharm'@'localhost';
SHOW GRANTS FOR 'ali_pharm'@'localhost';
SHOW GRANTS FOR 'rafay_analyst'@'localhost';
