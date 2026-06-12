"""Ponto de entrada da aplicacao de reconhecimento de formas."""

from __future__ import annotations

import argparse
import logging
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .correcoes import MetricasImagem
from .processamento import processar_imagem, salvar_comparacao, salvar_etapas
from .reconhecimento import ResultadoReconhecimento, reconhecer_formas
from .utils import configurar_logging, criar_diretorios, ler_imagem, listar_imagens, nome_seguro, salvar_imagem

LOGGER = logging.getLogger(__name__)
RAIZ_PROJETO = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Configuracao:
    imagens: Path
    resultados: Path
    relatorio: Path
    area_minima: float
    canny_baixo: int
    canny_alto: int
    limiar_escura: float = 80.0
    limiar_clara: float = 190.0
    limiar_contraste: float = 42.0
    limiar_ruido: float = 8.0


def gerar_texto_relatorio(
    nome_imagem: str,
    reconhecimento: ResultadoReconhecimento,
    processamentos: tuple[str, ...],
    metricas_iniciais: MetricasImagem,
    metricas_finais: MetricasImagem,
) -> str:
    contagens = Counter(objeto.forma for objeto in reconhecimento.objetos)
    tipos = ", ".join(f"{tipo} ({quantidade})" for tipo, quantidade in sorted(contagens.items())) or "Nenhum"
    linhas_objetos = [
        f"  {obj.indice}. {obj.forma}: area={obj.area:.2f} px2; "
        f"perimetro={obj.perimetro:.2f} px; circularidade={obj.circularidade:.3f}; caixa={obj.caixa}"
        for obj in reconhecimento.objetos
    ] or ["  Nenhum objeto detectado."]
    area_total = sum(objeto.area for objeto in reconhecimento.objetos)

    return "\n".join(
        [
            "RELATORIO DE PROCESSAMENTO E RECONHECIMENTO DE PADROES",
            "=" * 60,
            f"Nome da imagem: {nome_imagem}",
            f"Quantidade de objetos: {len(reconhecimento.objetos)}",
            f"Area total encontrada: {area_total:.2f} px2",
            f"Tipos de formas encontradas: {tipos}",
            "",
            "Metricas visuais:",
            "  Antes: "
            f"brilho={metricas_iniciais.brilho_medio:.2f}; "
            f"contraste={metricas_iniciais.contraste:.2f}; "
            f"ruido={metricas_iniciais.nivel_ruido:.2f}",
            "  Depois: "
            f"brilho={metricas_finais.brilho_medio:.2f}; "
            f"contraste={metricas_finais.contraste:.2f}; "
            f"ruido={metricas_finais.nivel_ruido:.2f}",
            "",
            "Objetos encontrados:",
            *linhas_objetos,
            "",
            "Processamentos aplicados:",
            *(f"  - {item}" for item in processamentos),
            "",
        ]
    )


def executar(config: Configuracao) -> int:
    criar_diretorios(config.imagens, config.resultados, config.relatorio)
    arquivos = listar_imagens(config.imagens)
    if not arquivos:
        LOGGER.warning("Nenhuma imagem encontrada em %s", config.imagens)
        LOGGER.info("Use 'python -m src.gerar_exemplos' para criar imagens demonstrativas.")
        return 0

    relatorios: list[str] = []
    falhas = 0
    for caminho in arquivos:
        LOGGER.info("Processando %s", caminho.name)
        try:
            imagem = ler_imagem(caminho)
            processamento = processar_imagem(
                imagem,
                canny_baixo=config.canny_baixo,
                canny_alto=config.canny_alto,
                limiar_escura=config.limiar_escura,
                limiar_clara=config.limiar_clara,
                limiar_contraste=config.limiar_contraste,
                limiar_ruido=config.limiar_ruido,
            )
            reconhecimento = reconhecer_formas(
                processamento.correcao.imagem, area_minima=config.area_minima
            )
            pasta_saida = config.resultados / nome_seguro(caminho.stem)
            salvar_etapas(processamento, pasta_saida)
            salvar_imagem(pasta_saida / "09_mascara_segmentacao.png", reconhecimento.mascara)
            salvar_imagem(pasta_saida / "10_formas_reconhecidas.png", reconhecimento.imagem_anotada)
            salvar_comparacao(imagem, reconhecimento.imagem_anotada, pasta_saida / "11_comparacao.png")

            texto = gerar_texto_relatorio(
                caminho.name,
                reconhecimento,
                processamento.processamentos_aplicados,
                processamento.correcao.metricas_iniciais,
                processamento.correcao.metricas_finais,
            )
            (config.relatorio / f"{nome_seguro(caminho.stem)}.txt").write_text(texto, encoding="utf-8")
            relatorios.append(texto)
        except Exception as erro:  # Mantem o lote em execucao se um arquivo estiver corrompido.
            falhas += 1
            LOGGER.exception("Falha ao processar %s: %s", caminho.name, erro)

    cabecalho = (
        "RELATORIO CONSOLIDADO\n"
        f"Gerado em: {datetime.now().astimezone().isoformat(timespec='seconds')}\n"
        f"Imagens processadas: {len(arquivos) - falhas}\nFalhas: {falhas}\n\n"
    )
    (config.relatorio / "relatorio_consolidado.txt").write_text(
        cabecalho + ("\n" + "-" * 70 + "\n").join(relatorios), encoding="utf-8"
    )
    LOGGER.info("Concluido: %d sucesso(s), %d falha(s).", len(arquivos) - falhas, falhas)
    return 1 if falhas else 0


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Processa imagens e reconhece formas geometricas.")
    parser.add_argument("--imagens", type=Path, default=RAIZ_PROJETO / "imagens")
    parser.add_argument("--resultados", type=Path, default=RAIZ_PROJETO / "resultados")
    parser.add_argument("--relatorio", type=Path, default=RAIZ_PROJETO / "relatorio")
    parser.add_argument("--area-minima", type=float, default=250.0)
    parser.add_argument("--canny-baixo", type=int, default=50)
    parser.add_argument("--canny-alto", type=int, default=150)
    parser.add_argument("--limiar-escura", type=float, default=80.0)
    parser.add_argument("--limiar-clara", type=float, default=190.0)
    parser.add_argument("--limiar-contraste", type=float, default=42.0)
    parser.add_argument("--limiar-ruido", type=float, default=8.0)
    parser.add_argument("--verbose", action="store_true")
    return parser


def main() -> int:
    argumentos = criar_parser().parse_args()
    configurar_logging(argumentos.verbose)
    if argumentos.area_minima <= 0:
        LOGGER.error("--area-minima deve ser maior que zero.")
        return 2
    if not 0 <= argumentos.canny_baixo < argumentos.canny_alto <= 255:
        LOGGER.error("Use 0 <= --canny-baixo < --canny-alto <= 255.")
        return 2
    if not 0 <= argumentos.limiar_escura < argumentos.limiar_clara <= 255:
        LOGGER.error("Use 0 <= --limiar-escura < --limiar-clara <= 255.")
        return 2
    if argumentos.limiar_contraste < 0 or argumentos.limiar_ruido < 0:
        LOGGER.error("Os limiares de contraste e ruido nao podem ser negativos.")
        return 2
    config = Configuracao(
        argumentos.imagens,
        argumentos.resultados,
        argumentos.relatorio,
        argumentos.area_minima,
        argumentos.canny_baixo,
        argumentos.canny_alto,
        argumentos.limiar_escura,
        argumentos.limiar_clara,
        argumentos.limiar_contraste,
        argumentos.limiar_ruido,
    )
    return executar(config)


if __name__ == "__main__":
    sys.exit(main())
