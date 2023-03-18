USE ImagineCup

-- Esta query será usada apenas para realizar testes
SELECT * FROM Comando

DELETE FROM Comando

-- Populando o banco de dados com as primeiras mensagens
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO) VALUES ('hi', '<welcome-msg>')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO) VALUES ('hello', '<welcome-msg>')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO) VALUES ('start', '<welcome-msg>')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO) VALUES ('finish', '<goodbye-msg>')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO) VALUES ('end', '<goodbye-msg>')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO) VALUES ('bye', '<goodbye-msg>')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO) VALUES ('goodbye', '<goodbye-msg>')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO) VALUES ('info', '<info-command>')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO) VALUES ('information', '<info-command>')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO) VALUES ('commands', '<info-command>')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO, FUNCAO) VALUES ('click', '<click-command>', 'To select an element on the website.')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO, FUNCAO) VALUES ('click on', '<click-command>', 'To select an element on the website.')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO, FUNCAO) VALUES ('select', '<click-command>', 'To select an element on the website.')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO, FUNCAO) VALUES ('select the', '<click-command>', 'To select an element on the website.')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO, FUNCAO) VALUES ('choose', '<click-command>', 'To select an element on the website.')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO, FUNCAO) VALUES ('choose the', '<click-command>', 'To select an element on the website.')
INSERT INTO Comando(PALAVRA_CHAVE, COMANDO, FUNCAO) VALUES ('get', '<click-command>', 'To select an element on the website.')

-- Atualizando a tabela de Comandos
ALTER TABLE Comando
ADD FUNCAO VARCHAR(50)

-- Informando a função de cada comando
UPDATE Comando
    SET FUNCAO = 'To listen again my welcome message'
    WHERE COMANDO = '<welcome-msg>'
UPDATE Comando
    SET FUNCAO = 'To finish the conversation'
    WHERE COMANDO = '<goodbye-msg>'
UPDATE Comando
    SET FUNCAO = 'To listen the commands one more time'
    WHERE COMANDO = '<info-command>'

ALTER TABLE Produto
ALTER COLUMN BARCODE VARCHAR(13)
ALTER TABLE Produto
ADD TIPO_PRECO VARCHAR(15)

SELECT * FROM Produto

SELECT NOME FROM Produto ORDER BY NOME