#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os,glob,sys,string,re
import shutil
import argparse
import mediainfo
from exifread import process_file, __version__

TAG_DATE_TIME = 'EXIF DateTimeOriginal'
#FIXME: issue#8
EXT_MOVIES = ('avi', 'AVI', 'mov', 'MOV', 'mp4', 'MP4')

class PhotoSort:
	def __init__(self, path_root_src=None, path_root_dst=None, ext_src=None, debug=False):
		extentions = []
		for extention in ext_src:
			extentions.append(extention.lower())
			extentions.append(extention.upper())
		
		setattr(self, "_ext_src", extentions)
		setattr(self, "_path_root_src", path_root_src)
		setattr(self, "_path_root_dst", path_root_dst)
		setattr(self, "_debug", debug)
	
	def get_src_dir(self):
		return self._path_root_src
	
	def get_dst_dir(self):
		return self._path_root_dst
	
	def get_src_ext(self):
		return self._ext_src
	
	def sort_files(self):
		for file_found in os.listdir(self._path_root_src):
			path_src_img = os.path.join(self._path_root_src, file_found)
			if not os.path.isfile(path_src_img):
				continue
			
			try:
				obj_img = None
				(path_src_img_wo_ext, ext) = os.path.splitext(file_found)
				
				#FIXME: issue#8
				# if the found mediafile is movies, use mediaionfo class method to get encoded date.
				date = None
				if ext[1:] in EXT_MOVIES:
					obj_media = mediainfo.MediaInfo(path_src_img, None)
					
					media_data = obj_media.info_video.get_encoded_date()
					date_and_time = media_data.split()
					# FIXME: issue#4:  want to translate directory name with some optional character.
					date = date_and_time[1].replace('-', '')
				
				# if the found mediafile is pictures, use exifread to get exif data and taken date.
				elif ext[1:] in self._ext_src:
					obj_img = open(path_src_img, "rb")
					exif_data = process_file(obj_img, stop_tag=TAG_DATE_TIME)
					obj_img.close()
					
					# thumbnail binary data is not used in this script.
					tag_unused = 'JPEGThumbnail'
					if tag_unused in exif_data:
						del exif_data[tag_unused]
					
					# EXIF DateTimeOriginal is stored with this format "YYYY:MM:DD HH:MM:SS".
					date_and_time = exif_data[TAG_DATE_TIME]
					
					# if date_and_time does not have attribute 'printable', enter to next loop.
					# FIXME: issue #4: want to translate directory name with some optional character.
					(date, time) = date_and_time.printable.split(' ')
					date = date.translate(None, ':')
				
				else:
					msg = 'This extention \'%s\' is not supported.' % ext[1:]
					raise ValueError(msg)
				
				# if destination path is not set, destination is same as source.
				if self._path_root_dst is not None:
					path_dst_dir = os.path.join(self._path_root_dst, date)
				else:
					path_dst_dir = os.path.join(os.path.dirname(path_src_img), date)
				path_dst_img = os.path.join(path_dst_dir, os.path.basename(path_src_img))
				
				# create directory to move.
				if not os.path.isdir(path_dst_dir):
					os.mkdir(path_dst_dir)
				shutil.move(path_src_img, path_dst_img)
				
			except Exception as err:
				if self._debug == True:
					print str(type(err)) + " occurs with message \"" + err.message + "\"."
				continue
			
			finally:
				if obj_img is not None:
					obj_img.close()
	
	def __del__(self):
		print "destructor is called."

# main routine for executed as python script
if __name__ == '__main__':
	try:
		parser = argparse.ArgumentParser(description='This script to make directory of date which the photo is taken, and move the photo into the directory.')
		parser.add_argument('path_root_src', \
				action='store', \
				nargs=None, \
				const=None, \
				default=None, \
				type=str, \
				choices=None, \
				help='Directory path where your taken photo files are located.', \
				metavar=None)
		parser.add_argument('-d', '--path-root-dst', \
				action='store', \
				nargs='?', \
				const=None, \
				default=None, \
				type=str, \
				choices=None, \
				help='Directory path where you want to create date folder and locate photo files. (default: same as source directory)', \
				metavar=None)
		parser.add_argument('-e', '--sort-files-extentions', \
				action='store', \
				nargs='+', \
				const=None, \
				default=['jpg'], \
				type=str, \
				choices=None, \
				help='Extentions of file which you want to sort. (default: jpg)', \
				metavar=None)
		parser.add_argument('--debug', \
				action='store_true', \
				default=False, \
				help='debug mode if this flag is set (default: False)')
		args = parser.parse_args()
		
		obj_photosort= PhotoSort(args.path_root_src, args.path_root_dst, args.sort_files_extentions, args.debug)
		obj_photosort.sort_files()
		
	except Exception as err:
		if args.debug == True:
			print "Exception type is ",type(err)
			print "Exception arg is ",err.args
			print "Exception is ",err
		
	finally:
		pass
