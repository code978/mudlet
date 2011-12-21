import io
import site
import traceback
from PythonQt.mudlet import *
import re
import pprint
from sys import *
import webbrowser

mudlet = MudletObject(HOST_HASH)

def printFixedStackTrace(trace,funcName):
    """Need to modify the stack trace to correspond
     to the lines numbers in the mudlet editor."""
    lines = trace.splitlines()
    lines[0] = 'Python ' + lines[0]
    replace = lines[1].split(',')
    lineno = replace[1].split()[1]
    scripttype = replace[2].split()[1]
    index = -1
    while (scripttype[index].isdigit()):
        index -= 1
    scripttype = scripttype[:index+1]
    replace[1] = ' line ' + str(int(lineno)-3)
    replace[2] = ' in ' + scripttype + ': ' + funcName
    lines[1] = ','.join(replace)
    print '\n'.join(lines)

class NestedDict(dict):
    def __getitem__(self,item):
        try:
            return dict.__getitem__(self,item)
        except KeyError:
            self[item] = type(self)()
            return self[item]
            
class Mapper:
    def __init__(self):
        self.envColors = Mapper.EnvColors()
        self.rooms = Mapper.Rooms()
        self.areaNamesMap = Mapper.AreaNamesMap()
        self.customEnvColors = Mapper.CustomEnvColors()
        self.hashTable = Mapper.HashTable()
        self.mapLabels = Mapper.MapLabels()
        
    class EnvColors(dict):
        def __init__(self):
            super(Mapper.EnvColors,self).__init__()
            for key,value in HOST_ENV_COLORS.iteritems():
                self[ord(key)]=value
            
        def __setitem__(self,key,value):
            super(Mapper.EnvColors,self).__setitem__(key,value)
            
    class Rooms(dict):
        def __init__(self):
            super(Mapper.Rooms,self).__init__()
            for key,value in HOST_ROOMS.iteritems():
                room = {}
                for room_key,room_value in value.iteritems():
                    room[str(room_key)]=room_value
                self[ord(key)]=room
                
    class AreaNamesMap(dict):
        def __init__(self):
            super(Mapper.AreaNamesMap,self).__init__()
            for key,value in HOST_AREA_NAMES_MAP.iteritems():
                self[ord(key)]=value
                
    class CustomEnvColors(dict):
        def __init__(self):
            super(Mapper.CustomEnvColors,self).__init__()
            for key,value in HOST_CUSTOM_ENV_COLORS.iteritems():
                self[ord(key)]=value
                
    class HashTable(dict):
        def __init__(self):
            super(Mapper.HashTable,self).__init__()
            for key,value in HOST_MAP_HASH_TABLE.iteritems():
                self[str(key)]=value
                
    class MapLabels(dict):
        def __init__(self):
            super(Mapper.MapLabels,self).__init__()
            for key,value in HOST_MAP_LABELS.iteritems():
                labelmap = {}
                for map_key,map_value in value.iteritems():
                    label = {}
                    for label_key,label_value in map_value.iteritems():
                        label[str(label_key)] = label_value
                    labelmap[ord(map_key)]=label
                self[ord(key)]=labelmap

line = ''
command = ''
atcp = {}
channel102 = {}
gmcp=NestedDict()
mapper = Mapper()

def onConnect():
    """Run when connection established
        Placeholder, should reimplement in PythonLocal.py"""
    
def onDisconnect():
    """Run on disconnect
        Placeholder, should reimplement in PythonLocal.py"""
    
def handleWindowResizeEvent():
    """Run when window resizes
        Placeholder, should reimplement in PythonLocal.py"""

def send(text,wantPrint=True):
    mudlet.send(text,wantPrint)
    
def expandAlias(text,wantPrint=True):
    mudlet.expandAlias(text,wantPrint)

def selectString(text,pos,console='main'):
    return mudlet.selectString(text,pos,console)
    
def resetFormat(console='main'):
    mudlet.resetFormat(console)

def setBgColor(r,g,b,console='main'): 
    mudlet.setBgColor(r,g,b,console)
    
def setFgColor(r,g,b,console='main'):
    mudlet.setFgColor(r,g,b,console)
    
def bg(color,console='main'):
    code = color_dict[color.strip()]
    setBgColor(code[0],code[1],code[2],console)
    
def fg(color,console='main'):
    code = color_dict[color.strip()]
    setFgColor(code[0],code[1],code[2],console)
    
def enableTimer(timer):
    return mudlet.enableTimer(timer)
    
def enableKey(key):
    return mudlet.enableKey(key)
    
def enableTrigger(trigger):
    return mudlet.enableTrigger(trigger)
    
def enableAlias(alias):
    return mudlet.enableAlias(alias)
    
def disableTimer(timer):
    return mudlet.disableTimer(timer)
    
def disableKey(key):
    return mudlet.disableKey(key)
    
def disableTrigger(trigger):
    return mudlet.disableTrigger(trigger)
    
def disableAlias(alias):
    return mudlet.disableAlias(alias)
    
def selectCaptureGroup(group):
    return mudlet.selectCaptureGroup(group)
    
def replace(text,console='main'):
    mudlet.replace(text,console)

def replaceAll(what,text,console='main'):
    mudlet.replaceAll(what,text,console)
    
def selectSection(col,length,console='main'):
    return mudlet.selectSection(col,length,console)
    
def deleteLine(console='main'):
    mudlet.deleteLine(console)

def reconnect():
    mudlet.reconnect()

def disconnect():
    mudlet.disconnect()
    
def raiseEvent(*arg):
    mudlet.raiseEvent(arg)
    

#Color Table ported from Lua table by Vadim Peretrokin 2009.
color_dict = {
        'snow'                  : (255, 250, 250),
        'ghost_white'           : (248, 248, 255),
        'GhostWhite'            : (248, 248, 255),
        'white_smoke'           : (245, 245, 245),
        'WhiteSmoke'            : (245, 245, 245),
        'gainsboro'             : (220, 220, 220),
        'floral_white'          : (255, 250, 240),
        'FloralWhite'           : (255, 250, 240),
        'old_lace'              : (253, 245, 230),
        'OldLace'               : (253, 245, 230),
        'linen'                 : (250, 240, 230),
        'antique_white'         : (250, 235, 215),
        'AntiqueWhite'          : (250, 235, 215),
        'papaya_whip'           : (255, 239, 213),
        'PapayaWhip'            : (255, 239, 213),
        'blanched_almond'       : (255, 235, 205),
        'BlanchedAlmond'        : (255, 235, 205),
        'bisque'                : (255, 228, 196),
        'peach_puff'            : (255, 218, 185),
        'PeachPuff'             : (255, 218, 185),
        'navajo_white'          : (255, 222, 173),
        'NavajoWhite'           : (255, 222, 173),
        'moccasin'              : (255, 228, 181),
        'cornsilk'              : (255, 248, 220),
        'ivory'                 : (255, 255, 240),
        'lemon_chiffon'         : (255, 250, 205),
        'LemonChiffon'          : (255, 250, 205),
        'seashell'              : (255, 245, 238),
        'honeydew'              : (240, 255, 240),
        'mint_cream'            : (245, 255, 250),
        'MintCream'             : (245, 255, 250),
        'azure'                 : (240, 255, 255),
        'alice_blue'            : (240, 248, 255),
        'AliceBlue'             : (240, 248, 255),
        'lavender'              : (230, 230, 250),
        'lavender_blush'        : (255, 240, 245),
        'LavenderBlush'         : (255, 240, 245),
        'misty_rose'            : (255, 228, 225),
        'MistyRose'             : (255, 228, 225),
        'white'                 : (255, 255, 255),
        'black'                 : (0, 0, 0),
        'dark_slate_gray'       : (47, 79, 79),
        'DarkSlateGray'         : (47, 79, 79),
        'dark_slate_grey'       : (47, 79, 79),
        'DarkSlateGrey'         : (47, 79, 79),
        'dim_gray'              : (105, 105, 105),
        'DimGray'               : (105, 105, 105),
        'dim_grey'              : (105, 105, 105),
        'DimGrey'               : (105, 105, 105),
        'slate_gray'            : (112, 128, 144),
        'SlateGray'             : (112, 128, 144),
        'slate_grey'            : (112, 128, 144),
        'SlateGrey'             : (112, 128, 144),
        'light_slate_gray'      : (119, 136, 153),
        'LightSlateGray'        : (119, 136, 153),
        'light_slate_grey'      : (119, 136, 153),
        'LightSlateGrey'        : (119, 136, 153),
        'gray'                  : (190, 190, 190),
        'grey'                  : (190, 190, 190),
        'light_grey'            : (211, 211, 211),
        'LightGrey'             : (211, 211, 211),
        'light_gray'            : (211, 211, 211),
        'LightGray'             : (211, 211, 211),
        'midnight_blue'         : (25, 25, 112),
        'MidnightBlue'          : (25, 25, 112),
        'navy'                  : (0, 0, 128),
        'navy_blue'             : (0, 0, 128),
        'NavyBlue'              : (0, 0, 128),
        'cornflower_blue'       : (100, 149, 237),
        'CornflowerBlue'        : (100, 149, 237),
        'dark_slate_blue'       : (72, 61, 139),
        'DarkSlateBlue'         : (72, 61, 139),
        'slate_blue'            : (106, 90, 205),
        'SlateBlue'             : (106, 90, 205),
        'medium_slate_blue'     : (123, 104, 238),
        'MediumSlateBlue'       : (123, 104, 238),
        'light_slate_blue'      : (132, 112, 255),
        'LightSlateBlue'        : (132, 112, 255),
        'medium_blue'           : (0, 0, 205),
        'MediumBlue'            : (0, 0, 205),
        'royal_blue'            : (65, 105, 225),
        'RoyalBlue'             : (65, 105, 225),
        'blue'                  : (0, 0, 255),
        'dodger_blue'           : (30, 144, 255),
        'DodgerBlue'            : (30, 144, 255),
        'deep_sky_blue'         : (0, 191, 255),
        'DeepSkyBlue'           : (0, 191, 255),
        'sky_blue'              : (135, 206, 235),
        'SkyBlue'               : (135, 206, 235),
        'light_sky_blue'        : (135, 206, 250),
        'LightSkyBlue'          : (135, 206, 250),
        'steel_blue'            : (70, 130, 180),
        'SteelBlue'             : (70, 130, 180),
        'light_steel_blue'      : (176, 196, 222),
        'LightSteelBlue'        : (176, 196, 222),
        'light_blue'            : (173, 216, 230),
        'LightBlue'             : (173, 216, 230),
        'powder_blue'           : (176, 224, 230),
        'PowderBlue'            : (176, 224, 230),
        'pale_turquoise'        : (175, 238, 238),
        'PaleTurquoise'         : (175, 238, 238),
        'dark_turquoise'        : (0, 206, 209),
        'DarkTurquoise'         : (0, 206, 209),
        'medium_turquoise'      : (72, 209, 204),
        'MediumTurquoise'       : (72, 209, 204),
        'turquoise'             : (64, 224, 208),
        'cyan'                  : (0, 255, 255),
        'light_cyan'            : (224, 255, 255),
        'LightCyan'             : (224, 255, 255),
        'cadet_blue'            : (95, 158, 160),
        'CadetBlue'             : (95, 158, 160),
        'medium_aquamarine'     : (102, 205, 170),
        'MediumAquamarine'      : (102, 205, 170),
        'aquamarine'            : (127, 255, 212),
        'dark_green'            : (0, 100, 0),
        'DarkGreen'             : (0, 100, 0),
        'dark_olive_green'      : (85, 107, 47),
        'DarkOliveGreen'        : (85, 107, 47),
        'dark_sea_green'        : (143, 188, 143),
        'DarkSeaGreen'          : (143, 188, 143),
        'sea_green'             : (46, 139, 87),
        'SeaGreen'              : (46, 139, 87),
        'medium_sea_green'      : (60, 179, 113),
        'MediumSeaGreen'        : (60, 179, 113),
        'light_sea_green'       : (32, 178, 170),
        'LightSeaGreen'         : (32, 178, 170),
        'pale_green'            : (152, 251, 152),
        'PaleGreen'             : (152, 251, 152),
        'spring_green'          : (0, 255, 127),
        'SpringGreen'           : (0, 255, 127),
        'lawn_green'            : (124, 252, 0),
        'LawnGreen'             : (124, 252, 0),
        'green'                 : (0, 255, 0),
        'chartreuse'            : (127, 255, 0),
        'medium_spring_green'   : (0, 250, 154),
        'MediumSpringGreen'     : (0, 250, 154),
        'green_yellow'          : (173, 255, 47),
        'GreenYellow'           : (173, 255, 47),
        'lime_green'            : (50, 205, 50),
        'LimeGreen'             : (50, 205, 50),
        'yellow_green'          : (154, 205, 50),
        'YellowGreen'           : (154, 205, 50),
        'forest_green'          : (34, 139, 34),
        'ForestGreen'           : (34, 139, 34),
        'olive_drab'            : (107, 142, 35),
        'OliveDrab'             : (107, 142, 35),
        'dark_khaki'            : (189, 183, 107),
        'DarkKhaki'             : (189, 183, 107),
        'khaki'                 : (240, 230, 140),
        'pale_goldenrod'        : (238, 232, 170),
        'PaleGoldenrod'         : (238, 232, 170),
        'light_goldenrod_yellow': (250, 250, 210),
        'LightGoldenrodYellow'  : (250, 250, 210),
        'light_yellow'          : (255, 255, 224),
        'LightYellow'           : (255, 255, 224),
        'yellow'                : (255, 255, 0),
        'gold'                  : (255, 215, 0),
        'light_goldenrod'       : (238, 221, 130),
        'LightGoldenrod'        : (238, 221, 130),
        'goldenrod'             : (218, 165, 32),
        'dark_goldenrod'        : (184, 134, 11),
        'DarkGoldenrod'         : (184, 134, 11),
        'rosy_brown'            : (188, 143, 143),
        'RosyBrown'             : (188, 143, 143),
        'indian_red'            : (205, 92, 92),
        'IndianRed'             : (205, 92, 92),
        'saddle_brown'          : (139, 69, 19),
        'SaddleBrown'           : (139, 69, 19),
        'sienna'                : (160, 82, 45),
        'peru'                  : (205, 133, 63),
        'burlywood'             : (222, 184, 135),
        'beige'                 : (245, 245, 220),
        'wheat'                 : (245, 222, 179),
        'sandy_brown'           : (244, 164, 96),
        'SandyBrown'            : (244, 164, 96),
        'tan'                   : (210, 180, 140),
        'chocolate'             : (210, 105, 30),
        'firebrick'             : (178, 34, 34),
        'brown'                 : (165, 42, 42),
        'dark_salmon'           : (233, 150, 122),
        'DarkSalmon'            : (233, 150, 122),
        'salmon'                : (250, 128, 114),
        'light_salmon'          : (255, 160, 122),
        'LightSalmon'           : (255, 160, 122),
        'orange'                : (255, 165, 0),
        'dark_orange'           : (255, 140, 0),
        'DarkOrange'            : (255, 140, 0),
        'coral'                 : (255, 127, 80),
        'light_coral'           : (240, 128, 128),
        'LightCoral'            : (240, 128, 128),
        'tomato'                : (255, 99, 71),
        'orange_red'            : (255, 69, 0),
        'OrangeRed'             : (255, 69, 0),
        'red'                   : (255, 0, 0),
        'hot_pink'              : (255, 105, 180),
        'HotPink'               : (255, 105, 180),
        'deep_pink'             : (255, 20, 147),
        'DeepPink'              : (255, 20, 147),
        'pink'                  : (255, 192, 203),
        'light_pink'            : (255, 182, 193),
        'LightPink'             : (255, 182, 193),
        'pale_violet_red'       : (219, 112, 147),
        'PaleVioletRed'         : (219, 112, 147),
        'maroon'                : (176, 48, 96),
        'medium_violet_red'     : (199, 21, 133),
        'MediumVioletRed'       : (199, 21, 133),
        'violet_red'            : (208, 32, 144),
        'VioletRed'             : (208, 32, 144),
        'magenta'               : (255, 0, 255),
        'violet'                : (238, 130, 238),
        'plum'                  : (221, 160, 221),
        'orchid'                : (218, 112, 214),
        'medium_orchid'         : (186, 85, 211),
        'MediumOrchid'          : (186, 85, 211),
        'dark_orchid'           : (153, 50, 204),
        'DarkOrchid'            : (153, 50, 204),
        'dark_violet'           : (148, 0, 211),
        'DarkViolet'            : (148, 0, 211),
        'blue_violet'           : (138, 43, 226),
        'BlueViolet'            : (138, 43, 226),
        'purple'                : (160, 32, 240),
        'medium_purple'         : (147, 112, 219),
        'MediumPurple'          : (147, 112, 219),
        'thistle'               : (216, 191, 216)
}

# Functions added by KrimMalak.

defaultbrowser="Unselected" #Placing here till I figure out how to make it a Mudlet variable a user can set.

def deselect():
    selectString("",1)
    
def replaceLine(what):
    '''Does not use insertText like Lua version, but seems to work fine.'''
    selectString(line, 1)
    replace(what)

def openUrl(url):
    """This can use some further expanding, but not up to adding stuff to the Settings menu yet.
       Basically, on my version of Ubuntu I had to explicitly state the browser I wanted.  Would be nice to
       be able what brower the user wanted to use.  This link lists browsers Python understands to look for: 
       http://www.python.org/doc//current/library/webbrowser.html#module-webbrowser
       Status: Functioning"""

    global defaultbrowser
    if defaultbrowser=="Unselected":
        defaultbrowser='firefox'
    browser=webbrowser.get(defaultbrowser)
    browser.open_new_tab(url)

def sendAll(commands):
    """Commands need to be passed as a list or tuple.  Status: Complete"""
    for x in commands:
        send(x)


def display(obj):
    pprint.pprint(obj,width=60)


def cecho(text,consule='main',insert=False):
    text=re.split("(<.*?>)",text)
    for line in text:
        if re.match("<(.*?)>",line):
            match=re.match("<(.*?)>",line)
            if ',' in match.group(1):
                split_match=match.group(1).split(',')
                if split_match[0] != '' and split_match[0] in color_dict:
                    fg(split_match[0],consule)
                if split_match[1] != '' and split_match[1] in color_dict:
                    bg(split_match[1],consule)
            elif match.group(1) in color_dict:
                fg(match.group(1),consule)
        else:
            if insert==False: 
		echo(line,consule) 
	    else: 
		insertText(line,consule)
    resetFormat()

def decho(text,consule='main',insert=False):
    text=re.split("(<.*?>)",text)
    for line in text:
        if re.match("<(.*?)>",line):
            match=re.match("<(.*?)>",line)
            if ':' in match.group(1):
                split_match=match.group(1).split(':')
                if split_match[0] != '':
                    codes=split_match[0].split(',')
                    setFgColor(int(codes[0]), int(codes[1]),int(codes[2]),consule)
                if split_match[1] != '':
                    codes=split_match[1].split(',')
                    setBgColor(int(codes[0]), int(codes[1]),int(codes[2]),consule)
            else:
                codes=match.group(1).split(',')
                setFgColor(int(codes[0]), int(codes[1]),int(codes[2]),consule)
        else:
            if insert==False: 
                echo(line,consule) 
            else: 
                insertText(line,consule)
    resetFormat()

def hecho(text,consule='main',insert=False):
    text=re.split("(\|c\w{6},\w{6}|\|c\w{6})",text)
    for line in text:
        if re.match("\|c\w{6},\w{6}|\|c\w{6}",line):
            m=re.match("(\|c\w{6},\w{6}|\|c\w{6})",line)
            if ',' in m.group(1):
                split_match=m.group(1).split(',')
                if split_match[0] != '':
                    codes=split_match[0]
                    codes=codes[2:4],codes[4:6],codes[6:8]
                    setFgColor(int(codes[0],16), int(codes[1],16),int(codes[2],16),consule)
                if split_match[1] != '':
                    codes=split_match[1]
                    codes=codes[0:2],codes[2:4],codes[4:6]
                    setBgColor(int(codes[0],16), int(codes[1],16),int(codes[2],16),consule)
            else:
                codes=m.group(1)
                codes=codes[2:4],codes[4:6],codes[6:8]
                setFgColor(int(codes[0],16), int(codes[1],16),int(codes[2],16),consule)
        else:
            if insert==False: 
                echo(line,consule) 
            else: 
                insertText(line,consule)
    resetFormat()


def replaceWildcard(what, replacement):
    selectCaptureGroup(what)
    replace(replacement)
    
def RGB2Hex(red, green, blue):
    _hex=hex(red)[2:]+hex(green)[2:]+hex(blue)[2:]
    print _hex

def showColors(wide=3):
    pos=1
    for k in color_dict.keys():
        v=color_dict[k]
        lum = (0.2126 * ((float(v[0])/255)**2.2)) + (0.7152 * ((float(v[1])/255)**2.2)) + (0.0722 * ((float(v[2])/255)**2.2))
        if lum > 0.5:
            fg="black"
        else:
            fg="white"
        if pos==wide:
            cecho("<"+fg+","+k+">"+k+" "*(23-len(k))+"<,black>  \n")
            pos=1
        else:
            cecho("<"+fg+","+k+">"+k+" "*(23-len(k))+"<,black>  ")
            pos=pos+1

def sendGMCP(msg):
    mudlet.sendGMCP(msg)

def sendATCP(msg):
    mudlet.sendATCP(msg)

def sendTelnetChannel102(msg):
    mudlet.sendTelnetChannel102(msg)

def sendIrc(channel, msg):
    mudlet.sendIrc(channel, msg)

def echo(txt, consule='main'):
    mudlet.echo(txt, consule)

def echoLink(txt, func, hint, consule='main', customFormat=False):
    mudlet.echoLink(txt, func, hint, consule, customFormat)

def insertLink(txt, func, hint, consule='main', customFormat=False):
    mudlet.insertLink(txt, func, hint, consule, customFormat)

def setLink(func, hint, consule='main'):
    mudlet.setLink(func, hint, consule)

def echoPopup(txt, func, hint, consule='main', customFormat=False):
    mudlet.echoPopup(txt, func, hint, consule, customFormat)

def setPopup(func,hint,consule='main'):
    mudlet.setPopup(func,hint,consule)

def insertPopup(txt, func, hint, consule='main'):
    mudlet.insertPopup(txt, func, hint, consule)

def createBuffer(name):
    mudlet.createBuffer(name)

def appendBuffer(console='main'):
    mudlet.appendBuffer(console)

def getLineNumber():
    return mudlet.getLineNumber()

def copy(console='main'):
    mudlet.copy(console)

def paste(console='main'):
    mudlet.paste(console)

def cut():
    mudlet.cut()

def feedTriggers(txt):
    mudlet.feedTriggers(txt)

def setBold(doBold,consule='main'):
    """Consule=The consule you want to set, doBold=True/False for setting
       bold on or off."""
    mudlet.setBold(consule,active)

def setUnderline(doUnderline,consule='main'):
    """Consule=The consule you want to set, doUnderline=True/False for setting
       Underline on or off."""
    mudlet.setUnderline(consule,active)

def setItalics(doItalics,consule='main'):
    """Consule=The consule you want to set, doItalics=True/False for setting
       Italics on or off."""
    mudlet.setItalics(consule,active)

def moveCursor(xpos, ypos, consule='main'):
    mudlet.moveCursor(xpos,ypos,consule)

def moveCursorEnd(consule='main'):
    mudlet.moveCursorEnd(consule)

def pasteWindow(consule='main'):
    mudlet.pasteWindow(consule)

def selectCurrentLine(consule='main'):
    mudlet.selectCurrentLine(consule)

def wrapLine(linenum, consule='main'):
    mudlet.wrapLine(linenum, consule)

def getFgColor(consule='main'):
    return mudlet.getFgColor(consule)

def getBgColor(consule='main'):
    return mudlet.getBgColor(consule)

def insertHTML(txt):
    mudlet.insertHTML(txt)

def insertText(txt,consule='main'):
    mudlet.insertText(txt, consule)

def isAnsiFgColor(color, consule='main'):
    return mudlet.isAnsiFgColor(color, consule)

def isAnsiBgColor(color, consule='main'):
    return mudlet.isAnsiBgColor(color, consule)
    
def getRGB(color):
    code = color_dict[color.strip()]
    return code

def getCurrentLine(consule='main'):
    return mudlet.getCurrentLine(consule)
    
def appendCmdLine(txt):
    mudlet.appendCmdLine(txt)
    
def denyCurrentSend():
    mudlet.denyCurrentSend()
    
def getLastLineNumber(console='main'):
    return mudlet.getLastLineNumber(console)
    
def getLineCount(console='main'):
    return mudlet.getLineCount(console)

def prefix(what, func="None", fg="", bg="", console='main'):
    moveCursor(0,getLineNumber(), console)
    if func=="None":
        insertText(what,console)
    elif func=='cecho':
        cecho("<"+fg+","+bg+">"+what,console,insert=True)
    elif func=='decho':
        decho("<"+str(fg[0])+","+str(fg[1])+","+str(fg[2])+":"+str(bg[0])+","+str(bg[1])+","+str(bg[2])+">"+what,console,insert=True)
    elif func=='hecho':
        hecho("|c"+fg+","+bg+what,console,insert=True)

def suffix(what, func="None", fg="", bg="", console='main'):
    length = len(line)
    moveCursor(length, getLineNumber(), console)
    if func=="None":
        insertText(what,console)
    elif func=='cecho':
        cecho("<"+fg+","+bg+">"+what,console,insert=True)
    elif func=='decho':
        decho("<"+str(fg[0])+","+str(fg[1])+","+str(fg[2])+":"+str(bg[0])+","+str(bg[1])+","+str(bg[2])+">"+what,console,insert=True)
    elif func=='hecho':
        hecho("|c"+fg+","+bg+what,console,insert=True)

def getLines(From,To):
    return mudlet.getLines(From,To)

def getTime(return_string,fmt="yyyy.MM.dd hh:mm:ss.zzz"):
    if return_string==True:
	time=mudlet.getTime(return_string,fmt)[0]
	time=str(time)
        return time
    else:
	time=dict(zip(("hour","min",'sec','msec','year','month','day'),mudlet.getTime(return_string,fmt)))
        return time

def getTimeStamp(line,console='main'):
    return mudlet.getTimeStamp(line,console)

def isPrompt():
    return mudlet.isPrompt()

def startLogging(logOn):
    mudlet.startLogging(logOn)

def isActive(obj, objType):
    return mudlet.isActive(obj,objType)

def killAlias(obj):
    return mudlet.killAlias(obj)

def killTrigger(obj):
    return mudlet.killTrigger(obj)

def killTimer(obj):
    return mudlet.killTimer(obj)

def exists(obj, objType):
    return mudlet.exists(obj, objType)

def setTriggerStayOpen(name,numOfLines):
    mudlet.setTriggerStayOpen(name,numOfLines)

def showMultimatches():
    echo("\n-------------------------------------------------------");
    echo("\nThe table multimatches[n][m] contains:");
    echo("\n-------------------------------------------------------");
    for i in range(0,len(multimatches)):
        echo("\nregex " + str(i) + " captured: (multimatches["+ str(i) +"][1-n])");
        for i2 in range(0,len(multimatches[i])):
                echo("\n          key="+str(i2)+" value="+multimatches[i][i2]);
    echo("\n-------------------------------------------------------\n");

def createStopWatch():
    return mudlet.createStopWatch()

def stopStopWatch( ID ):
    return mudlet.stopStopWatch( ID )

def startStopWatch( ID ):
    return mudlet.startStopWatch( ID )

def resetStopWatch( ID ):
    return mudlet.startStopWatch( ID )

def getStopWatchTime( ID ):
    return mudlet.getStopWatchTime( ID )

def getMudletHomeDir():
    return mudlet.getMudletHomeDir()

def getNetworkLatency():
    return mudlet.getNetworkLatency()

def resetProfile():
    mudlet.resetProfile()

def connectToServer(port, url):
    mudlet.connectToServer(port, url)

def downloadFile(path, url):
    mudlet.downloadFile(path, url)

def invokeFileDialog(directory, title):
    return mudlet.invokeFileDialog(directory, title)

def loadRawFile(the_file):
    mudlet.loadRawFile(the_file)

def playSoundFile(sound):
    mudlet.playSoundFile(sound)

def sendSocket(txt):
    mudlet.sendSocket(txt)

def permTimer(name,folder,time,func):
    return mudlet.startPermTimer(name,folder,time,func)

def tempBeginOfLineTrigger(regex,func):
    return mudlet.startTempBeginOfLineTrigger(regex,func)

def tempTimer(time, func):
    return mudlet.startTempTimer(time, func)

def permAlias(name,folder,regex,func):
    return mudlet.startPermAlias(name,folder,regex,func)

def tempAlias(regex,func):
    return mudlet.startTempAlias(regex,func)

def tempExactMatchTrigger(regex,func):
    return mudlet.startTempExactMatchTrigger(regex,func)

def tempTrigger(regex,func):
    return mudlet.startTempTrigger(regex,func)

def tempLineTrigger(_from, howmany, func):
    return mudlet.startTempLineTrigger(_from, howmany, func)

def tempColorTrigger(fg, bg, func):
    return mudlet.startTempColorTrigger(fg, bg, func)

def permRegexTrigger(name,folder,regexlist,func):
    return mudlet.startPermRegexTrigger(name,folder,regexlist,func)

def permSubstringTrigger(name,folder,regexlist,func):
    return mudlet.startPermSubstringTrigger(name,folder,regexlist,func)

def permBeginOfLineStringTrigger(name,folder,regexlist,func):
    return mudlet.startPermBeginOfLineStringTrigger(name,folder,regexlist,func)

execfile('PythonLocal.py')
