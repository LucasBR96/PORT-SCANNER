# PORT SCANNER

UFF - UNIVERSIDADE FEDERAL FLUMINENSE

**Alunos:**
1. Lucas Fuzato Cipriano
2. João Pedro Loyola
3. Joel Lopes Cunha de Souza

**Matéria:** Redes de Computadores 1

**Turma:** A1

**Período**: 2021.1

## O trabalho

O objetivo desse trabalho é construir um port scanner, que é um programa que testa a conexão entre o computador do usuário e algum servidor dado pelo seu URL, através de um ou mais numero( s ) de porta, usando uma linguagem de programação de escolha dos integrantes do grupo e os conhecimentos adquiridos nas aulas da disciplina. Para tal, foi escolhida a linguagem de programação python na sua versão 3.8, sem nenhuma biblioteca de terceiros e usando apenas os módulos da biblioteca padrão. ( Entre eles o módulo socket ). 

## Como foi Feito.

Existem dois modos de execução: O **Iterativo** ou Sequencial, que cumpre os requisitos pedidos no enunciado do trabalho, e o **Multithread** ou Paralelo, a versão otimizada feita para buscar o ponto extra oferecido pelo professor como desafio.

Em ambos os modos o port scanner cria um socket para cada numero de porta que esteja entre os valores mínimo e máximo e que tenha um número de protocolo conhecido, para depois tentar uma conexão com o host alvo. Se a conexão for aceita, o programa classifica a porta como **ABERTA**, se a conexão expirar por timeout, o programa considera que um firewall está impedindo o cliente de fazer uma conexão pela porta escolhida, então classifica porta como **FILTRADA**. Em qualquer outro caso, a porta será classificada como **FECHADA**.

Para cada porta analisada, o scanner vai mostrar uma mensagem na tela igual à abaixo:

``

Além disso, antes de estabelecer a conexão, o programa testará se um protocolo é conhecido para o número de porta. Se não for, o port scanner irá ignorar o número. Isso pode ser mudado ao ao trocar o valor da variável *must_serv* para *False* no código fonte.

### Modo iterativo

Aqui o programa vai testar uma porta por vez, e mostrar o resultado imediatamente na tela. É relativamente lento comparado ao outro modo, com o tempo total de execução igual a soma do tempo de todas as portas. Mas entrega o que foi pedido

### Modo multithread

Como foi dito antes, esse modo foi feito considerando o desafio proposto pelo professor. Nele, usando os recursos disponibilizados pelo módulo threading, cada conexão é testada por uma thread distinta. Assim todas as portas são testadas ao mesmo tempo ( na prática ). Aqui o programa espera todos os testes serem finalizados antes de mostrar os resultados. O tempo de execução é igual ao maior tempo de resposta entre os números de porta mais um pequeno overhead causado pelo escalonamento das threads.

**CUIDADO:** Esse modo é bastante intensivo para a CPU. Podendo chegar a 100% de utilização. Use por sua conta e risco.

## Otimização

O professor desafiou os alunos a otimizar o programa com a promessa de um ponto extra em caso de sucesso. Seguindo a ideia do Joel, decidimos usar multithread para tal.

`Joel explica a ideia de multithread dele aqui`

## Como usar

Pode-se dizer que o programa ainda está em sua versão "beta" pois a versão com threads não está pronta nem testada, enquanto o Makefile não está pronto e não foi escrito ( ainda ) nenhum outro script de instalação. Então para executar o programa deve-se usar a forma "rudimentar".

1. Use **git clone** para 
