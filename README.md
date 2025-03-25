# Implementação da Camada de Enlace

Este projeto tem como objetivo implementar uma comunicação simples na camada de enlace utilizando dois processos: **remetente** e **destinatário**. O sistema utiliza um protocolo personalizado para encapsular uma mensagem em um *frame*, empregando cabeçalho e terminador para sincronização e adicionando o código de Hamming para detecção e correção de erros de 1 bit.

---

## Visão Geral

Neste projeto, dois processos independentes se comunicam por meio da troca de *frames* que contêm a mensagem original (payload) e bits de paridade gerados com o algoritmo de Hamming. O remetente constrói o frame e o envia pela saída padrão, enquanto o destinatário lê o frame, realiza a sincronização com base em um cabeçalho e terminador previamente definidos, corrige possíveis erros de 1 bit e extrai a mensagem original.

---

## Descrição do Projeto

O projeto é dividido em duas partes principais:

1. **Remetente**:  
   - Lê uma sequência de bits (payload) via *stdin*.
   - Calcula e insere os bits de paridade usando o código de Hamming.
   - Monta o frame com cabeçalho, payload codificado e terminador.
   - Envia o frame pela *stdout*.

2. **Destinatário**:  
   - Lê o frame completo via *stdin*.
   - Identifica o cabeçalho e o terminador para sincronizar a leitura.
   - Extrai o payload codificado e verifica/corrige possíveis erros de 1 bit.
   - Remove os bits de paridade para recuperar a mensagem original.
   - Exibe a mensagem decodificada na *stdout*.

---

## Detalhes do Protocolo

### Estrutura do Frame

O frame é construído da seguinte forma:

- **Cabeçalho (HEADER):**  
  Uma sequência de bits fixa (ex.: `01111110`) que marca o início do frame.

- **Payload Codificado:**  
  A mensagem original em bits, à qual são adicionados os bits de paridade calculados pelo código de Hamming.

- **Terminador (TERMINATOR):**  
  Uma sequência de bits fixa (ex.: `01111110`) que marca o final do frame.

Essa delimitação garante que o destinatário possa sincronizar a leitura do frame mesmo em fluxos contínuos de dados.

### Código de Hamming

O código de Hamming é utilizado para detectar e corrigir erros de 1 bit. Os principais passos são:

- **Determinar o número de bits de paridade necessários:**  
  Usando a fórmula:  
  \[
  2^p \geq m + p + 1
  \]
  onde *m* é o número de bits de dados e *p* o número de bits de paridade.

- **Inserir os bits de paridade:**  
  Os bits de paridade são posicionados nas posições que são potências de 2 (1, 2, 4, 8, ...).

- **Cálculo dos bits de paridade:**  
  Cada bit de paridade é calculado com base em blocos de bits selecionados conforme a posição. No destinatário, é recalculado o conjunto de paridade para detectar a presença de erros (síndrome). Se o resultado indicar um erro, o bit incorreto é corrigido.

---

## Arquivos do Projeto

- **remetente.py:**  
  Responsável por ler a mensagem, calcular os bits de Hamming, montar o frame (com cabeçalho e terminador) e enviar a mensagem codificada pela saída padrão.

- **destinatario.py:**  
  Responsável por ler o frame, sincronizar os dados com base nos delimitadores, detectar e corrigir erros de 1 bit, e extrair a mensagem original.

---

## Como Executar

### Testando o Remetente

Para testar somente o remetente e verificar se o frame está sendo montado corretamente, execute:
```bash
python3 remetente.py "01101001"
```

A saída deverá iniciar com o cabeçalho, seguida pelo payload codificado (com bits de paridade) e finalizar com o terminador.

Você pode redirecionar a saída para um arquivo para análise:

```bash
python3 remetente.py "01101001" > frame.txt
```

### Testando o Destinatário

Crie um arquivo de teste contendo um frame completo (gerado previamente pelo remetente) e execute:

```bash
cat frame.txt | python3 destinatario.py
```

Isso permitirá validar se o destinatário está conseguindo:

- Sincronizar a leitura através dos delimitadores.

- Corrigir eventuais erros de 1 bit.

- Extrair e exibir corretamente a mensagem original.

### Testando a Comunicação Completa

Para testar a comunicação entre os dois processos utilizando pipes, execute:

```bash
python3 remetente.py "01101001" | python3 destinatario.py
```

Se a implementação estiver correta, a saída será a mensagem original: 01101001.

## Testes e Validações

### Sincronização:

Certifique-se de que o destinatário localiza corretamente o cabeçalho e o terminador para extrair o payload codificado.

### Correção de Erros:

Teste a robustez do sistema modificando manualmente um bit no payload codificado (no arquivo de teste, por exemplo) e verifique se o destinatário detecta e corrige o erro.

### Integridade dos Dados:

Confirme que, mesmo após a inserção dos bits de paridade, a mensagem original é recuperada corretamente pelo destinatário.

## Considerações Finais

Este projeto demonstra conceitos fundamentais da camada de enlace, como a delimitação de frames, a sincronização de dados e a correção de erros utilizando o código de Hamming.