
# EUResearchHub - Database and query implementations

- [Table Creation](#table)
- [Roles](#roles)
- [Trigger](#triggers)

<h2 id="table">Table Creation</h2>

In this document we have listed all the queries for the creation of the database and the implementation of indexes, triggers, cheks and functions.<br>
To mantain a more readable and compact code, all the queries are sorted according to the table in which they are inserted.<br>

- [Projects](#prj)
- [Evaluation Windows](#evnwin)
- [Messages](#msg)
- [Documents](#doc)
- [Document types](#doctype)
- [Document versions](#docver)
- [Evaluators](#evr)
- [Evaluators Messages](#evrmsg)
- [Evaluators Projects](#evrprj)
- [Evaluation Reports](#evnrep)
- [Evaluators Evaluation Reports](#evrevnrep)
- [Researchers](#res)
- [Researchers Projects](#resprj)
- [Researchers Messages](#resmsg)

---

<h3 id="prj" >Projects</h3>

````sql
CREATE TYPE enum_status AS ENUM ('approved', 'submitted for evaluation', 'require changes', 'not approved');

CREATE TABLE "EUResearchHub".projects (
	id int NULL,
	title varchar NULL,
	status enum_status NULL,
	description varchar NULL,
	last_update_date date NULL,
	fk_evaluation_window int NOT NULL,
	CONSTRAINT projects_pk PRIMARY KEY (id),
	CONSTRAINT projects_fk FOREIGN KEY (fk_evaluation_window) REFERENCES "EUResearchHub".evaluation_windows(id)
);

````
>Query for the creation of the Projects Table
---

````sql
ALTER TABLE "EUResearchHub".projects RENAME COLUMN last_update_date TO "date";
ALTER TABLE "EUResearchHub".projects ALTER COLUMN "date" TYPE timestamp USING "date"::timestamp;
````
>Update of the name and the type of last_update_date
---


<h3 id="evnwin" >Evaluation Windows</h3>

````sql
CREATE TABLE "EUResearchHub".evaluation_windows (
	id int NULL,
	"from" date NULL,
	"to" date NULL,
	CONSTRAINT evaluation_windows_pk PRIMARY KEY (id)
);
````
>Query for the creation of the Evaluation Windows Table
> 
---

<h3 id="msg" >Messages</h3>

````sql
CREATE TABLE "EUResearchHub".messages (
	id int NULL,
	"text" varchar NOT NULL,
	fk_projects int NOT NULL,
	CONSTRAINT messages_pk PRIMARY KEY (id),
	CONSTRAINT messages_fk FOREIGN KEY (fk_projects) REFERENCES "EUResearchHub".projects(id)
);
````

>Query for the creation of the Messages Table
---

````sql
ALTER TABLE "EUResearchHub".messages ADD "date" timestamp NULL;
````
> Add of the date attribute
---

<h3 id="doc" >Documents</h3>

````sql
CREATE TABLE "EUResearchHub".documents (
	id int NULL,
	file_path varchar NULL,
	fk_document_type int NOT NULL,
	fk_project int NOT NULL,
	CONSTRAINT documents_pk PRIMARY KEY (id),
	CONSTRAINT document_type_fk FOREIGN KEY (fk_document_type) REFERENCES "EUResearchHub".document_types(id),
	CONSTRAINT projects_fk FOREIGN KEY (fk_project) REFERENCES "EUResearchHub".projects(id)
);
````

>Query for the creation of the Documents Table

---

<h3 id="doctype" >Document Types</h3>

````sql
CREATE TABLE "EUResearchHub".document_types (
	id int NULL,
	nome varchar NULL,
	descrizione varchar NULL,
	CONSTRAINT document_types_pk PRIMARY KEY (id)
);
````
>Query for the creation of the Document Types Table
---

<h3 id="docver" >Document Versions</h3>

````sql
CREATE TABLE "EUResearchHub".document_versions (
	id int NULL,
	description varchar NULL,
	date_version date NULL,
	fk_document int NOT NULL,
	CONSTRAINT document_versions_pk PRIMARY KEY (id),
	CONSTRAINT document_versions_fk FOREIGN KEY (fk_document) REFERENCES "EUResearchHub".documents(id)
);
````
>Query for the creation of the Document Versions Table
---

````sql
ALTER TABLE "EUResearchHub".document_versions RENAME COLUMN date_version TO "date";
ALTER TABLE "EUResearchHub".document_versions ALTER COLUMN "date" TYPE timestamp USING "date"::timestamp;
````
>Update of the name and the type of date_version
---

<h3 id="evr" >Evaluators</h3>

````sql
CREATE TABLE "EUResearchHub".evaluators (
	id int NULL,
	"password" varchar NULL,
	"name" varchar NULL,
	email varchar NULL,
	CONSTRAINT evaluators_pk PRIMARY KEY (id)
);
````
>Query for the creation of the Evaluators Table
---

````sql
ALTER TABLE "EUResearchHub".evaluators ADD surname varchar NULL;
````
>Add of the surname attribute
---

<h3 id="evrmsg" >Evaluators Messages</h3>

````sql
CREATE TABLE "EUResearchHub".evaluators_messages (
	fk_evaluators int NULL,
	fk_messages int NULL,
	CONSTRAINT evaluators_messages_pk PRIMARY KEY (fk_evaluators,fk_messages),
	CONSTRAINT evaluators_messages_fk FOREIGN KEY (fk_messages) REFERENCES "EUResearchHub".messages(id),
	CONSTRAINT evaluators_messages_fk_1 FOREIGN KEY (fk_evaluators) REFERENCES "EUResearchHub".evaluators(id)
);
````
>Query for the creation of the Evaluators Messages Table
---

<h3 id="evrprj" >Evaluators Projects</h3>

````sql
CREATE TABLE "EUResearchHub".evaluators_projects (
	fk_evaluators int NULL,
	fk_projects int NULL,
	CONSTRAINT evaluators_projects_pk PRIMARY KEY (fk_evaluators,fk_projects),
	CONSTRAINT evaluators_projects_fk FOREIGN KEY (fk_projects) REFERENCES "EUResearchHub".projects(id),
	CONSTRAINT evaluators_projects_fk_1 FOREIGN KEY (fk_evaluators) REFERENCES "EUResearchHub".evaluators(id)
);
````
>Query for the creation of the Evaluators Projects Table
---

<h3 id="evnrep" >Evaluation Reports</h3>

````sql
CREATE TABLE "EUResearchHub".evaluation_reports (
	id int NULL,
	"comment" varchar NULL,
	date_creation date NULL,
	file_path varchar NULL,
	fk_document int NOT NULL,
	CONSTRAINT evaluation_reports_pk PRIMARY KEY (id),
	CONSTRAINT evaluation_reports_fk FOREIGN KEY (fk_document) REFERENCES "EUResearchHub".documents(id)
);
````
>Query for the creation of the Evaluation Reports Table
---

````sql
ALTER TABLE "EUResearchHub".evaluation_reports RENAME COLUMN date_creation TO "date";
ALTER TABLE "EUResearchHub".evaluation_reports ALTER COLUMN "date" TYPE timestamp USING "date"::timestamp;
````
>Update of the name and the type of date_creation
---

<h3 id="evrevnrep" >Evaluators Evaluation Reports</h3>

````sql
CREATE TABLE "EUResearchHub".evaluators_evaluation_reports (
	fk_evaluators int NULL,
	fk_evaluation_reports int NULL,
	CONSTRAINT evaluators_evaluation_reports_pk PRIMARY KEY (fk_evaluators,fk_evaluation_reports),
	CONSTRAINT evaluators_evaluation_reports_fk FOREIGN KEY (fk_evaluation_reports) REFERENCES "EUResearchHub".evaluation_reports(id),
	CONSTRAINT evaluators_evaluation_reports_fk_1 FOREIGN KEY (fk_evaluators) REFERENCES "EUResearchHub".evaluators(id)
);
````
>Query for the creation of the Evaluators Evaluation Reports Table
---

<h3 id="res" >Researchers</h3>

````sql
CREATE TABLE "EUResearchHub".researchers (
	id int NULL,
	"password" varchar NULL,
	"name" varchar NULL,
	email varchar NULL,
	affiliation varchar NULL,
	CONSTRAINT researchers_pk PRIMARY KEY (id)
);
````
>Query for the creation of the Researchers Table
---

````sql
ALTER TABLE "EUResearchHub".researchers ADD surname varchar NULL;
````
>Add of the surname attribute
---


<h3 id="resprj" >Researchers Projects</h3>

````sql
CREATE TABLE "EUResearchHub".researchers_projects (
	fk_researchers int NULL,
	fk_projects int NULL,
	CONSTRAINT researchers_projects_pk PRIMARY KEY (fk_researchers,fk_projects),
	CONSTRAINT researchers_projects_fk FOREIGN KEY (fk_projects) REFERENCES "EUResearchHub".projects(id),
	CONSTRAINT researchers_projects_fk_1 FOREIGN KEY (fk_researchers) REFERENCES "EUResearchHub".researchers(id)
);
````
>Query for the creation of the Researchers Projects Table
---

<h3 id="resmsg" >Researchers Messages</h3>

````sql
CREATE TABLE "EUResearchHub".researchers_messages (
	fk_researchers int NULL,
	fk_messages int NULL,
	CONSTRAINT researchers_messages_pk PRIMARY KEY (fk_researchers,fk_messages),
	CONSTRAINT researchers_messages_fk FOREIGN KEY (fk_messages) REFERENCES "EUResearchHub".messages(id),
	CONSTRAINT researchers_messages_fk_1 FOREIGN KEY (fk_researchers) REFERENCES "EUResearchHub".researchers(id)
);
````
>Query for the creation of the Researchers Messages Table

---

<h2 id="roles" >Roles</h2>

<p>
SQL roles are used to group database users into sets that share common 
privileges and permissions. By assigning a role to a user, the user 
automatically inherits all the privileges and permissions associated with 
that role. This helps simplify the process of managing user privileges and 
access control within a database.
</p>

- [Admin](#admin)
- [Researcher Role](#res-role)
- [Evaluator role](#evr-role)

---

<h3 id="admin" >Admin</h3>
````sql
CREATE ROLE "Admin" SUPERUSER CREATEDB CREATEROLE NOINHERIT LOGIN NOREPLICATION BYPASSRLS PASSWORD '1234';
GRANT ALL ON SCHEMA "EUResearchHub" TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".document_types TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".document_versions TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".documents TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".evaluation_reports TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".evaluation_windows TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".evaluators TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".evaluators_evaluation_reports TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".evaluators_messages TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".evaluators_projects TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".messages TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".projects TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".researchers TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".researchers_messages TO "Admin";
GRANT ALL ON TABLE "EUResearchHub".researchers_projects TO "Admin";
````
>Query for the creation of the Admin role
---

<h3 id="res-role" >Researcher</h3>
````sql
CREATE ROLE researcher NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN NOREPLICATION NOBYPASSRLS PASSWORD '1234';
GRANT SELECT ON TABLE "EUResearchHub".document_types TO researcher;
GRANT INSERT, SELECT ON TABLE "EUResearchHub".document_versions TO researcher;
GRANT INSERT, DELETE, SELECT ON TABLE "EUResearchHub".documents TO researcher;
GRANT SELECT ON TABLE "EUResearchHub".evaluation_reports TO researcher;
GRANT SELECT ON TABLE "EUResearchHub".evaluation_windows TO researcher;
GRANT INSERT, SELECT ON TABLE "EUResearchHub".messages TO researcher;
GRANT INSERT, DELETE, SELECT ON TABLE "EUResearchHub".projects TO researcher;
GRANT INSERT, SELECT ON TABLE "EUResearchHub".researchers_projects TO researcher;
GRANT SELECT ON TABLE "EUResearchHub".researchers_messages TO researcher;
````
>Query for the creation of the Researcher role
---

<h3 id="evr-role" >Evaluators</h3>
````sql
CREATE ROLE evaluator NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN NOREPLICATION NOBYPASSRLS PASSWORD '4321';
GRANT SELECT ON TABLE "EUResearchHub".document_types TO evaluator;
GRANT SELECT ON TABLE "EUResearchHub".document_versions TO evaluator;
GRANT SELECT ON TABLE "EUResearchHub".documents TO evaluator;
GRANT INSERT, SELECT ON TABLE "EUResearchHub".evaluation_reports TO evaluator;
GRANT SELECT ON TABLE "EUResearchHub".evaluation_windows TO evaluator;
GRANT INSERT ON TABLE "EUResearchHub".messages TO evaluator;
GRANT UPDATE, SELECT ON TABLE "EUResearchHub".projects TO evaluator;
GRANT SELECT ON TABLE "EUResearchHub".researchers TO evaluator;
GRANT SELECT ON TABLE "EUResearchHub".researchers_messages TO evaluator;
GRANT SELECT ON TABLE "EUResearchHub".researchers_projects TO evaluator;
````
>Query for the creation of the Evaluator role
---


<h2 id="triggers" >Triggers</h2>



