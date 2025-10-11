CREATE DATABASE IF NOT EXISTS se_proj
USE DATABASE se_proj
  
CREATE TABLE users(

    --no eamil
    username varchar (100)  ,
    user_id char(10) AUTO_INCREMENT dafault starting "1111111111"or "0000000000" PRIMARY KEY, --starting from 1111111111 ,root admin id:  0000000000
    password char(10) ,
    status ENUM("ACTIVATE" , "INACTIVATED") DEFAULT "ACTIVE",
    careated_at datetime DEFAULT CURRENT_TIMESTAMP,
    last_login datetime null ,
    last_logout datetime null,

    role_id char(10),
    FOREIGN KEY (role_id)  REFERENCES roles(role_id)


    );

CREATE TABLE roles(

    role_id char(10) AUTOINCEREMNT PRIMARY KEY ,
    role_name ENUM("ADMIN" , "MANAGER" , "CASHIER")
    --discription needed?
);

INSERT INTO roles (role_id, role_name) VALUES ("0000000001","ADMIN")
INSERT INTO roles (role_id, role_name) VALUES ("0000000002" , "MANAGER")
INSERT INTO roles (role_id, role_name) VALUES ("0000000003","CASHIER")



CREATE TABLE report(

    report_id char(10) AUTOINCEREMNT PRIMARY KEY ,
    report_type ENUM("Inventory" , "Procurment" , "Requisition" , "System" ,"Audit" ),
    generated_at datetime DEFUALT CURRENTDATETIME,
    generated_by char(10) ,
    file_path varchar(255),

    FOREIGN KEY (generated_by) REFERENCES users(user_id)

);



CREATE TABLE audit_logs(--system activiies : tables saves every thing happened in the sys.

    log_id char(10) AUTOINCEREMNT PRIMARY KEY,--each system entry(log) has an ID
    user_id char(10) ,
    role_name ENUM("ADMIN" , "MANAGER" , "CASHIER"),
    action varchar(255) ,--written dynamically by the system exampl:"ADMIN added new manager"
    action_time datetime null DEFAULT CURRENT_TIMESTAMP,
  --module not sure yet it is catigoty

);

