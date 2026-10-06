"""Run with Blender --python-exit-code 1 -P; uses an isolated factory scene."""
import math
import sys
import tempfile
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reflection_card import create_card


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.mesh.primitive_cube_add()
    original = bpy.context.object
    original_matrix = [list(row) for row in original.matrix_world]
    selected = list(bpy.context.selected_objects)
    card = create_card('Test card', size=(2, 4), location=(1, 2, 3), target=(2, 4, 6), roll=.4)
    bpy.context.view_layer.update()
    assert bpy.context.object == original and list(bpy.context.selected_objects) == selected
    assert [list(row) for row in original.matrix_world] == original_matrix
    normal = card.rotation_quaternion @ Vector((0, 0, 1))
    assert normal.dot(Vector((1, 2, 3)).normalized()) > .999999
    assert tuple(card.scale) == (1, 1, 1)
    assert math.isclose((card.data.vertices[1].co - card.data.vertices[0].co).length, 2)
    assert math.isclose((card.data.vertices[2].co - card.data.vertices[1].co).length, 4)
    assert [tuple(v.uv) for v in card.data.uv_layers.active.data] == [(0, 0), (1, 0), (1, 1), (0, 1)]
    assert not card.visible_camera and not card.visible_shadow and card.visible_glossy and card.visible_diffuse
    tree = card.active_material.node_tree
    mix = next(n for n in tree.nodes if n.type == 'MIX_SHADER')
    assert mix.inputs[1].links[0].from_node.type == 'BSDF_TRANSPARENT'
    assert mix.inputs[2].links[0].from_node.type == 'EMISSION'
    ramp = tree.nodes['X feather'].color_ramp
    assert ramp.interpolation == 'B_SPLINE' and ramp.evaluate(.5)[0] > .5
    assert ramp.evaluate(.5)[0] > ramp.evaluate(0)[0]

    before = (len(bpy.data.objects), len(bpy.data.materials), len(bpy.data.meshes))
    for changes in ({'size': (0, 1)}, {'target': (0, 0, 0)}, {'grey': float('nan')},
                    {'x_stops': [(0, 0), (.5, 1), (.5, 0), (1, 0)]},
                    {'y_stops': [(0, -1), (1, 0)]}, {'strength': -1}):
        args = dict(size=(1, 1), location=(0, 0, 0), target=(0, 0, 1))
        args.update(changes)
        try:
            create_card('Invalid', **args)
        except ValueError:
            pass
        else:
            raise AssertionError(f'Invalid input accepted: {changes}')
        assert before == (len(bpy.data.objects), len(bpy.data.materials), len(bpy.data.meshes))

    second = create_card('Test card', size=(1, 1), location=(0, 0, 0), target=(0, 0, 1),
                         tone_stops=[(0, .1), (.5, 1), (1, .2)])
    assert second.name != card.name and second.data != card.data
    name = card.name  # Plain values survive opening another file.
    with tempfile.TemporaryDirectory(prefix='reflection-card-test-') as directory:
        scene = str(Path(directory) / 'test.blend')
        bpy.ops.wm.save_as_mainfile(filepath=scene)
        bpy.ops.wm.open_mainfile(filepath=scene)
        reopened = bpy.data.objects[name]
        assert reopened.visible_glossy and not reopened.visible_camera and not reopened.visible_shadow
        assert len(reopened.data.uv_layers.active.data) == 4
        assert reopened.active_material.node_tree.nodes['X feather'].color_ramp.interpolation == 'B_SPLINE'
    print('PASS: geometry, UVs, orientation, graph, visibility, preservation, input validation, independent cards and saved-scene roundtrip')


if __name__ == '__main__':
    main()
