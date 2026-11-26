"""Checagem da ADR-doutorado-experiments (D2674).

Regras: experiments/ nao guarda credencial nem dado sensivel (repo publico) e
todo experimento em Python fixa a seed.
"""
import pathlib
import re
import unittest

RAIZ = pathlib.Path(__file__).resolve().parent.parent
EXPERIMENTS = RAIZ / "experiments"

NOMES_PROIBIDOS = re.compile(
    r"(^\.env($|\.)|\.pem$|\.key$|\.p12$|\.pfx$|id_rsa|credentials?\.json$|secrets?\.)",
    re.IGNORECASE,
)
SEED = re.compile(r"(seed\s*\(|random_state\s*=|SEED\s*=)")


def arquivos():
    return [p for p in EXPERIMENTS.rglob("*") if p.is_file()]


class RegrasExperiments(unittest.TestCase):
    def test_diretorio_existe(self):
        self.assertTrue(EXPERIMENTS.is_dir(), "experiments/ deve existir")

    def test_sem_credencial_ou_segredo(self):
        proibidos = [str(p.relative_to(RAIZ)) for p in arquivos() if NOMES_PROIBIDOS.search(p.name)]
        self.assertEqual(proibidos, [], f"arquivos proibidos em repo publico: {proibidos}")

    def test_experimento_python_fixa_seed(self):
        sem_seed = [
            str(p.relative_to(RAIZ))
            for p in arquivos()
            if p.suffix == ".py" and not SEED.search(p.read_text(encoding="utf-8"))
        ]
        self.assertEqual(sem_seed, [], f"experimento sem seed fixa: {sem_seed}")

    def test_detector_pega_violacao(self):
        self.assertTrue(NOMES_PROIBIDOS.search(".env"))
        self.assertTrue(NOMES_PROIBIDOS.search("id_rsa"))
        self.assertIsNone(SEED.search("import random\nprint(random.random())"))


if __name__ == "__main__":
    unittest.main()
