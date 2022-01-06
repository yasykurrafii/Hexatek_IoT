-- buat bikin user raspberry nya 
show grants for 'rasp1'@'192.168.25.3';
create user 'rasp2'@'192.168.25.3' identified by 'rasp2';
grant all privileges on *.*  to 'rasp2'@'192.168.25.3';
flush privileges;

CREATE SCHEMA `hexatek`;
USE hexatek;

CREATE TABLE dht(
	id INT NOT NULL AUTO_INCREMENT,
    ip VARCHAR(12) NOT NULL,
    suhu INT NOT NULL,
    humidity INT NOT NULL,
    tanggal DATETIME DEFAULT current_timestamp,
    primary key (id)
);

CREATE TABLE rly(
	id INT NOT NULL AUTO_INCREMENT,
    ip VARCHAR(12) NOT NULL,
    gpio INT NOT NULL,
    kondisi INT NOT NULL,
    tanggal DATETIME DEFAULT current_timestamp,
    primary key (id)
);

CREATE TABLE skl(
	id INT NOT NULL AUTO_INCREMENT,
    ip VARCHAR(12) NOT NULL,
    gpio INT NOT NULL,
    kondisi INT NOT NULL,
    tanggal DATETIME DEFAULT current_timestamp,
    primary key (id)
);