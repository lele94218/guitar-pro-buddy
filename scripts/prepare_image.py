#!/usr/bin/env python3
"""Create one cropped, bounded JPEG for review; never displays the image."""
from pathlib import Path
import argparse, io, json
from PIL import Image, ImageOps


def prepare(source, destination, crop=None, max_side=1600, max_kib=300):
    source=Path(source);destination=Path(destination)
    if source.resolve()==destination.resolve():raise ValueError('Keep the source; choose a different output path')
    if destination.suffix.lower() not in ('.jpg','.jpeg'):raise ValueError('Output must be JPEG')
    if not 128<=max_side<=2400 or not 10<=max_kib<=500:raise ValueError('Invalid review image budget')
    # PIL retains its decompression-bomb protections. Do not disable them.
    with Image.open(source) as original:
        im=ImageOps.exif_transpose(original)
        if crop:
            left,top,right,bottom=crop
            if not (0<=left<right<=im.width and 0<=top<bottom<=im.height):raise ValueError('Crop is outside the source')
            im=im.crop(crop)
        if im.mode!='RGB':
            rgba=im.convert('RGBA');rgb=Image.new('RGB',rgba.size,'white');rgb.paste(rgba,mask=rgba.getchannel('A'));im=rgb
        im.thumbnail((max_side,max_side),Image.Resampling.LANCZOS)
        data=None;quality=None
        # Bounded attempts; never silently shrink below readable preview size.
        for attempt in range(8):
            for q in (85,75,65):
                buf=io.BytesIO();im.save(buf,format='JPEG',quality=q,optimize=True)
                if buf.tell()<=max_kib*1024:data=buf.getvalue();quality=q;break
            if data is not None:break
            new=(max(1,int(im.width*.8)),max(1,int(im.height*.8)))
            if min(new)<240:break
            im=im.resize(new,Image.Resampling.LANCZOS)
        if data is None:raise ValueError('Cannot meet budget at useful size; crop a smaller relevant region')
        destination.parent.mkdir(parents=True,exist_ok=True)
        temporary=destination.with_suffix(destination.suffix+'.tmp')
        try:temporary.write_bytes(data);temporary.replace(destination)
        finally:temporary.unlink(missing_ok=True)
        return {'path':str(destination),'bytes':len(data),'width':im.width,'height':im.height,'quality':quality}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source');p.add_argument('destination')
    p.add_argument('--crop',type=int,nargs=4,metavar=('LEFT','TOP','RIGHT','BOTTOM'))
    p.add_argument('--max-side',type=int,default=1600);p.add_argument('--max-kib',type=int,default=300)
    a=p.parse_args()
    print(json.dumps(prepare(a.source,a.destination,a.crop,a.max_side,a.max_kib),ensure_ascii=False))
