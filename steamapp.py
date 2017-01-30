from __future__ import with_statement
import mechanize
import BeautifulSoup as bs4
import string
import re
import os
import time
from time import gmtime, strftime
import model_v2
import config
import csv
import lxml
import urllib2 #Need this for avatar retrieval - Mechanize can't open the url for some reason... *Sigh*

# import simplejson as json

def steam_db_init():
    # Initialize mechanize
    br = mechanize.Browser()

    gametitlelist=[]
    hdvaluelist=[]
    hdunitlist=[]
    uspricelist=[]
    apptypelist=[]
    iconlist=[]
    multilist=[]
    winlist=[]
    maclist=[]
    linuxlist=[]
    joylist=[]
    mclist=[]

    errorlog = []

    # Get User Game List
    # json_get_steamID64 = json.load(urllib2.build_opener().open(urllib2.Request('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key='+config.API_KEY+'&format=json&vanityurl='+steam_user)))
    try:
        page = br.open('http://steamcommunity.com/id/'+steam_user+'/games?tab=all&xml=1', 'xml')
        dom = bs4.BeautifulSoup(page)
        if dom.find('error'):
            page = br.open('http://steamcommunity.com/profiles/'+steam_user+'/games?tab=all&xml=1', 'xml')
            dom = bs4.BeautifulSoup(page)
            if dom.find('error'):
                print 'bs errored'
                tablecells = '<tr class="gamerow"><td></td><td></td><td></td><td>That user account could not be retrieved (check your privacy settings).</td><td><td></td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>'
                useravatarlarge = 'http://mysteamgauge.com/default_avatar.jpg'
                return tablecells, useravatarlarge
            # elif dom.find('p',{'class','errorPrivate'}):
                # tablecells = '<tr class="gamerow"><td></td><td></td><td></td><td>That user account is private.</td><td></td><td></td><td></td></tr>'
                # useravatarlarge = 'http://mysteamgauge.com/default_avatar.jpg'
                # return tablecells, useravatarlarge

        # Get a list of all the user's game ids
        gameidlist = []
        play_time_list = []
        gameid_filter = []
        # print 'page loaded fine'
        for x in dom.findAll('appid'):
            gameid_filter.append(x.text)
        #Get a list of game playtime
        user64id = dom.find('steamid64').text.encode('ascii','ignore')
        user_games_page = bs4.BeautifulSoup(urllib2.urlopen('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+config.API_KEY+'&steamid='+user64id+'&format=xml'))
        for x in user_games_page.findAll('appid'):
            if x.text in map(unicode.lower, gameid_filter):
                gameidlist.append(x.text)
                play_time = x.parent.find('playtime_forever').text
                if play_time:
                    if play_time == u'0':
                        play_time_list.append(play_time)
                    else:
                        play_time_list.append(unicode(int(play_time)/60))
                else:
                    play_time_list.append(u'0')
        print 'database queried fine'
        # Get Steam Avatar
        page2 = urllib2.urlopen('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+config.API_KEY+'&steamids='+user64id+'&format=xml')
        dom = bs4.BeautifulSoup(page2)
        useravatar = dom.findAll('avatar')[0].text.encode('ascii','ignore')
        useravatarmed = dom.findAll('avatarmedium')[0].text.encode('ascii','ignore')
        useravatarlarge = dom.findAll('avatarfull')[0].text.encode('ascii','ignore')
        usercreation=dom.findAll('timecreated')[0].text.encode('ascii','ignore')

        # Pull data for each game id
        # return gametitle, hdvalue, hdunit, type, multi, price, win, mac, linux, joy, metacritic, icon, slogo, logo, error
        for x in gameidlist:
            game_result = hdd_size(x)
            gametitlelist.append(game_result[0])
            hdvaluelist.append(game_result[1])
            hdunitlist.append(game_result[2])
            apptypelist.append(game_result[3])
            multilist.append(game_result[4])
            uspricelist.append(game_result[5])
            winlist.append(game_result[6])
            maclist.append(game_result[7])
            linuxlist.append(game_result[8])
            joylist.append(game_result[9])
            mclist.append(game_result[10])
            if game_result[11] == '-':
                iconlist.append('http://mysteamgauge.com/default_avatar.jpg')
            else:
                iconlist.append(game_result[11])
            errorlog.append(game_result[14])
        write_error(errorlog)
        tablecells = export_user(gameidlist,gametitlelist,hdvaluelist,hdunitlist,uspricelist,apptypelist,play_time_list,iconlist,multilist,winlist,maclist,linuxlist,joylist,mclist)
        return tablecells, useravatarlarge, usercreation

    except:
        tablecells = '<tr class="gamerow"><td></td><td></td><td></td><td>That user account could not be retrieved (check your privacy settings)</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>'
        useravatarlarge = 'http://mysteamgauge.com/default_avatar.jpg'
        usercreation = '0000000000'
        return tablecells, useravatarlarge, usercreation

def write_error(errors):
    error_list = []
    inFile = open(config.FILE_LOCATION+'errors.log', 'r')
    contents = inFile.read()
    error_list = contents.split('\n')
    inFile.close()
    new_errors = [x for x in errors if x not in error_list]
    if new_errors != '':
        outFile = open(config.FILE_LOCATION+'errors.log', 'a')
        for x in new_errors:
            outFile.write('\n'+x.encode('ascii','ignore')+'\n'+strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        outFile.close()

def hdd_size(app_query):
    queryid = model_v2.App_v1.query.filter_by(appid=app_query).first()
    if queryid == None:
        gametitle = 'Unavailable'
        hdvalue = '-'
        hdunit = '-'
        type = '-'
        multi = ''
        price = '-'
        win = ''
        mac = ''
        linux = ''
        joy = ''
        metacritic = ''
        icon = 'http://mysteamgauge.com/default_avatar.jpg'
        slogo = 'http://mysteamgauge.com/default_avatar.jpg'
        logo = 'http://mysteamgauge.com/default_avatar.jpg'
        error = app_query
        return gametitle, hdvalue, hdunit, type, multi, price, win, mac, linux, joy, metacritic, icon, slogo, logo, error
        # errorlog.append(app_query)
    else:
        gametitle = queryid.title
        hdvalue = queryid.hdspace
        hdunit = queryid.hdunit
        type = queryid.apptype
        multi = queryid.multiplayer
        price = queryid.usprice
        win = queryid.win_support
        mac = queryid.mac_support
        linux = queryid.linux_support
        joy = queryid.joysupport
        metacritic = queryid.metacritic
        icon = queryid.app_icon
        slogo = queryid.app_slogo
        logo = queryid.app_logo
        error = ''

        return gametitle, hdvalue, hdunit, type, multi, price, win, mac, linux, joy, metacritic, icon, slogo, logo, error

# tablecells = export_user(gameidlist,gametitlelist,hdvaluelist,hdunitlist,uspricelist,apptypelist,play_time_list,iconlist,multilist,winlist,maclist,linuxlist,joylist,mclist)
def export_user(gameidlist,gametitlelist,hdvaluelist,hdunitlist,uspricelist,apptypelist,play_time_list,iconlist,multilist,winlist,maclist,linuxlist,joylist,mclist):
    merged=[]
    table=[]
    for w,x,y,z,u,v,t,s,r,q,p,o,n,m in zip(gameidlist,gametitlelist,hdvaluelist,hdunitlist,uspricelist,apptypelist,play_time_list,iconlist,multilist,winlist,maclist,linuxlist,joylist,mclist):
        # w:gameidlist, x:gametitlelist, y:hdvaluelist, z:hdunitlist, u:uspricelist, v:apptypelist, t:play_time_list, s:iconlist, r:multilist, q:winlist, p:maclist, o:linuxlist, n:joylist, m:mclist
        merged.append(w)
        merged.append(x)
        merged.append(y)
        merged.append(z)
        merged.append(u)
        merged.append(v)
        merged.append(t)
        merged.append(r)
        merged.append(q)
        merged.append(p)
        merged.append(o)
        merged.append(n)
        merged.append(m)
        os_class=''
        multi_val=''
        if q == 'TRUE':
            os_class += ' win_os'
        if p == 'TRUE':
            os_class += ' mac_os'
        if o == 'TRUE':
            os_class += ' linux_os'
        if r == 'TRUE':
            multi_val = 'Yes'
        else:
            multi_val = 'No'
        table.append('<tr class="gamerow"><td class="col0 checkbox_col"><input class="includegame" name="includegame" type="checkbox" checked="checked" onclick="update_count();"></td><td class="col1 type_col" onclick="checkgame(this);">'+v+'</td>')
        table.append('<td class="col2 gameid_col" onclick="checkgame(this);">'+w+'</td>')
        table.append('<td class="col3 gamename_col" onclick="checkgame(this);"><img class="app_icon" src="'+s+'" alt="'+x+' icon"/><span class="app_title">'+x+'</span></td>')
        table.append('<td class="col4 os_col'+os_class+'" onclick="checkgame(this);"></td>')
        table.append('<td class="col5 contoller_col" onclick="checkgame(this);">'+n+'</td>')
        table.append('<td class="col6 metascore_col" onclick="checkgame(this);">'+m+'</td>')
        table.append('<td class="col7 multiplay_col" onclick="checkgame(this);">'+multi_val+'</td>')
        table.append('<td class="col8 playtime_col" onclick="checkgame(this);">'+t+'</td>')
        table.append('<td class="col9 value_col" onclick="checkgame(this);">'+u+'</td>')
        table.append('<td class="col10 size_col" onclick="checkgame(this);">'+y+'</td>')
        table.append('<td class="col11 unit_col" onclick="checkgame(this);">'+z+'</td></tr>')

    pubdir = os.path.abspath(os.path.dirname(os.getcwd()))+ config.PUBLIC_DIRECTORY
    fileloc = pubdir+'/'+steam_user+'.csv'
    headerlist=['Game Id','Game Name','Size','Unit','Value','Type','Hours Played','Mutiplayer','Windows','Mac OS','Linux','Controller Support','Metascore']
    with open(fileloc, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(headerlist)
        for a,b,c,d,e,f,g,h,i,j,k,l,m in zip(merged[0::13],merged[1::13],merged[2::13],merged[3::13],merged[4::13],merged[5::13],merged[6::13],merged[7::13],merged[8::13],merged[9::13],merged[10::13],merged[11::13],merged[12::13]):
            rowlist = [a,b,c,d,e,f,g,h,i,j,k,l,m]
            spamwriter.writerow(rowlist)

    # Write lists to html tables
    return ''.join(table)
