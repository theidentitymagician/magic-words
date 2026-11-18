# Tile a tall full-page phone screenshot into side-by-side strips for fast review.
# python3 mobile_grid.py page_390.jpg grid  -> grid_0.jpg, grid_1.jpg ...
import sys
from PIL import Image
src, prefix = sys.argv[1], sys.argv[2]
im = Image.open(src); W, H = im.size; ch = 1000
parts = [im.crop((0, y, W, min(y + ch, H))) for y in range(0, H, ch)]
for g in range(0, len(parts), 4):
    grp = parts[g:g + 4]; out = Image.new('RGB', (len(grp) * (W + 20), ch), 'white')
    for i, p in enumerate(grp): out.paste(p, (i * (W + 20), 0))
    out.save(f'{prefix}_{g // 4}.jpg', quality=80); print(f'{prefix}_{g // 4}.jpg')
