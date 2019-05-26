#!/usr/bin/python3
# Autor: Cleiton Piccini.
# Trabalho com a finalidade de interpretar um arquivo de log pós falha de um SGBD.
import re


def openArq(nameArq):
	
	arq = open (nameArq, 'r+')
	linha = []
	#Percorre todo o arquivo, separando cada linha para um indice de um array
	for indice in arq:
		#Divide a linha, transformando ela em um vetor, cada elemento é separado de acordo com o token especificado
	    aux = indice.split('\n')
	    linha.append(aux[0])
	
	return linha

def defineProcess (linhas):

	nameProces = []
	i = 1
	#Percorre o Array das linhas do log, buscando os processos que foram startados.E os passando para o Array de processos.
	while (i < len(linhas)-1):
		result = re.search ('start', linhas[i]) 
		if result != None:
			aux1 = linhas[i].split('<')
			aux2 = aux1[1].split('>')
			aux3 = aux2[0].split(' ')
			nameProces.append(aux3[1])
		i = i + 1
	
	return nameProces

def defineCommit (linhas, nameProces):
	
	commits = []
	i = 1
	#Percorre o Array das linhas do log, buscando os processos que foram commitados.
	while (i < len(linhas)):
		result1 = re.search ('commit', linhas[i]) 
		result2 = re.search ('Commit', linhas[i]) 
		if result1 != None or result2 != None:
			j = 0
			#Percorre o Array de processos, caso exita um processo commitado o mesmo é passado para o Array de commitados.
			while (j < len(nameProces)):
				result = re.search (nameProces[j], linhas[i])
				if result != None:	
					commits.append(nameProces[j])
				j = j + 1
		i = i + 1
	
	return commits

def defineVars(linhas):

	nameVar = []
	valueVar = []
	i = 0
	aux1 = []
	#Divide a linha, transformando ela em um vetor, cada elemento é separado de acordo com o token especificado
	variaveis = linhas[0].split(' | ')
	#Percorre o array gerado pelo split do token '|'. Separando da string o nome da variavel e seu valor inicial.
	while (i < len(variaveis)):
		aux1 = variaveis[i].split('=')
		nameVar.append(aux1[0])
		valueVar.append (aux1[1])
		i = i + 1
		
	return nameVar, valueVar

def redo(linhas, commits, nameVar, valueVar ):
	
	redoProces = []
	redoVar = []
	redoValues = []
	redoOk = []

	i = (len(linhas)) - 1

	#percore todas as linha de tras para frente
	while (i >= 0) :

		n_linhas = 0
		#percore o array dos processos commitados
		while (n_linhas < len(commits)):
			n_vars = 0
			#percore o array das variaveis, para verificar qual variavel recebera REDO
			while (n_vars < len(nameVar)):
				var_ok = re.search(nameVar[n_vars], linhas[i])
				process_ok = re.search(commits[n_linhas], linhas[i])
				log_type = re.search('write', linhas[i])
				no_commit = re.search('Commit', linhas[i])
				#Teste casos de REDO do arquivo de log com base nos padroes do arquivo teste2.txt
				if (var_ok != None) and (process_ok != None) and (log_type != None):
					virgula = linhas[i].split(',')
					valor = virgula[2].split('>')
					print ('REDO',commits[n_linhas],nameVar[n_vars],'=', valor[0])	
					nameVar[n_vars] = '-1'
				#Testa casos de REDO do arquivo de log com base nos padroes do arquivo teste01.txt
				if (var_ok != None) and (process_ok != None) and (log_type == None) and (no_commit == None):
					virgula = linhas[i].split(',')
					valor = virgula[2].split('>')
					print ('REDO',commits[n_linhas],nameVar[n_vars],'=', valor[0])	
					nameVar[n_vars] = '-1'

				n_vars = n_vars + 1
			n_linhas = n_linhas + 1
		i = i - 1


arquivo = input('Digiete o nome arquivo de LOG : ')
linhas = openArq(arquivo)
processos = defineProcess(linhas)
comitados = defineCommit (linhas, processos)

nameVar, valueVar = defineVars(linhas)

redo(linhas, comitados, nameVar, valueVar)
