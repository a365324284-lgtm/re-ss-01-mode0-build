import struct
import sys
import tarfile
import shutil
from pathlib import Path

def properties(data, offset):
    h = struct.unpack_from('>10I', data, offset)
    end = offset + h[1]
    if end > len(data):
        raise ValueError('Truncated FDT')
    pos, strings, stack = offset + h[2], offset + h[3], []
    out = {}
    while pos < end:
        token = struct.unpack_from('>I', data, pos)[0]
        pos += 4
        if token == 1:
            z = data.index(0, pos)
            stack.append(data[pos:z].decode())
            pos = (z + 4) & ~3
        elif token == 2:
            stack.pop()
        elif token == 3:
            n, nameoff = struct.unpack_from('>II', data, pos)
            pos += 8
            z = data.index(0, strings + nameoff)
            name = data[strings + nameoff:z].decode()
            out[('/'.join(stack), name)] = data[pos:pos+n]
            pos = (pos+n+3) & ~3
        elif token == 9:
            return out
        elif token != 4:
            raise ValueError('Bad token')
    raise ValueError('No FDT end')

def inspect(image):
    with tarfile.open(image) as t:
        kernel = t.extractfile('sysupgrade-jdcloud_re-ss-01/kernel').read()
    fit = properties(kernel, 0)
    dtb = fit[('/images/fdt-1', 'data')]
    props = properties(dtb, 0)
    assert props[('', 'model')] == b'JDCloud RE-SS-01\0'
    mode = struct.unpack('>I', props[('/soc@0/wifi@c000000', 'qcom,ath11k-fw-memory-mode')])[0]
    region = struct.unpack('>4I', props[('/reserved-memory/memory@4ab00000', 'reg')])
    return mode, region

if __name__ == '__main__':
    folder, dest = map(Path, sys.argv[1:])
    images = list(folder.glob('*jdcloud_re-ss-01-squashfs-sysupgrade.bin'))
    assert len(images) == 1, 'Expected exactly one board image'
    mode, region = inspect(images[0])
    assert mode == 0, f'Unexpected memory mode {mode}'
    assert region == (0, 0x4ab00000, 0, 0x5500000), f'Unexpected Q6 {region}'
    shutil.copy2(images[0], dest / ('EXPERIMENTAL-mode0-' + images[0].name))
    (dest / 'device-tree-check.txt').write_text(
        'Model: JDCloud RE-SS-01\nMode: 0\nQ6: 0x4ab00000 + 0x5500000 (85 MiB)\n'
        'Static checks only. No hardware test. No guarantee of >8 AP operation.\n')
