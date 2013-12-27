#!/usr/bin/python
# -*- coding: utf-8 -*-

# With the MindfulClock you turn your device into a Bell of Mindfulness.
# Concept, Design: Marcurs Möller
#                  <marcus.moeller@outlook.com>
#                  <http://apps.microsoft.com/windows/de-de/app/
#                   mindfulclock/58063160-9cc6-4dee-9d92-17df4ce4318a>
# Programming: Andreas Ulrich
#              <ulrich3110@gmail.com>,
#              <http://erasand.jimdo.com/kontakt/>
#
# This file is part of the "MindfulClock".
# "MindfulClock" is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# "MindfulClock" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU General Public License for more details. You should
# have received a copy of the GNU General Public License along with
# "MindfulClock".  If not, see <http://www.gnu.org/licenses/>.


import wx


class Popup(wx.PopupTransientWindow):
    '''mfc1.Popup(parent, style, text, font, colors, icon)

    Show the text notification for the MindfulClock.
    parent = wx.window
    style = wx.SIMPLE_BORDER, wx.RAISED_BORDER, wx.SUNKEN_BORDER,
            wx.NO_BORDER
    text = 'notification text'
    font = (size, 'family', 'style', 'weight')
    colors = (text_color, background_color), colors in html-fomat,
             '#RRGGBB'.
    icon = 'path' to icon for close button

    '''

    def OnDismiss(self):
        self.parent.textnotif = 'close'

    def __init__(self, parent, style, text, font, colors, icon):
        # subclass
        super(Popup, self).__init__(parent, style=style)
        # Set background color.
        if colors[1]:
            self.SetBackgroundColour(colors[1])
        # Text.
        self.caption = wx.StaticText(self, label=text, pos=(10, 10))
        # Set font.
        self.set_font(font)
        # Set text color.
        if colors[0]:
            self.caption.SetForegroundColour(colors[0])
        # Text size.
        tsize = self.caption.GetBestSize()
        # Close button.
        button = wx.BitmapButton(self, bitmap=wx.Bitmap(icon))
        # Bindings
        button.Bind(wx.EVT_BUTTON, self.on_close)
        # Button size and position.
        bsize = button.GetBestSize()
        # w = widgets maximum width.
        if tsize.width > bsize.width:
            # Text is wider than the button.
            w = tsize.width
        else:
            # The button is wider than the text.
            w = bsize.width
        # x, y = button position
        x = (w - bsize.width) / 2
        y = tsize.height + font[0] * 2
        # h = widgets height
        h = y + bsize.height
        # Set button to position.
        button.SetPosition((x, y))
        # Notification size.
        self.size = (w + font[0], h + font[0])
        self.SetSize(self.size)
        # Parent
        self.parent = parent

    def on_close(self, event):
        '''Event for bitmap button.'''
        self.parent.textnotif = 'close'
        self.Show(False)
        self.Destroy()

    def set_font(self, font):
        '''Set the wx.Font from the tuple font to the caption.'''
        # font = (size, 'family', 'style', 'weight')
        familydic = {'decorative': wx.FONTFAMILY_DECORATIVE,
                     'default': wx.FONTFAMILY_DEFAULT,
                     'modern': wx.FONTFAMILY_MODERN,
                     'roman': wx.FONTFAMILY_ROMAN,
                     'script': wx.FONTFAMILY_SCRIPT,
                     'swiss': wx.FONTFAMILY_SWISS,
                     'teletype': wx.FONTFAMILY_TELETYPE}
        styledic = {'normal': wx.NORMAL,
                    'slant': wx.SLANT,
                    'italic': wx.ITALIC}
        weightdic = {'normal': wx.FONTWEIGHT_NORMAL,
                     'light': wx.FONTWEIGHT_LIGHT,
                     'bold': wx.FONTWEIGHT_BOLD}
        textfont = self.caption.GetFont()
        textfont.SetPointSize(font[0])
        textfont.SetFamily(familydic[font[1]])
        textfont.SetStyle(styledic[font[2]])
        textfont.SetWeight(weightdic[font[3]])
        self.caption.SetFont(textfont)


class wxTestFrame(wx.Frame):
    '''wxTestFrame()

    Test object for GUI development.

    '''

    def __init__(self):
        super(wxTestFrame, self).__init__(None)
        self.textnotif = 'not used'
        self.timer = wx.Timer(self, 1)
        self.timer.Start(200)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        wx.FutureCall(millis=100, callable=self.show_popup())
        self.Centre()
        self.Show()

    def on_timer(self, event):
        '''Event, wx.Timer.'''
        if self.textnotif == 'close':
            print('Popup closed.')
            self.timer.Stop()

    def show_popup(self):
        '''Show dialogue.'''
        t = 'Please enter your message ..'
        popup = Popup(parent=self,
                      style=wx.NO_BORDER,
                      text=t,
                      font=(20, 'default', 'italic', 'bold'),
                      colors=(None, None),
                      icon='icons/32/weather-clear.png')
        popw, poph = popup.size
        dispw, disph = wx.GetDisplaySize()
        offx = (dispw - popw) / 2
        offy = (disph - poph) / 2
        popup.Position(ptOrigin=(0, 0), size=(offx, offy))
        popup.Popup()
        #              Test fonts
        #                     'decorative'  'normal'  'normal'
        #                     'default'     'slant'   'light'
        #                     'modern'      'italic'  'bold'
        #                     'roman'
        #                     'script'
        #                     'swiss'
        #                     'teletype'
        # Borders: wx.SIMPLE_BORDER
        #          wx.RAISED_BORDER
        #          wx.SUNKEN_BORDER
        #          wx.NO_BORDER
        # colors=(None, None)
        # colors=('#0000FF', '#FFFF00')


if __name__ == '__main__':
    app = wx.App()
    frame = wxTestFrame()
    app.MainLoop()
