#!/usr/bin/env python3
import sys

HEADER = "01111110"
TERMINATOR = "01111110"

def is_power_of_two(x):
    return x and (x & (x - 1) == 0)

def calculate_parity_bits(data_bits):
    m = len(data_bits)
    # Determina quantos bits de paridade são necessários: 2^r >= m + r + 1
    r = 0
    while (2**r < m + r + 1):
        r += 1
    total_length = m + r
    # Cria um vetor (1-indexado) para os bits: posições de potência de 2 serão reservadas para paridade.
    bits = [None] * (total_length + 1)
    j = 0
    for i in range(1, total_length + 1):
        if is_power_of_two(i):
            bits[i] = 0  # placeholder para o bit de paridade
        else:
            bits[i] = int(data_bits[j])
            j += 1
    # Calcula cada bit de paridade
    for i in range(1, total_length + 1):
        if is_power_of_two(i):
            parity = 0
            j = i
            while j <= total_length:
                # Pega um bloco de i bits a partir de j
                block = bits[j:j+i]
                for bit in block:
                    parity ^= bit
                j += 2 * i
            bits[i] = parity
    # Converte a lista (ignorando a posição 0) para uma string de bits
    return ''.join(str(bit) for bit in bits[1:])

def main():
    if len(sys.argv) < 2:
        print("Uso: {} <sequência de bits>".format(sys.argv[0]))
        sys.exit(1)
    payload = sys.argv[1]
    # Validação simples: deve conter apenas 0s e 1s
    if any(ch not in '01' for ch in payload):
        print("Erro: a mensagem deve conter apenas 0s e 1s")
        sys.exit(1)
    
    # Gera o código de Hamming para o payload
    encoded_payload = calculate_parity_bits(payload)
    
    # Monta o frame: HEADER + encoded_payload + TERMINATOR
    frame = HEADER + encoded_payload + TERMINATOR
    sys.stdout.write(frame)
    
if __name__ == '__main__':
    main()
