"""Create a separate numbered review board; never alter the clean input image."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size):
    for name in ('DejaVuSans.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def validate(data):
    if not isinstance(data.get('title'), str) or not data['title'].strip():
        raise ValueError('A review title is required')
    notes = data.get('notes')
    if not isinstance(notes, list) or not notes:
        raise ValueError('Nonempty observed notes are required')
    for note in notes:
        box = note.get('box')
        if not isinstance(box, list) or len(box) != 4 or any(type(v) not in (int, float) or not math.isfinite(v) for v in box):
            raise ValueError('box must be finite [x,y,width,height] values')
        x, y, w, h = box
        if min(x, y) < 0 or min(w, h) <= 0 or x + w > 1 or y + h > 1:
            raise ValueError('Normalized box lies outside image')
        if note.get('status') not in ('open', 'resolved', 'check'):
            raise ValueError('status must be open, resolved or check')
        for field in ('title', 'observation', 'action'):
            if not isinstance(note.get(field), str) or not note[field].strip():
                raise ValueError('Missing note ' + field)
    return notes


def wrap(text, face, width):
    # Pixel-based wrapping, including long words; no truncated annotations.
    lines = []
    for paragraph in text.splitlines() or ['']:
        line = ''
        for char in paragraph:
            candidate = line + char
            if face.getlength(candidate) > width and line:
                split = line.rfind(' ')
                if split > len(line) // 2:
                    lines.append(line[:split]); line = line[split + 1:] + char
                else:
                    lines.append(line); line = char
            else:
                line = candidate
        lines.append(line)
    return lines


def build(image_path, data, output):
    image_path = Path(image_path).resolve(strict=True)
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError('Choose a new review output directory')
    notes = validate(data)
    before = sha(image_path)
    with Image.open(image_path) as opened:
        source = opened.convert('RGB')
    width = 1280
    height = max(1, round(source.height * width / source.width))
    face, head, title_face = font(22), font(26), font(32)
    title_lines = wrap(data['title'], title_face, 1700)
    top = 36 + len(title_lines) * 42
    laid_out = []
    note_height = 0
    for i, note in enumerate(notes, 1):
        heading = wrap(f'{i:02} / {note["title"]}', head, 414)
        body = wrap(note['observation'] + '\nNext: ' + note['action'], face, 414)
        block = len(heading) * 33 + len(body) * 29 + 32
        laid_out.append((note, heading, body, note_height))
        note_height += block
    board = Image.new('RGB', (1800, top + max(height, note_height) + 62), '#f4f1ea')
    board.paste(source.resize((width, height), Image.Resampling.LANCZOS), (28, top))
    draw = ImageDraw.Draw(board)
    for i, line in enumerate(title_lines):
        draw.text((28, 22 + i * 42), line, font=title_face, fill='#222926')
    colours = {'open': '#be542e', 'resolved': '#326752', 'check': '#506c91'}
    for i, (note, headings, body, offset) in enumerate(laid_out, 1):
        colour = colours[note['status']]
        x, y, w, h = note['box']
        x0, y0 = 28 + round(x * width), top + round(y * height)
        x1, y1 = 28 + round((x + w) * width), top + round((y + h) * height)
        draw.rectangle((x0, y0, x1, y1), outline=colour, width=4)
        tagx = min(x0, 28 + width - 48); tagy = min(y0, top + height - 37)
        draw.rectangle((tagx, tagy, tagx + 48, tagy + 37), fill=colour)
        draw.text((tagx + 7, tagy + 3), str(i), font=head, fill='white')
        yy = top + offset
        for line in headings:
            draw.text((1340, yy), line, font=head, fill=colour); yy += 33
        for line in body:
            draw.text((1340, yy), line, font=face, fill='#27302a'); yy += 29
    footer = 'Separate review overlay | source SHA-256 ' + before[:20] + ' | open / resolved / check'
    draw.text((28, board.height - 40), footer, font=font(18), fill='#566159')
    output.mkdir(parents=True)
    board.save(output / 'review.png')
    record = dict(data, source_file=image_path.name, source_sha256=before,
                  source_size=list(source.size), board_size=list(board.size))
    (output / 'review.json').write_text(json.dumps(record, indent=2) + '\n')
    if sha(image_path) != before:
        raise RuntimeError('Clean image changed during review')
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path, required=True)
    parser.add_argument('--notes', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = build(args.image, json.loads(args.notes.read_text()), args.output)
    print('REVIEW_COMPLETE', result['source_sha256'])


if __name__ == '__main__':
    main()
