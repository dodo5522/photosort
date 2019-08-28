# README #

## How to use?

```
usage: main.py [-h] [-d [PATH_ROOT_DST]]
               [-p SORT_PHOTO_EXTENTIONS [SORT_PHOTO_EXTENTIONS ...]]
               [-v SORT_VIDEO_EXTENTIONS [SORT_VIDEO_EXTENTIONS ...]]
               [-l DELIMITER] [--subdir-year] [--subdir-month] [--copy]
               [--callback-function CALLBACK_FUNCTION] [--debug DEBUG]
               path_root_src

This script to make directory of date which the photo is taken, and move the
photo into the directory.

positional arguments:
  path_root_src         Directory path where your taken photo files are
                        located.

optional arguments:
  -h, --help            show this help message and exit
  -d [PATH_ROOT_DST], --path-root-dst [PATH_ROOT_DST]
                        Directory path where you want to create date folder
                        and locate photo files. (default: same as source
                        directory)
  -p SORT_PHOTO_EXTENTIONS [SORT_PHOTO_EXTENTIONS ...], --sort-photo-extentions SORT_PHOTO_EXTENTIONS [SORT_PHOTO_EXTENTIONS ...]
                        Extentions of photo file which you want to sort.
                        (default: jpg)
  -v SORT_VIDEO_EXTENTIONS [SORT_VIDEO_EXTENTIONS ...], --sort-video-extentions SORT_VIDEO_EXTENTIONS [SORT_VIDEO_EXTENTIONS ...]
                        Extentions of video file which you want to sort.
                        (default: mov)
  -l DELIMITER, --delimiter DELIMITER
                        A character as delimiter which you want to set the
                        name of date folder like "2014-05-01". (default: none)
  --subdir-year         Generate sub directory of year if this is set.
  --subdir-month        Generate sub directory of month if this is set.
  --copy                Copy media files but not move.
  --callback-function CALLBACK_FUNCTION
                        Function to be callback when copying/moving a photo
                        finished. The format is like
                        "/User/takashi/flickr_uploader/flickr_uploader:up-
                        load?key=xxx&param=yyy". The "upload" function should
                        have an argument "path_to_photo_uploading" as first
                        and another args is passed to keyword arguments.
                        (default: none)
  --debug DEBUG         debug mode if this flag is set (default: info)
```
