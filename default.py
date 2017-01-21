import sys
import os
import xbmc
import xbmcgui
import xbmcaddon

AEONT_ADDON = xbmcaddon.Addon()
AEONT_ADDON_VERSION = AEONT_ADDON.getAddonInfo('version')
AEONT_ADDON_LANGUAGE = AEONT_ADDON.getLocalizedString
AEONT_ADDON_PATH = AEONT_ADDON.getAddonInfo('path').decode("utf-8")
AEONT_ADDON_ID = AEONT_ADDON.getAddonInfo('id')
AEONT_ADDON_DATA_PATH = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % AEONT_ADDON_ID))
HOME = xbmcgui.Window(10000)
sys.path.append(xbmc.translatePath(os.path.join(AEONT_ADDON_PATH, 'resources', 'lib')))

from Utils import *


class Aeon_Tools_Main:

    def __init__(self):
        log("version %s started" % AEONT_ADDON_VERSION)
        self._init_vars()
        self._parse_argv()
        if not xbmcvfs.exists(AEONT_ADDON_DATA_PATH):
            # addon data path does not exist...create it
            xbmcvfs.mkdir(AEONT_ADDON_DATA_PATH)
        if self.infos:
            self._StartInfoActions()
        if self.control == "plugin":
            xbmcplugin.endOfDirectory(self.handle)
        while self.daemon and not xbmc.abortRequested:
            if not HOME.getProperty("cpa_aeon_set") == 'none':
                self.aeont_image_now_cpa = xbmc.getInfoLabel("Control.GetLabel(7978)")
                if self.aeont_image_now_cpa == '' and HOME.getProperty("cpa_aeon_fallback") != '':
                    self.aeont_image_now_cpa = HOME.getProperty("cpa_aeon_fallback")
                if self.aeont_image_now_cpa != self.aeont_image_prev_cpa:
                    try:
                        self.aeont_image_prev_cpa = self.aeont_image_now_cpa
                        HOME.setProperty("aeon_tools_OldColorcpa", HOME.getProperty("aeon_tools_Colorcpa"))
                        HOME.setProperty("aeon_tools_OldCColorcpa", HOME.getProperty("aeon_tools_CColorcpa"))
                        HOME.setProperty('aeon_tools_7978ImageUpdating', '0')
                        if HOME.getProperty("cpa_aeon_set") == 'overall_color':
                            imagecolor = Overall_Color(self.aeont_image_now_cpa)
                            HOME.setProperty("aeon_tools_Colorcpa", imagecolor)
                            HOME.setProperty("aeon_tools_CColorcpa", Complementary_Color(imagecolor))
                        elif HOME.getProperty("cpa_aeon_set") == 'frequent_color':
                            imagecolor = Frequent_Color(self.aeont_image_now_cpa)
                            HOME.setProperty("aeon_tools_Colorcpa", imagecolor)
                            HOME.setProperty("aeon_tools_CColorcpa", Complementary_Color(imagecolor))
                        HOME.setProperty('aeon_tools_7978ImageUpdating', '1')
                    except:
                        HOME.setProperty('aeon_tools_7978ImageUpdating', '1')
                        log("Could not process image for cpa daemon")
            if not HOME.getProperty("cfa_aeon_set") == 'none':
                self.aeont_image_now_cfa = xbmc.getInfoLabel("Control.GetLabel(7977)")
                if self.aeont_image_now_cfa != self.aeont_image_prev_cfa:
                    try:
                        self.aeont_image_prev_cfa = self.aeont_image_now_cfa
                        HOME.setProperty("aeon_tools_OldColorcfa", HOME.getProperty("aeon_tools_Colorcfa"))
                        HOME.setProperty("aeon_tools_OldCColorcfa", HOME.getProperty("aeon_tools_CColorcfa"))
                        HOME.setProperty('aeon_tools_7977ImageUpdating', '0')
                        if HOME.getProperty("cfa_aeon_set") == 'overall_color':
                            imagecolor = Overall_Color(self.aeont_image_now_cfa)
                            HOME.setProperty("aeon_tools_Colorcfa", imagecolor)
                            HOME.setProperty("aeon_tools_CColorcfa", Complementary_Color(imagecolor))
                        elif HOME.getProperty("cfa_aeon_set") == 'frequent_color':
                            imagecolor = Frequent_Color(self.aeont_image_now_cfa)
                            HOME.setProperty("aeon_tools_Colorcfa", imagecolor)
                            HOME.setProperty("aeon_tools_CColorcfa", Complementary_Color(imagecolor))
                        HOME.setProperty('aeon_tools_7977ImageUpdating', '1')
                    except:
                        HOME.setProperty('aeon_tools_7977ImageUpdating', '1')
                        log("Could not process image for cfa daemon")
            self.aeont_image_now = xbmc.getInfoLabel("Player.Art(thumb)")
            self.aeont_image_now_fa = xbmc.getInfoLabel("MusicPlayer.Property(Fanart_Image)")
            if self.aeont_image_now != self.aeont_image_prev and xbmc.Player().isPlayingAudio():
                try:
                    self.aeont_image_prev = self.aeont_image_now
                    imagecolor = Overall_Color(self.aeont_image_now)
                    HOME.setProperty("ImageColor1", imagecolor)
                except:
                    log("Could not process image for f daemon")
            if self.aeont_image_now_fa != self.aeont_image_prev_fa and xbmc.Player().isPlayingAudio():
                try:
                    self.aeont_image_prev_fa = self.aeont_image_now_fa
                    imagecolor = Overall_Color(self.aeont_image_now_fa)
                    HOME.setProperty("ImageColorfa1", imagecolor)
                except:
                    log("Could not process image for fa daemon")
            xbmc.sleep(300)

    def _StartInfoActions(self):
        HOME.setProperty(self.prefix + 'aeon_tools_ImageUpdating', '0')
        for info in self.infos:
            if info == 'overall_color':
                HOME.setProperty(self.prefix + "ImageOldColor", HOME.getProperty(self.prefix + "ImageOldColor"))
                HOME.setProperty(self.prefix + "ImageOldCColor", HOME.getProperty(self.prefix + "ImageOldCColor"))
                imagecolor = Overall_Color(self.id)
                HOME.setProperty(self.prefix + "ImageColor", imagecolor)
                HOME.setProperty(self.prefix + "ImageCColor", Complementary_Color(imagecolor))
            elif info == 'frequent_color':
                HOME.setProperty(self.prefix + "ImageOldColor", HOME.getProperty(self.prefix + "ImageOldColor"))
                HOME.setProperty(self.prefix + "ImageOldCColor", HOME.getProperty(self.prefix + "ImageOldCColor"))
                imagecolor = Frequent_Color(self.id)
                HOME.setProperty(self.prefix + "ImageColor", imagecolor)
                HOME.setProperty(self.prefix + "ImageCColor", Complementary_Color(imagecolor))
        HOME.setProperty(self.prefix + 'aeon_tools_ImageUpdating', '1')

    def _init_vars(self):
        self.window = xbmcgui.Window(10000)  # Home Window
        self.control = None
        self.infos = []
        self.id = ""
        self.dbid = ""
        self.prefix = ""
        self.daemon = False
        self.aeont_image_now = ""
        self.aeont_image_now_fa = ""
        self.aeont_image_now_cfa = ""
        self.aeont_image_now_cpa = ""
        self.aeont_image_prev = ""
        self.aeont_image_prev_fa = ""
        self.aeont_image_prev_cfa = ""
        self.aeont_image_prev_cpa = ""
        self.autoclose = ""

    def _parse_argv(self):
        args = sys.argv
        for arg in args:
            arg = arg.replace("'\"", "").replace("\"'", "")
            if arg == 'script.aeon.tools':
                continue
            elif arg.startswith('daemon='):
                self.daemon = True
            elif arg.startswith('prefix='):
                self.prefix = arg[7:]
                if not self.prefix.endswith("."):
                    self.prefix = self.prefix + "."
            elif arg.startswith('container='):
                self.container = RemoveQuotes(arg[10:])

class Aeon_Tools_Monitor(xbmc.Monitor):

    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onPlayBackStarted(self):
        pass


if __name__ == "__main__":
    Aeon_Tools_Main()
log('finished')
