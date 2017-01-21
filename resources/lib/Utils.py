import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import xbmcplugin
import os, sys
import simplejson
import hashlib
import urllib
import random
import math
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageStat, ImageFilter
from decimal import *
from xml.dom.minidom import parse

AEONT_ADDON = xbmcaddon.Addon()
AEONT_ADDON_ID = AEONT_ADDON.getAddonInfo('id')
AEONT_ADDON_LANGUAGE = AEONT_ADDON.getLocalizedString
AEONT_ADDON_DATA_PATH = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % AEONT_ADDON_ID))
AEONT_ADDON_COLORS = os.path.join(AEONT_ADDON_DATA_PATH, "colors.txt")
HOME = xbmcgui.Window(10000)

aeont_colors_dict={}


def Random_Color():
    return "ff" + "%06x" % random.randint(0, 0xFFFFFF)


def Complementary_Color(hex_color):
    """Returns complementary RGB color [should be format((255!]
    rgb = [hex_color[2:4], hex_color[4:6], hex_color[6:8]]
    comp = [format((325 - int(a, 16)), '02x') for a in rgb]
    return "FF" + "%s" % ''.join(comp)
    Example:
    >>>complementaryColor('FFFFFF')
    '000000'
    """
    rgb = [hex_color[2:4], hex_color[4:6], hex_color[6:8]]
    comp = ['%02X' % (255 - int(a, 16)) for a in rgb]
    """
    if (int(comp[0], 16) > 99 and int(comp[0], 16) < 150 and
        int(comp[1], 16) > 99 and int(comp[1], 16) < 150 and
        int(comp[2], 16) > 99 and int(comp[2], 16) < 150):
            return "FFc2836d"
    """
    return "FF" + "%s" % ''.join(comp)


def RemoveQuotes(label):
    if label.startswith("'") and label.endswith("'") and len(label) > 2:
        label = label[1:-1]
        if label.startswith('"') and label.endswith('"') and len(label) > 2:
            label = label[1:-1]
    return label


def Color_Only(filterimage, var1, var2, var3):
    if filterimage == "":
        return "", "", ""
    md5 = hashlib.md5(filterimage).hexdigest()
    if not aeont_colors_dict:
        try:
            with open(AEONT_ADDON_COLORS) as file:
                for line in file:
                    a, b, c, d = line.strip().split(':')
                    global aeont_colors_dict
                    aeont_colors_dict[a] = b + ':' + c + ':' + d
        except:
            log ("no colors.txt yet")
    if md5 not in aeont_colors_dict:
        filename = md5 + ".png"
        targetfile = os.path.join(AEONT_ADDON_DATA_PATH, filename)
        cachedthumb = xbmc.getCacheThumbName(filterimage)
        xbmc_vid_cache_file = os.path.join("special://profile/Thumbnails/Video", cachedthumb[0], cachedthumb)
        xbmc_cache_file = os.path.join("special://profile/Thumbnails/", cachedthumb[0], cachedthumb[:-4] + ".jpg")

        img = None
        for i in range(1, 4):
            try:
                if xbmcvfs.exists(xbmc_cache_file):
                    
                    img = Image.open(xbmc.translatePath(xbmc_cache_file))
                    break
                elif xbmcvfs.exists(xbmc_vid_cache_file):
                    
                    img = Image.open(xbmc.translatePath(xbmc_vid_cache_file))
                    break
                else:
                    filterimage = urllib.unquote(filterimage.replace("image://", "")).decode('utf8')
                    if filterimage.endswith("/"):
                        filterimage = filterimage[:-1]
                    
                    xbmcvfs.copy(filterimage, targetfile)
                    img = Image.open(targetfile)
                    break
            except:
                xbmc.sleep(300)
        if not img:
            return "", ""
        img.thumbnail((128, 128), Image.ANTIALIAS)
        img = img.convert('RGB')

        imagecolor, cimagecolor, fimagecolor = Get_Colors(img, md5)

        global aeont_colors_dict
        aeont_colors_dict[md5] = imagecolor + ':' + cimagecolor + ':' + fimagecolor  # update entry
        with open(AEONT_ADDON_COLORS, 'w') as file:  # rewrite file
            for id, values in aeont_colors_dict.items():
                file.write(':'.join([id] + values.split(':')) + '\n')
    else:
        imagecolor, cimagecolor, fimagecolor = aeont_colors_dict[md5].split(':')
    HOME.setProperty(var1, imagecolor)
    HOME.setProperty(var2, cimagecolor)
    HOME.setProperty(var3, fimagecolor)
    return imagecolor, cimagecolor, fimagecolor


def Get_Colors(img, md5):
    if not aeont_colors_dict:
        try:
            with open(AEONT_ADDON_COLORS) as file:
                for line in file:
                    a, b, c, d = line.strip().split(':')
                    global aeont_colors_dict
                    aeont_colors_dict[a] = b + ':' + c + ':' + d
        except:
            log ("no colors.txt yet")
    if md5 not in aeont_colors_dict:
        colour_tuple = [None, None, None]
        for channel in range(3):
            # Get data for one channel at a time
            pixels = img.getdata(band=channel)
            values = []
            for pixel in pixels:
                values.append(pixel)
            colour_tuple[channel] = clamp(sum(values) / len(values))
        imagecolor = 'ff%02x%02x%02x' % tuple(colour_tuple)
        w, h = img.size
        pixels = img.getcolors(w * h)

        most_frequent_pixel = pixels[0]

        for count, colour in pixels:
            if count > most_frequent_pixel[0]:
                most_frequent_pixel = (count, colour)

        fimagecolor = 'ff%02x%02x%02x' % tuple(most_frequent_pixel[1])

        cimagecolor = Complementary_Color(imagecolor)
        global aeont_colors_dict
        aeont_colors_dict[md5] = imagecolor + ':' + cimagecolor + ':' + fimagecolor  # update entry
        with open(AEONT_ADDON_COLORS, 'w') as file:  # rewrite file
            for id, values in aeont_colors_dict.items():
                file.write(':'.join([id] + values.split(':')) + '\n')
    else:
        imagecolor, cimagecolor, fimagecolor = aeont_colors_dict[md5].split(':')
    return imagecolor, cimagecolor, fimagecolor





def clamp(x): 
    return max(0, min(x, 255))


def log(txt):
    if isinstance(txt, str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (AEONT_ADDON_ID, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)


def prettyprint(string):
    log(simplejson.dumps(string, sort_keys=True, indent=4, separators=(',', ': ')))
