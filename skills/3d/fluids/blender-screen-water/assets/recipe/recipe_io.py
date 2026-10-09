"""Portable paths, cache parsing and guards for isolated water jobs."""
import gzip
import hashlib
import json
import math
from pathlib import Path
import struct

RECIPE = Path(__file__).resolve().parent


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def recipe_hashes():
    return {p.name: sha(p) for p in sorted(RECIPE.glob('*.py'))}


def output_path(value):
    path = Path(value).expanduser().absolute()
    if path.is_symlink():
        raise ValueError('Output must not be a symlink')
    resolved = path.resolve()
    package = RECIPE.parents[1]
    protected = package if (package / 'SKILL.md').exists() else RECIPE
    if resolved.is_relative_to(protected):
        raise ValueError('Write to a working directory outside the skill/recipe')
    return resolved


def fresh_output(value):
    path = output_path(value)
    if path.exists():
        raise FileExistsError('Use a new output directory: ' + str(path))
    return path


def cache_snapshot(simulation):
    base = Path(simulation).resolve()
    return {str(p.relative_to(base)): {'bytes': p.stat().st_size, 'sha256': sha(p)}
            for p in sorted((base / 'cache/mesh').glob('fluid_mesh_*.bobj.gz'))}


def parse_frames(value):
    frames = []
    for part in value.split(','):
        if ':' in part:
            start, end = map(int, part.split(':'))
            if not 1 <= start < end <= 181:
                raise ValueError('Frame ranges must be within 1:181 with exclusive ends')
            frames.extend(range(start, end))
        else:
            frame = int(part)
            if not 1 <= frame <= 180:
                raise ValueError('Frames must be in 1–180')
            frames.append(frame)
    return sorted(set(frames))


def read_bobj(path):
    data = gzip.decompress(Path(path).read_bytes())
    position = 0

    def section(fmt):
        nonlocal position
        if position + 4 > len(data):
            raise ValueError('Truncated BOBJ count')
        count = struct.unpack_from('<i', data, position)[0]
        position += 4
        size = struct.calcsize(fmt)
        end = position + count * size
        if count < 0 or end > len(data):
            raise ValueError('Invalid BOBJ section length')
        values = list(struct.iter_unpack(fmt, data[position:end]))
        position = end
        return values

    vertices = section('<fff')
    section('<fff')  # Cached normals are replaced with Blender smooth shading.
    faces = section('<iii')
    if any(not math.isfinite(v) for point in vertices for v in point):
        raise ValueError('Non-finite BOBJ vertex')
    if any(i < 0 or i >= len(vertices) for face in faces for i in face):
        raise ValueError('Invalid BOBJ vertex index')
    return vertices, faces


def render_output(output, simulation, frames, settings):
    path = output_path(output)
    if path.is_relative_to(simulation):
        raise ValueError('Keep renders outside the simulation directory')
    for frame in frames:
        mesh = simulation / 'cache/mesh' / f'fluid_mesh_{frame:04d}.bobj.gz'
        if not mesh.is_file():
            raise FileNotFoundError('Missing cached mesh: ' + str(mesh))
    spec = dict(settings, recipe_hashes=recipe_hashes(), simulation=str(simulation),
                cache_meshes=cache_snapshot(simulation))
    manifest = path / 'settings.json'
    if path.exists():
        if not manifest.is_file() or json.loads(manifest.read_text()) != spec:
            raise ValueError('Recipe, settings or cache changed; use a new render directory')
        # A completed PNG is written atomically. Interrupted partial files are never resumed.
        if list(path.glob('*.partial*')):
            raise ValueError('Interrupted render present; use a new render directory')
    else:
        path.mkdir(parents=True, exist_ok=False)
        manifest.write_text(json.dumps(spec, indent=2) + '\n')
    return path
