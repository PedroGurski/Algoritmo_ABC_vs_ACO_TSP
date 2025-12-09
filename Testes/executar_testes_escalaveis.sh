#!/bin/bash

# ==============================================================================
# SCRIPT DE TESTES COM VARIAÇÃO GRANULAR (DE 5 EM 5)
# ==============================================================================

# --- Configuração dos Parâmetros para Teste ---
# Use o formato: seq <INÍCIO> <PASSO> <FIM>
#
# Você pode ajustar estes valores para controlar a granularidade e o tempo total.
# ATENÇÃO: Mais pontos de dados = mais tempo de execução.

# Varia o número de cidades de 10 a 50, em passos de 5 (9 valores)
CIDADES_SEQ="seq 10 5 30"

# Varia o número de abelhas de 10 a 100, em passos de 10 (10 valores)
ABELHAS_SEQ="seq 10 10 90"

# Varia o número de formigas de 10 a 100, em passos de 10 (10 valores)
FORMIGAS_SEQ="seq 10 10 90"

# --- Limpeza e Preparação ---
# Remove resultados antigos para garantir uma nova execução limpa.
echo "Limpando resultados antigos..."
rm -f resultados.csv
rm -rf graficos_gerados
echo "Limpeza concluída."

# --- Laços de Execução ---
# Calcula o número total de execuções para dar uma estimativa do progresso.
NUM_CIDADES=$(eval "$CIDADES_SEQ" | wc -l)
NUM_ABELHAS=$(eval "$ABELHAS_SEQ" | wc -l)
NUM_FORMIGAS=$(eval "$FORMIGAS_SEQ" | wc -l)
TOTAL_EXECS=$((NUM_CIDADES * NUM_ABELHAS * NUM_FORMIGAS))
COUNT=0

echo "Iniciando bateria de testes com $TOTAL_EXECS execuções..."

# Itera sobre todas as combinações definidas nas sequências
for CIDADES in $(eval "$CIDADES_SEQ"); do
  for ABELHAS in $(eval "$ABELHAS_SEQ"); do
    for FORMIGAS in $(eval "$FORMIGAS_SEQ"); do
      
      COUNT=$((COUNT + 1))
      echo "-----------------------------------------------------------------"
      echo "Execução $COUNT de $TOTAL_EXECS: Cidades=$CIDADES, Abelhas=$ABELHAS, Formigas=$FORMIGAS"
      echo "-----------------------------------------------------------------"

      # Chama o script Python (comparacao.py) com os parâmetros na ORDEM CORRETA
      python3 comparacao.py $CIDADES $ABELHAS $FORMIGAS
      
      # Verifica se o comando Python falhou
      if [ $? -ne 0 ]; then
          echo "ERRO: A execução com os parâmetros acima falhou. Abortando."
          exit 1
      fi

    done
  done
done

echo "================================================================="
echo "BATERIA DE TESTES CONCLUÍDA COM SUCESSO!"
echo "Resultados salvos em: resultados.csv"
echo "Gráficos individuais salvos em: graficos_gerados/"
echo "================================================================="
