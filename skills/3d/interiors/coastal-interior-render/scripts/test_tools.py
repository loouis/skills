"""Small portability and negative-control tests; no production quality claim."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


review = module('review_board')
render = module('render_views')


class ToolsTest(unittest.TestCase):
    def note(self):
        return {'title': 'Long review title ' * 15, 'notes': [dict(title='A long observation ' * 8,
            status='open', box=[.1, .2, .4, .3], observation='Inspect this actual region. ' * 14,
            action='Render a matched control and inspect the result.')]}

    def test_source_immutable_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp); source = p / 'clean.png'
            Image.new('RGB', (320, 180), '#aa9977').save(source)
            before = source.read_bytes()
            result = review.build(source, self.note(), p / 'review')
            self.assertEqual(before, source.read_bytes())
            self.assertGreater(result['board_size'][1], 720)
            self.assertEqual(result['source_size'], [320, 180])
            self.assertEqual(json.loads((p/'review/review.json').read_text())['source_sha256'], review.sha(source))
            with self.assertRaises(FileExistsError):
                review.build(source, self.note(), p / 'review')

    def test_invalid_notes_fail_closed(self):
        for bad in ([], [dict(self.note()['notes'][0], box=[.9, .1, .2, .3])],
                    [dict(self.note()['notes'][0], box=[float('nan'), .1, .2, .3])],
                    [dict(self.note()['notes'][0], action='')]):
            with self.assertRaises(ValueError):
                review.validate(dict(title='Test', notes=bad))

    def test_camera_manifest_preflight(self):
        view = dict(camera='Hero', slug='hero', width=640, height=360, samples=8)
        self.assertEqual(render.validate_views({'views': [view]}, {'Hero'}), [view])
        for views in ([], [dict(view, camera='Typo')], [view, view],
                      [dict(view, slug='../overwrite')], [dict(view, width=0)],
                      [dict(view, samples=True)]):
            with self.assertRaises(ValueError):
                render.validate_views({'views': views}, {'Hero'})


if __name__ == '__main__':
    unittest.main()
