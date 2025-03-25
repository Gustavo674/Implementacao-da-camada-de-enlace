#!/usr/bin/env python3
import sys

HEADER = "01111110"
TERMINATOR = "01111110"

def is_power_of_two(x):
    return x and (x & (x - 1) == 0)

def hamming_decode(encoded):
    n = len(encoded)
    # Cria um vetor 1-indexado com os bits recebidos
    bits = [None] + [int(ch) for ch in encoded]
    
    # Calcula o síndrome: soma os índices das posições de paridade que não conferem
    syndrome = 0
    i = 1
    while i <= n:
        if is_power_of_two(i):
            parity = 0
            j = i
            while j <= n:
                block = bits[j:j+i]
                for bit in block:
                    parity ^= bit
                j += 2 * i
            if parity != 0:
                syndrome += i
        i *= 2
    # Se o síndrome for diferente de zero, há erro em um único bit; corrige-o
    if syndrome != 0 and syndrome <= n:
        bits[syndrome] = 1 - bits[syndrome]
    
    # Extrai os bits de dados (exclui as posições que são potências de 2)
    data_bits = []
    for i in range(1, n + 1):
        if not is_power_of_two(i):
            data_bits.append(str(bits[i]))
    return ''.join(data_bits)

def main():
    # Lê o frame completo da entrada padrão
    frame = sys.stdin.read().strip()
    if not frame:
        print("Erro: nenhum dado recebido.")
        sys.exit(1)
    # Procura pelo HEADER e TERMINATOR para sincronizar
    start_index = frame.find(HEADER)
    if start_index == -1:
        print("Erro: cabeçalho não encontrado.")
        sys.exit(1)
    start_index += len(HEADER)
    end_index = frame.find(TERMINATOR, start_index)
    if end_index == -1:
        print("Erro: terminador não encontrado.")
        sys.exit(1)
    encoded_payload = frame[start_index:end_index]
    
    # Decodifica o bloco recebido e corrige erros de 1 bit, se houver
    decoded_message = hamming_decode(encoded_payload)
    sys.stdout.write(decoded_message)
    
if __name__ == '__main__':
    main()
