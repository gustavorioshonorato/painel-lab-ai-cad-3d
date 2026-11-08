import json
import tempfile
import unittest
from pathlib import Path

from generator import build_layout, generate


class GeneratorTests(unittest.TestCase):
    def test_default_demo_has_layout_and_exports(self):
        with tempfile.TemporaryDirectory() as td:
            result = generate({"width_mm": 900, "height_mm": 1600, "drive_count": 2, "control_count": 1, "terminal_count": 12}, Path(td))
            self.assertEqual(len(result["layout"]["components"]), 5)
            self.assertIn("<svg", result["svg"])
            self.assertIn("AC1009", (Path(td) / "panel_layout.dxf").read_text(encoding="ascii"))
            saved = json.loads((Path(td) / "panel_config.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["counts"]["drives"], 2)

    def test_multiple_drive_rows_fit_default_enclosure(self):
        layout = build_layout({"width_mm": 900, "height_mm": 1800, "drive_count": 6, "control_count": 2, "terminal_count": 24})
        drives = [c for c in layout["components"] if c["kind"] == "drive"]
        self.assertEqual(len(drives), 6)
        self.assertGreater(len({c["y"] for c in drives}), 1)

    def test_invalid_dimensions_are_rejected(self):
        with self.assertRaises(ValueError):
            build_layout({"width_mm": 400, "height_mm": 1600})

    def test_too_many_controls_are_rejected_for_narrow_enclosure(self):
        with self.assertRaises(ValueError):
            build_layout({"width_mm": 600, "height_mm": 1600, "control_count": 5})

    def test_generated_entities_are_ascii_and_contain_no_client_tags(self):
        result = generate({"width_mm": 900, "height_mm": 1600, "drive_count": 1, "control_count": 1, "terminal_count": 8})
        dxf = result["dxf_bytes"]
        self.assertGreater(dxf, 500)
        labels = {c["id"] for c in result["layout"]["components"]}
        self.assertTrue(all(label.startswith(("P-", "C-", "A-", "T-")) for label in labels))


if __name__ == "__main__":
    unittest.main()
