CREATE OR REPLACE FUNCTION aumento () RETURNS void 
AS $$

DECLARE

valor integer := 10;

BEGIN
	
	UPDATE dados set salary =  salary * 1.10 ;

END;

$$ LANGUAGE plpgsql;	
//////////////////////////////////////////
CREATE OR REPLACE FUNCTION aumento_variavel (valor float, funcionario integer) RETURNS void 
AS $$

BEGIN
	
	UPDATE dados set salary =  salary * valor WHERE id = funcionario;

END;

$$ LANGUAGE plpgsql;	
/////////////////////////
CREATE OR REPLACE FUNCTION imposto() RETURNS trigger AS $$
 BEGIN
 NEW.salary_imp := NEW.salary * 1.10;
 RETURN NEW;
 END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER imposto_trigger before INSERT ON dados
FOR EACH ROW EXECUTE PROCEDURE imposto();


create table EMPREGADO
( 
	id int not null primary key, 
	nome varchar, 
	cpf CHAR(12) NOT NULL, 
	Num_Departamento SMALLINT NOT NULL, 
	Salario DECIMAL(10,2), 
	Supervisor CHAR(12) 
);

create table Auditoria
(
	empregado_ID int,
	cpf CHAR(12) NOT NULL,
	Num_Departamento SMALLINT NOT NULL,
	Salario DECIMAL(10,2 ), 
	Supervisor CHAR(12) ,
	evento int, 
	usuario varchar, 
	date date
);

CREATE OR REPLACE FUNCTION audit() RETURNS trigger AS $$
BEGIN

IF (TG_OP = 'INSERT') THEN
 INSERT INTO Auditoria VALUES 
 (
 	NEW.id, 
 	NEW.cpf,
 	NEW.Num_Departamento,
 	NEW.Salario,
 	NEW.Supervisor,
 	1,
 	USER,
 	NOW()
 );
 RETURN NEW;
END IF;
IF (TG_OP = 'UPDATE') THEN
 INSERT INTO Auditoria VALUES 
 (
 	NEW.id,  
 	NEW.cpf,
 	NEW.Num_Departamento,
 	NEW.Salario,
 	NEW.Supervisor,
 	2,
 	USER,
 	NOW()
 );
 RETURN NEW;
END IF;

IF (TG_OP = 'DELETE') THEN
 INSERT INTO Auditoria VALUES 
 (
 	OLD.id,  
 	OLD.cpf,
 	OLD.Num_Departamento,
 	OLD.Salario,
 	OLD.Supervisor,
 	3,
 	USER,
 	NOW()
 );
 RETURN OLD;
END IF;

END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_trigger before INSERT OR DELETE OR UPDATE ON EMPREGADO
FOR EACH ROW EXECUTE PROCEDURE audit();

INSERT INTO EMPREGADO VALUES (1, 'TESTE', 20, 10, 1000, 'ZE');
INSERT INTO EMPREGADO VALUES (2, 'TESTE 2', 21, 10, 2000, 'EU');
INSERT INTO EMPREGADO VALUES (3, 'TESTE 3', 22, 10, 3000, 'OPA');
INSERT INTO EMPREGADO VALUES (4, 'TESTE 4', 23, 10, 4000, 'OI');

UPDATE EMPREGADO set Salario = 1300 WHERE id = 1;
UPDATE EMPREGADO set Salario = 2300 WHERE id = 2;
UPDATE EMPREGADO set Salario = 3300 WHERE id = 3;
UPDATE EMPREGADO set Salario = 4300 WHERE id = 4;

DELETE FROM EMPREGADO WHERE id = 20;
DELETE FROM EMPREGADO WHERE id = 1;


----------------------------------

CREATE TABLE AvailableFlights
(
	Num_flight in , 
	date date, 
	numberOfFreeSeats int , 
	price float
);

CREATE TABLE Bookings(Num_flight int , date date , passenger int , price float)
