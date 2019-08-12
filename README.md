Image annotation
================

This is a script to annotate single polygon within frames and save them into binary images.

## Requisites

- OpenCV;
- Python 3.5.2;
- Numpy;

## How to use

On Terminal, run the command:

```
python3 image_annotation.py -p path/to/frames/directory -s /path/to/save/annotations -c #resuming_frame_number
```

where
- -p path/to/frames/directory: optional argument, if not informed the default will be the current directory;
- -s /path/to/save/annotations: optional argument, if not informed the default will be the current directory;
- -c #resuming_frame_number: optional argument, if not informed the default will be first frame (0);