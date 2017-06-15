PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE employees
                    (ID INT PRIMARY KEY ASC,
                    FULL_NAME TEXT,
                    EMPLOYEE_TYPE TEXT,
                    OFFICE TEXT,
                    LIVINGSPACE TEXT);
INSERT INTO "employees" VALUES(1,'OLUWAFEMI SULE','fellow','Dakar','Unallocated');
INSERT INTO "employees" VALUES(2,'DOMINIC WALTERS','staff','Dakar',NULL);
INSERT INTO "employees" VALUES(3,'SIMON PATTERSON','fellow','Dakar','Unallocated');
INSERT INTO "employees" VALUES(4,'MARI LAWRENCE','fellow','Dakar','Unallocated');
INSERT INTO "employees" VALUES(5,'LEIGH RILEY','staff','Dakar',NULL);
INSERT INTO "employees" VALUES(6,'TANA LOPEZ','fellow','Dakar','Unallocated');
INSERT INTO "employees" VALUES(7,'KELLY McGUIRE','staff','Unallocated',NULL);
CREATE TABLE rooms
                    (ID INT PRIMARY KEY NOT NULL,
                    ROOM_NAME TEXT,
                    ROOM_TYPE TEXT,
                    ROOM_OCCUPANTS TEXT);
INSERT INTO "rooms" VALUES(1,'Dakar','officeSpace',NULL);
COMMIT;
