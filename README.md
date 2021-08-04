# PORT SCANNER

UFF - UNIVERSIDADE FEDERAL FLUMINENSE

**Alunos**

**Matéria:** Redes de Computadores 1

**Turma:** A1

**Período**: 2021.1

## O trabalho

O objetivo desse trabalho é construir um port scanner, que é um programa que testa a conexão entre o computador do usuário e algum servidor dado pelo seu URL, através de um ou mais numero( s ) de porta, usando uma linguagem de programação de escolha dos integrantes do grupo e os conhecimentos adquiridos nas aulas da disciplina. Para tal, foi escolhida a linguagem de programação python na sua versão 3.8, sem nenhuma biblioteca de terceiros e usando apenas os módulos da biblioteca padrão. ( Entre eles o módulo socket ). Um detalhe é que esse projeto não utiliza objetos, a não ser aqueles de classes ja definidas pela linguagem.

## Conteúdos desse diretório

O diretório aqui presente contém o código desenvolvido pelos integrantes do grupo para o trabalho. A pasta src contém o código fonte propriamente dito para a aplicação, o Makefile auxilia na instalação do aplicativo tema do projeto, e o README. Vendo a pasta src com mais detalhes:

1. O arquivo iteractive.py contém o código fonte para a execução do port scanner em modo iterativo, que é o modo de execução padrão para esse trabalho. No momento que este README é escrito esse arquivo está praticamente pronto.

2. O arquivo thrdport.py, por sua vez, é a fonte para a excução em modo multithread. Esse modo foi pensado para o ponto extra que o professor ofereceu em troca do desafio de otimizar o aplicativo. Não está pronto ainda

3. O arquivo pscan.py é o código principal do aplicativo. Enquanto o Makefile não estiver pronto é por ele que o programa deve ser executado.

4. Finalmente, tests.py contém os testes para o garantir o bom funcionameto das funções desenvolvidas nos outros arquivos.

## Otimização

O professor desafiou os alunos a otimizar o programa com a promessa de um ponto extra em caso de sucesso. Seguindo a ideia do Joel, decidimos usar multithread para tal.

`Joel explica a ideia de multithread dele aqui`

## Como usar


