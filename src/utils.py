"""Funcoes utilitarias de arquivos, imagens e logging."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray

Imagem = NDArray[np.uint8]
EXTENSOES_SUPORTADAS = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}


def configurar_logging(verbose: bool = False) -> None:
    """Configura mensagens da aplicacao no terminal."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )


def criar_diretorios(*diretorios: Path) -> None:
    """Cria os diretorios informados, incluindo seus pais."""
    for diretorio in diretorios:
        diretorio.mkdir(parents=True, exist_ok=True)


def listar_imagens(diretorio: Path) -> list[Path]:
    """Lista imagens suportadas em ordem alfabetica, sem recursao."""
    if not diretorio.exists():
        raise FileNotFoundError(f"Diretorio de imagens nao encontrado: {diretorio}")
    if not diretorio.is_dir():
        raise NotADirectoryError(f"O caminho de imagens nao e um diretorio: {diretorio}")

    return sorted(
        (arquivo for arquivo in diretorio.iterdir() if arquivo.suffix.lower() in EXTENSOES_SUPORTADAS),
        key=lambda arquivo: arquivo.name.lower(),
    )


def ler_imagem(caminho: Path) -> Imagem:
    """Le uma imagem preservando corretamente caminhos com caracteres especiais."""
    try:
        dados = np.fromfile(caminho, dtype=np.uint8)
        imagem = cv2.imdecode(dados, cv2.IMREAD_COLOR)
    except (OSError, ValueError) as erro:
        raise OSError(f"Falha ao ler a imagem '{caminho}': {erro}") from erro
    if imagem is None:
        raise ValueError(f"Arquivo invalido ou formato nao suportado: {caminho}")
    return imagem


def salvar_imagem(caminho: Path, imagem: Imagem) -> None:
    """Salva uma imagem e informa claramente erros de codificacao ou escrita."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    extensao = caminho.suffix.lower() or ".png"
    sucesso, dados = cv2.imencode(extensao, imagem)
    if not sucesso:
        raise OSError(f"OpenCV nao conseguiu codificar a imagem: {caminho}")
    try:
        dados.tofile(caminho)
    except OSError as erro:
        raise OSError(f"Falha ao salvar '{caminho}': {erro}") from erro


def nome_seguro(nome: str) -> str:
    """Converte um nome de arquivo em identificador seguro para pastas."""
    limpo = re.sub(r"[^A-Za-z0-9_-]+", "_", nome.strip())
    return limpo.strip("_") or "imagem"

