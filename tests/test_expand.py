import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
import json


REPO = Path(os.environ.get("SKILLS_ROOT", Path(__file__).resolve().parents[1]))
REFERENCE = ".ai/skills/feature-tickets/references/expand-contract.md"
CASES = (
    ("old_writer", "Antigo", "Inicial", ["nome"], ["Antigo", "Antigo"]),
    ("new_writer", "Inicial", "Novo", ["razao_social"], ["Novo", "Novo"]),
    ("equal_both", "Igual", "Igual", ["nome", "razao_social"], ["Igual", "Igual"]),
    ("no_dirty", "Antigo", "Novo", [], ["Antigo", "Novo"]),
    ("conflicting_both", "Antigo", "Novo", ["nome", "razao_social"], None),
)

# Extrai o callback publicado e testa somente sua lógica, com model e persistência simulados.
# Não exerce eventos, banco, casts ou integração Laravel/Pest.
PHP_STUB = r"""<?php
namespace Illuminate\Validation {
    class ValidationException extends \RuntimeException {
        public array $messages;
        public static function withMessages(array $messages): self {
            $exception = new self('validation');
            $exception->messages = $messages;
            return $exception;
        }
    }
}
namespace {
    class Cliente {
        public function __construct(public ?string $nome, public ?string $razao_social, private array $dirty) {}
        public function isDirty(string $column): bool { return in_array($column, $this->dirty, true); }
    }
    $callback = __CALLBACK__;
    [$name, $old, $new, $dirty, $expected] = json_decode($argv[1], true, flags: JSON_THROW_ON_ERROR);
    $model = new Cliente($old, $new, $dirty);
    $persisted = ['Inicial', 'Inicial'];
    $rejected = false;
    try {
        $callback($model);
        $persisted = [$model->nome, $model->razao_social];
    } catch (\Illuminate\Validation\ValidationException $exception) {
        $rejected = true;
        assert(isset($exception->messages['razao_social']), 'erro vinculado à coluna nova');
    }
    if ($expected === null) {
        assert($rejected, 'ambos dirty divergentes devem rejeitar');
        assert($persisted === ['Inicial', 'Inicial'], 'rejeição preserva persistência simulada');
        assert([$model->nome, $model->razao_social] === [$old, $new], 'sem precedência silenciosa');
    } else {
        assert(!$rejected, 'escrita compatível deve ser aceita');
        assert([$model->nome, $model->razao_social] === $expected, 'valores esperados');
    }
    echo "PASS $name\n";
}
"""


class ExpandContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which("php"):
            raise RuntimeError("O self-check do exemplo exige PHP no PATH.")

    def test_published_callback_preserves_double_write_contract(self):
        document = (REPO / REFERENCE).read_text(encoding="utf-8")
        callback = re.search(
            r"static::saving\((function \(Cliente \$cliente\): void \{.*?\n\s*\})\);",
            document,
            re.S,
        )
        self.assertIsNotNone(callback, "Callback saving ausente no exemplo expand-contract.")
        self.case_results = []
        with tempfile.TemporaryDirectory(prefix="skills-expand-") as temp:
            script = Path(temp) / "callback.php"
            script.write_text(PHP_STUB.replace("__CALLBACK__", callback.group(1)), encoding="utf-8")
            for case in CASES:
                with self.subTest(case=case[0]):
                    result = subprocess.run(
                        [
                            "php", "-d", "zend.assertions=1", "-d", "assert.exception=1",
                            str(script), json.dumps(case),
                        ],
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        timeout=10,
                    )
                    self.case_results.append({
                        "case": case[0], "returncode": result.returncode,
                        "stdout": result.stdout, "stderr": result.stderr,
                    })
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertEqual(result.stdout, "PASS " + case[0] + "\n")


if __name__ == "__main__":
    unittest.main()
