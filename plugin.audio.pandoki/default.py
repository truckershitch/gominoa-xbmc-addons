# Pandoki - Kodi Pandora client
import os, sys, time
import xbmc, xbmcaddon, xbmcgui, xbmcvfs
from urllib import parse as urlparse

path = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('path'))
path = xbmcvfs.translatePath(os.path.join(path, 'resources', 'lib'))
sys.path.append(path)

from resources.lib.pandoki import *

def Wait(key, value):
    Prop(key, value)
    if run: return

    until = time.time() + 15
    while Prop(key) and (time.time() < until):
        xbmc.sleep(1000)


handle	= sys.argv[1]
query	= urlparse.parse_qs(sys.argv[2][1:])

search	= query.get('search')[0] if query.get('search')	else None
create	= query.get('create')[0] if query.get('create')	else None
rename	= query.get('rename')[0] if query.get('rename')	else None
delete	= query.get('delete')[0] if query.get('delete')	else None
title	= query.get( 'title')[0] if query.get('title')	else None
thumb	= query.get( 'thumb')[0] if query.get('thumb')	else None
rate	= query.get(  'rate')[0] if query.get('rate')	else None
play	= query.get(  'play')[0] if query.get('play')	else None


run = Prop('run') # only start up once
if (not run) or (float(run) < (time.time() - 3)):
    run = Pandoki()
else: run = False


if search:
    if search == 'hcraes':
        search = xbmcgui.Dialog().input('%s - Search' % Val('name'), Prop('search'))
        Prop('search', search)

    Prop('handle',  handle)
    Wait('action', 'search')

elif create:
    Prop('create',  create)
    Wait('action', 'create')

elif rename:
    title = xbmcgui.Dialog().input('%s - Search' % Val('name'), title)
    Prop('title',   title)
    Prop('rename',  rename)
    Wait('action', 'rename')

elif delete and xbmcgui.Dialog().yesno('%s - Delete Station' % Val('name'), 'Are you sure you want to delete?', '', title):
    Prop('delete',  delete)
    Wait('action', 'delete')

elif thumb:
    img = xbmcgui.Dialog().browseSingle(2, 'Select Thumb', 'files', useThumbs = True)
    Val("art-%s" % thumb, img)
    xbmc.executebuiltin("Container.Refresh")

elif rate:
    Prop('rate',    rate)
    Wait('action', 'rate')

elif play:
    Prop('play',    play)
    Wait('action', 'play')

else:
    Prop('handle',  handle)
    Wait('action', 'dir')

if run:    run.Loop()
