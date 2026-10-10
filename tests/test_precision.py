import importlib.util
from pathlib import Path
import shutil
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PublishedPrecisionTests(unittest.TestCase):
    def test_published_float_counterexample_is_true_and_discriminating(self):
        self.assertIsNotNone(shutil.which("php"), "PHP is required to verify the published claim")
        path = ROOT / "experimentos/2026-10-09-projeto-real/check_precision.py"
        spec = importlib.util.spec_from_file_location("check_precision", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.check(ROOT)
        self.assertTrue(result["valid"], result)


if __name__ == "__main__":
    unittest.main()
