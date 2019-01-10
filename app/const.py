#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018
https://stackoverflow.com/questions/2682745/how-do-i-create-a-constant-in-python
"""

class MetaConst(type):
    def __getattr__(cls, key):
        return cls[key]

    def __setattr__(cls, key, value):
        raise TypeError


class Const(object, metaclass=MetaConst):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        raise TypeError


class APP(Const):

    NOTICE_NRM = "NORMAL"
    NOTICE_ERR = "ERROR"
    NOTICE_WRN = "WARN"


class TMI_CHANNEL(Const):

    STATE_UNKNOWN = "STATE_UNKNOWN"
    STATE_READY = "STATE_READY"
    STATE_RUNNING = "STATE_RUNNING"
    STATE_STEPPING = "STATE_STEPPING"
    STATE_PAUSE = "STATE_PAUSE"
    STATE_ENDING = "STATE_ENDING"
    STATE_DONE = "STATE_DONE"
    STATE_INTERNAL_CRASH = "STATE_CRASH"  # TODO:

    EVENT_TYPE_INIT = "EVENT_TYPE_INIT"
    EVENT_TYPE_START = "EVENT_TYPE_START"
    EVENT_TYPE_RUN = "EVENT_TYPE_RUN"
    EVENT_TYPE_STEP = "EVENT_TYPE_STEP"
    EVENT_TYPE_RUN_ITEM_DONE = "EVENT_TYPE_RUN_ITEM_DONE"
    EVENT_TYPE_SKIP = "EVENT_TYPE_SKIP"
    EVENT_TYPE_REWIND = "EVENT_TYPE_REWIND"
    EVENT_TYPE_PAUSE = "EVENT_TYPE_PAUSE"
    EVENT_TYPE_ENDING = "EVENT_TYPE_ENDING"
    EVENT_TYPE_DONE = "EVENT_TYPE_DONE"
    EVENT_TYPE_CRASH = "EVENT_TYPE_CRASH"

    EVENT_THREAD_STOP = "EVENT_THREAD_STOP"

    GUI_TYPE_RESPONSE = "GUI_TYPE_RESPONSE"


class TMI_PUB(Const):

    TMI_SHUTDOWN         = "TMIShutdown"

    TMI_CHANNELS         = "tmi_ch_root"

    TMI_CHANNELS_SCRIPT  = TMI_CHANNELS + ".script"  # a new script is loaded

    TMI_FRAME            = "TMIFrame"
    TMI_FRAME_STATUSLINE_RESULT_SERVER = TMI_FRAME + ".result_server"
    TMI_FRAME_SYSTEM_NOTICE = TMI_FRAME + ".system_notice"                 # {"notice": <msg>, ["toolbar": T/F,] "from": [msg]}
    TMI_FRAME_SYSTEM_NOTICE_DIALOG = TMI_FRAME + ".system_notice_dialog"
    TMI_FRAME_SYSTEM_NOTICE_TOOLBAREN = TMI_FRAME + ".toolbar_enable"

    TMI_CHANNELS_PLAY    = TMI_CHANNELS + ".play"
    TMI_CHANNELS_STEP    = TMI_CHANNELS + ".step"
    TMI_CHANNELS_STOP    = TMI_CHANNELS + ".stop"
    TMI_CHANNELS_PAUSE   = TMI_CHANNELS + ".pause"
    TMI_CHANNELS_FF      = TMI_CHANNELS + ".ff"      # skip ahead one
    TMI_CHANNELS_REWIND  = TMI_CHANNELS + ".rewind"  # go back one

    TMI_CHANNEL_STATE    = TMI_CHANNELS + ".state" # from TMIChanCon
                           # {"ch": #, "state": <state>, "from": 'TMIChanCon'}

    TMI_CHANNEL_RESULT       = TMI_CHANNELS + ".result" # from TMIChanCon
    TMI_CHANNEL_RESULT_CRASH = TMI_CHANNELS + ".result_crash"  # from TMIChanCon  TODO
    TMI_CHANNEL_VIEW_RESULT  = TMI_CHANNELS + ".view_result"

    TMI_CHANNEL_0         = TMI_CHANNELS + ".0"
    TMI_CHANNEL_0_BUTTON  = TMI_CHANNEL_0 + ".button" # from TMIChannel gui to TMIChannelController, test_suite_class
    TMI_CHANNEL_0_TEXTBOX = TMI_CHANNEL_0 + ".textbox" # from TMIChannel gui to TMIChannelController, test_suite_class
    TMI_CHANNEL_0_TOOL    = TMI_CHANNEL_0 + ".tool"   # from TMIChannel gui to TMIChannelController, test_suite_class
    TMI_CHANNEL_0_PLAY    = TMI_CHANNEL_0 + ".play"   # play this channel

    TMI_CHANNEL_1         = TMI_CHANNELS + ".1"
    TMI_CHANNEL_1_BUTTON  = TMI_CHANNEL_1 + ".button"
    TMI_CHANNEL_1_TEXTBOX = TMI_CHANNEL_1 + ".textbox"
    TMI_CHANNEL_1_TOOL    = TMI_CHANNEL_1 + ".tool"
    TMI_CHANNEL_1_PLAY    = TMI_CHANNEL_0 + ".play"   # play this channel

    TMI_CHANNEL_2         = TMI_CHANNELS + ".2"
    TMI_CHANNEL_2_BUTTON  = TMI_CHANNEL_2 + ".button"
    TMI_CHANNEL_2_TEXTBOX = TMI_CHANNEL_2 + ".textbox"
    TMI_CHANNEL_2_TOOL    = TMI_CHANNEL_2 + ".tool"
    TMI_CHANNEL_2_PLAY    = TMI_CHANNEL_0 + ".play"   # play this channel

    TMI_CHANNEL_3         = TMI_CHANNELS + ".3"
    TMI_CHANNEL_3_BUTTON  = TMI_CHANNEL_3 + ".button"
    TMI_CHANNEL_3_TEXTBOX = TMI_CHANNEL_3 + ".textbox"
    TMI_CHANNEL_3_TOOL    = TMI_CHANNEL_3 + ".tool"
    TMI_CHANNEL_3_PLAY    = TMI_CHANNEL_0 + ".play"   # play this channel

    TMI_CHANNEL_4         = TMI_CHANNELS + ".4"
    TMI_CHANNEL_4_BUTTON  = TMI_CHANNEL_4 + ".button"
    TMI_CHANNEL_4_TEXTBOX = TMI_CHANNEL_4 + ".textbox"
    TMI_CHANNEL_4_TOOL    = TMI_CHANNEL_4 + ".tool"
    TMI_CHANNEL_4_PLAY    = TMI_CHANNEL_0 + ".play"   # play this channel

    TMI_CHANNEL_5         = TMI_CHANNELS + ".5"
    TMI_CHANNEL_5_BUTTON  = TMI_CHANNEL_5 + ".button"
    TMI_CHANNEL_5_TEXTBOX = TMI_CHANNEL_5 + ".textbox"
    TMI_CHANNEL_5_TOOL    = TMI_CHANNEL_5 + ".tool"
    TMI_CHANNEL_5_PLAY    = TMI_CHANNEL_0 + ".play"   # play this channel

    TMI_CHANNEL_6         = TMI_CHANNELS + ".6"
    TMI_CHANNEL_6_BUTTON  = TMI_CHANNEL_6 + ".button"
    TMI_CHANNEL_6_TEXTBOX = TMI_CHANNEL_6 + ".textbox"
    TMI_CHANNEL_6_TOOL    = TMI_CHANNEL_6 + ".tool"
    TMI_CHANNEL_6_PLAY    = TMI_CHANNEL_0 + ".play"   # play this channel

    TMI_CHANNEL_7         = TMI_CHANNELS + ".7"
    TMI_CHANNEL_7_BUTTON  = TMI_CHANNEL_7 + ".button"
    TMI_CHANNEL_7_TEXTBOX = TMI_CHANNEL_7 + ".textbox"
    TMI_CHANNEL_7_TOOL    = TMI_CHANNEL_7 + ".tool"
    TMI_CHANNEL_7_PLAY    = TMI_CHANNEL_0 + ".play"   # play this channel

    @staticmethod
    def get_tmi_channel_num_button(num):
        return getattr(TMI_PUB, "TMI_CHANNEL_{}_BUTTON".format(num))

    @staticmethod
    def get_tmi_channel_num_textbox(num):
        return getattr(TMI_PUB, "TMI_CHANNEL_{}_TEXTBOX".format(num))

    @staticmethod
    def get_tmi_channel_num_play(num):
        return getattr(TMI_PUB, "TMI_CHANNEL_{}_PLAY".format(num))
