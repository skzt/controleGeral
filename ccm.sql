use ccm;

CREATE TABLE Chamadas
(
	num_chamado VARCHAR(20) NOT NULL,
	num_serie VARCHAR(20) NOT NULL,
	data DATE NOT NULL,
	hora TIME,
	filial VARCHAR(3) NOT NULL,
	responsavel VARCHAR(30) NOT NULL,
	descricao VARCHAR(140) NOT NULL,
	PRIMARY KEY(num_chamado)
)ENGINE = INNODB;

CREATE TABLE Visitas
(
	id INT NOT NULL AUTO_INCREMENT,
	num_chamado VARCHAR(20) NOT NULL,
	data_visita DATE NOT NULL,
	hora_visita TIME,
	observacao VARCHAR(140) NOT NULL,
	resolvido BOOLEAN NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT FK_ChamadoVisitas FOREIGN KEY (num_chamado)
  	REFERENCES Chamadas(num_chamado)
  	ON DELETE CASCADE
  	ON UPDATE CASCADE 
)ENGINE = INNODB;

CREATE TABLE Pecas
(
	num_chamado VARCHAR(20) NOT NULL,
	nf_entrada INT(20) NOT NULL,
	data_envio DATE NOT NULL,
	nf_saida INT(20) UNIQUE,
	data_recebimento DATE,
	PRIMARY KEY(nf_entrada),
	CONSTRAINT FK_ChamadoPecas FOREIGN KEY(num_chamado) REFERENCES Chamadas(num_chamado)
	ON DELETE CASCADE
	ON UPDATE CASCADE
)ENGINE = INNODB;
