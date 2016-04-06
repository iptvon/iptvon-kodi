#################################################
# -*- coding: utf-8 -*-
#################################################
# By IPTVON
# Atualização 0.0.5: 06/04/2015
#################################################
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, urllib, urllib2, os, sys, datetime, time, re, base64

from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

####################################################### CONSTANTES #####################################################

addon_id    = 'plugin.video.iptvon'
selfAddon   = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder   = addonfolder + '/resources/art/'
fanart      = addonfolder + '/fanart.jpg'
selfAddon   = xbmcaddon.Addon(id=addon_id)

usern = urllib.quote(selfAddon.getSetting('username'))
passw = selfAddon.getSetting('password')

passcp = selfAddon.getSetting('passcp')

server  = 'http://stream.iptvon.tk:8000/'
server2 = 'http://www.iptvon.tk/stream/playlists/'
flmsrv  = 'http://www.iptvon.tk/stream/filmes/'
vidsrv  = 'http://www.iptvon.tk/stream/videos/'
imgsrv  = 'http://www.iptvon.tk/stream/imgs/'

url_base = base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vbWVzdHJlLnBocA==')
url_base2 = base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vY2FuYWlzLmh0bWw=')
url_base3 = base64.b64decode('aHR0cDovL3d3dy50di1tc24uY29tL3BsYXllci9wbGF5ZXIuc3dm')

flm24h ='rtmp://208.53.180.242/ctv playpath=filmes swfUrl=http://www.carolineoliveira.com.br/swf/player.swf?IPTVINABOX pageUrl=http://carolineoliveira.com.br/tvamigos/filmes.html'

#########################################################################################################
PLIST = []
PLAYLISTSS = []
dialog = xbmcgui.Dialog()

def myAccount(url):
		link = openURL(url)
		status = re.compile('"status":"(.+?)"').findall(link)
		expdate = re.compile('"exp_date":"(.+?)"').findall(link)
		user  = re.compile('"username":"(.+?)"').findall(link)
		activecons = re.compile('"active_cons":"(.+?)"').findall(link)
		created = re.compile('"created_at":"(.+?)"').findall(link)
		maxcons = re.compile('"max_connections":"(.+?)"').findall(link)
		format = re.compile('"allowed_output_formats":(.+?)}').findall(link)
		
		addDir2('[COLOR green]INFORMAÇÕES DA CONTA[/COLOR]','','','')
		
		for url in user       : addDir2('[COLOR yellow]Usuário: [/COLOR]%s'%(url),'','','')
		for url in status     : addDir2('[COLOR yellow]Status: [/COLOR]%s'%(url),'','','')
		for url in created    : 
				dthr = int(url)
				t = time.gmtime(dthr)
				if int(t[4]) < 10 : tmin = '0' + str(t[4])
				else        : tmin = t[4]
						
				if int(t[5]) < 10 : tsec = '0' + str(t[5])
				else        : tsec = t[5]
				dtCre = '%s/%s/%s %s:%s:%s' % (t[2], t[1], t[0], t[3], tmin, tsec)
				addDir2('[COLOR yellow]Criado: [/COLOR]%s'%(dtCre),'','','')
				
		for url in expdate    : 
				dthr = int(url)
				t = time.gmtime(dthr)
				
				if int(t[4]) < 10 : tmin = '0' + str(t[4])
				else         : tmin = t[4]
						
				if int(t[5]) < 10 : tsec = '0' + str(t[5])
				else         : tsec = t[5]
				dtExp = '%s/%s/%s %s:%s:%s' % (t[2], t[1], t[0], t[3], tmin, tsec)
				addDir2('[COLOR yellow]Expira: [/COLOR]%s'%(dtExp),'','','')
				
		for url in activecons : addDir2('[COLOR yellow]Conexões Ativas: [/COLOR]%s'%(url),'','','')
		for url in maxcons    : addDir2('[COLOR yellow]Conexões Máximas: [/COLOR]%s'%(url),'','','')
		for url in format     : addDir2('[COLOR yellow]Formatos Disponíveis: [/COLOR]%s'%(url),'','','')
		
		xbmc.executebuiltin("Container.SetViewMode(50)")
		
def menuPrincipal():
		link  = urllib.urlopen('%s/panel_api.php?username=%s&password=%s'%(server,usern,passw)).read()
		
		try :
				login = re.compile('"auth":(.+?),').findall(link)[0]
				
				if login == '1'  :
						addDir("Tv", "", 1, artfolder + "tv.png",1,True,'',fanart)
						addDir("Filmes", "", 2, artfolder + "filmes.png",1,True,'',fanart)
						addDir("Séries", "", 3, artfolder + "series.png",1,True,'',fanart)
						addDir("Vídeos", "", 4, artfolder + "filmes.png",1,True,'',fanart)
						addDir("Minha Conta", '%s/panel_api.php?username=%s&password=%s'%(server,usern,passw), 99998, artfolder + "conta.png",1,True,'',fanart)
						addDir("Configurações", "", 99999, artfolder + "config.png",1,False,'',fanart)
						
						xbmc.executebuiltin("Container.SetViewMode(50)")
				else:
						dialog.ok("Error!", "Details Were Incorrect!")
						return
		except :
				addDir("Apenas para usuários.", "", "-", artfolder + "conta.png")
				addDir("Caso já tenha login/senha, insira na configuração do addon.", "", "-", artfolder + "conta.png")
		
def getCategorias() :
		link = server + 'get.php?username=%s&password=%s&type=m3u_plus&output=hls' % (usern, passw)
		
		getPlaylist(link)
		
		totP = len(PLIST)
		
		CATS = []
		
		for i in range(totP) :
				titC = PLIST[i][0]
				
				if titC not in CATS : CATS.append(titC)
						
		totC = len(CATS)	

		for i in range(totC) :
				titC = CATS[i]
				
				if not ',' in titC :  ### Gambiarra para corrigir a lista
						imgC = imgsrv + titC.lower() + ".png"
						
						if titC == "PT"  : titC = "Portugal"
						if titC == "BR"  : titC = "Brasil"
						if titC == "UK"  : titC = "Bônus Inglaterra"
						if titC == "FR"  : titC = "Bônus França"
				
						addDir(titC, '', 10, imgC, totC)
						
						#if titC == "Brasil" :
						#		addDir('Bônus Brasil', '', 11, imgsrv + 'br.png', 1)						
				
		addDir('Bônus USA/Canada', '', 10, imgsrv + 'usa.png', 1)
		addDir('Bônus Espanha', '', 10, imgsrv + 'es.png', 1)
		addDir('Bônus Adultos', '', 13, 'adultos.png', 1)
		
		xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
		xbmc.executebuiltin("Container.SetViewMode(500)")
		
def getCanais(categoria):
		if 'Portugal'   in categoria : categoria = "PT"
		if 'Brasil'     in categoria : categoria = "BR"
		if 'USA'        in categoria : categoria = "USA"
		if 'Inglaterra' in categoria : categoria = "UK"
		if 'França'     in categoria : categoria = "FR"
		if 'Espanha'    in categoria : categoria = "ES"
		if 'Adultos'    in categoria : categoria = "XXX"
			
		canais = getPlaylist(server2 + 'get.php?category=%s' % (categoria))
		
		totC = len(canais)
		
		for i in range(totC) :
				catC = PLIST[i][0]
				
				if catC == categoria :
						titC = PLIST[i][1]
						
						if not 'RADIO' in titC :								
								urlC = PLIST[i][2]
								
								if not '://' in PLIST[i][3] : imgC = imgsrv + PLIST[i][3]
								else                        : imgC = PLIST[i][3]
								
								addDir(titC, urlC, 100, imgC, totC, False)
								
		xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
		xbmc.executebuiltin("Container.SetViewMode(500)")

def getCanais2():
		cat = "BR2"
		canais = getPlaylist2(server2 + 'get.php?category=%s' % (cat))

		totC = len(canais)
		
		for i in range(totC) :
				catC = PLIST[i][0]
				
				if catC == cat :
						titC = PLIST[i][1]
						urlC = PLIST[i][2]
						imgC = imgsrv + PLIST[i][3]

						addDir(titC, urlC, 101, imgC, totC, False)
		
		xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
		xbmc.executebuiltin('Container.SetViewMode(500)')	
		
def getCanaisXXX():
		cat = 'XXX'
		
		passcp = selfAddon.getSetting('passcp')
		
		if len(passcp) > 0 :
				keyb = xbmc.Keyboard('', 'Digite a sua senha para acessar os canais adultos') 
				keyb.doModal() 
				
				if (keyb.isConfirmed()):
						if keyb.getText() == passcp :
								canais = getPlaylist(server2 + 'get.php?category=%s' % (cat))
								
								totC = len(canais)
								
								for i in range(totC) :
										catC = PLIST[i][0]
										
										if catC == cat :
												titC = PLIST[i][1]
												
												if not 'RADIO' in titC :
														#if ':' in titC :titC = titC.split(': ')[1]
														
														urlC = PLIST[i][2]
														
														if not '://' in PLIST[i][3] :
																imgC = imgsrv + PLIST[i][3]
														else :
																imgC = PLIST[i][3]
														
														addDir(titC, urlC, 100, imgC, totC, False)
														
								xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
								xbmc.executebuiltin("Container.SetViewMode(500)")
						else :
								dlg = xbmcgui.Dialog()
								dlg.ok('Controle Parental', 'Senha Incorreta. Tente Novamente')				
								getCanaisXXX()
		else :
				dlg = xbmcgui.Dialog()
				dlg.ok('Controle Parental', 'Você deve configurar uma senha para acessar os canais adultos.')				
				selfAddon.openSettings()
				getCanaisXXX()
				
def menuFilmes():
    #addDir("Filmes IPTVON"    , flmsrv + "/filmesiptvon.m3u8", 20, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    #addDir("Filmes Dublados"  , flmsrv + "?x=dub",  21, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    #addDir("Filmes Legendados", flmsrv + "?x=leg",  21, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Filmes Infantís"  , flmsrv + "?x=inf",  21, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Filmes 24h"       , flm24h           , 100, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png", 0, False)
		
    xbmc.executebuiltin("Container.SetViewMode(50)")
		
def getFilmes(url):
		canais = getPlaylist(url)
		
		totC = len(canais)
		
		for i in range(totC) :
				titC = PLIST[i][1]
				
				if not 'RADIO' in titC :						
						urlC = PLIST[i][2]
						
						if not '://' in PLIST[i][3] : imgC = imgsrv + PLIST[i][3]
						else                        : imgC = PLIST[i][3]
								
						addDir(titC, urlC, 100, imgC, totC, False)
										
		xbmc.executebuiltin("Container.SetViewMode(500)")

def menuVideos():
    #addDir("Festivais"  , vidsrv + "?x=fes", 40, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    #addDir("Shows"      , vidsrv + "?x=sho", 40, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    #addDir("Videoclipes", vidsrv + "?x=vdc", 40, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    
    xbmc.executebuiltin("Container.SetViewMode(50)")
		
def getItems(url):	
		link = openURL(url)
		
		if '<item>' in link : 
				items = link.split('<item>')
				
				for item in items:
				
						if '<title>' in item :
								nameF = re.compile('<title>(.*?)</title>').findall(item)[0]
								fartF = re.compile('<fanart>(.*?)</fanart>').findall(item)[0]
								
								if not fartF : fartF = ""
								
								imgF  = re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
								
								item  = item.replace('\n','')
								
								urlF  = re.compile('<link>(.*?)</link>').findall(item)[0]
								
								if not urlF : urlF = "http:///"

								addDirF(nameF, urlF, 100, imgF, fartF, False)
										
		xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
		xbmc.executebuiltin("Container.SetViewMode(500)")
		
def getPlaylist(url) :
		link = openURL(url)
		
		link = link + "\n\n\n\n"
		
		playlist = re.compile('tvg-logo="(.*?)" group-title="(.+?)",(.+?)\r.+?(.+?)[\n]', re.DOTALL).findall(link.replace('\n\n','\n'))
		
		for imgP, catP, titP, urlP in playlist:
				if imgP == '' : 
						imgP = urlP.replace('m3u8','png')
								
				urlP = urlP.replace('\r','')

				PLIST.append([catP, titP, urlP, imgP])
				
		return PLIST
		
def getPlaylist2(url) :
		link = openURL(url)
		
		link = link + "\n\n\n\n"
		
		playlist = re.compile('tvg-logo="(.*?)" group-title="(.+?)",(.+?)\r.+?(.+?)[\n]', re.DOTALL).findall(link.replace('\n\n','\n'))
		
		for imgP, catP, titP, urlP in playlist:
				if imgP == '' : imgP = urlP.replace('m3u8','png')
								
				urlP = urlP.replace('\r','')

				#if not '://' in urlP : urlP = '%slive/%s/%s/%s' % (server, usern, passw, urlP)
				
				PLIST.append([catP, titP, urlP, imgP])
				
		return PLIST
		
def player(arg, icon, nome):
		#playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist = xbmc.PlayList(1)
		playlist.clear()
		
		try:
				tuple_ = eval(arg)
				
				print tuple_
				
				for link in tuple_:
						print "LINK = " + str(link)
						
						if not '://' in link : 
						
								if 'n2r' in link :
										params = url.split(',')
										
										ip = params[1]
										playpath = params[2]
										url2Play = 'rtmp://'+ip+'/live?wmsAuthSign='+getWMS() +' playpath='+playpath+' swfUrl='+base64.b64decode('aHR0cDovL3d3dy50di1tc24uY29tL3BsYXllci9wbGF5ZXIuc3dm')+' live=1 pageUrl='+base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vbWVzdHJlLnBocA==')+' token='+getToken() +' '

								else :
									url2Play = '%slive/%s/%s/%s' % (server, usern, passw, link)
						else :
								url2Play = link
						
						print "URL2PLAY " + str(url2Play)
						
						listitem = xbmcgui.ListItem(nome, thumbnailImage=iconimage)
						listitem.setInfo('video', {'Title': nome})
						listitem.setProperty('mimetype', 'video/mp4')
						playlist.add(url2Play, listitem)
		except:
				if not '://' in arg : 
						if 'n2r' in arg :
								params = url.split(',')
								
								ip = params[1]
								playpath = params[2]
								url2Play = 'rtmp://'+ip+'/live?wmsAuthSign='+getWMS() +' playpath='+playpath+' swfUrl='+base64.b64decode('aHR0cDovL3d3dy50di1tc24uY29tL3BsYXllci9wbGF5ZXIuc3dm')+' live=1 pageUrl='+base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vbWVzdHJlLnBocA==')+' token='+getToken() +' '
						else :
								url2Play = '%slive/%s/%s/%s' % (server, usern, passw, arg)
				else :
						url2Play = arg
				
				listitem = xbmcgui.ListItem(nome, thumbnailImage=iconimage)
				listitem.setInfo('video', {'Title': nome})
				
				#playlist.add(url=url2Play, listitem=listitem, index=7)
				playlist.add(url2Play, listitem)
				
		#xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)		
		#xbmcplugin.endOfDirectory(int(sys.argv[1]))
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)

def player2(url, iconimage, name):
		playlist = xbmc.PlayList(1)
		playlist.clear()
		
		args     = url.split(',')
		ip       = args[0]
		playpath = args[1]
		link     = 'rtmp://' + ip + '/live?wmsAuthSign=' + getWMS() +' playpath='+playpath+' swfUrl='+url_base3+' live=1 pageUrl='+url_base+' token='+getToken() +' '
		
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		
		playlist.add(link,listitem)	
		
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)

#############################################################################################################

def openURL(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent' , "Magic Browser")
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()

	return link

def addLink(name, url, iconimage):
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('fanart_image', "%s/fanart.jpg" % selfAddon.getAddonInfo("path"))
		
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)

def addDir(name, url, mode, iconimage, total=0, pasta=True, plot='', fanart=''):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)

	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)

	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
	liz.setProperty('fanart_image', fanart)

	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)
		
def addDir2(name, url, mode, iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	
	ok=True
	
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	
	return ok


def addDirF(name, url, mode, iconimage, fanart, pasta=True, total=1) : 
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)

	ok = True

	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)

	liz.setInfo(type="Video", infoLabels={ "Title": name } )

	try    : liz.setProperty('fanart_image', fanart)
	except : liz.setProperty('fanart_image', '')
					
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)

	return ok
		
def getWMS():
		req = urllib2.Request(base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vbWVzdHJlLnBocA=='))
		req.add_header('referer', base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vY2FuYWlzLmh0bWw='))
		response = urllib2.urlopen(req)
		link     = response.read()
		response.close()
		wms = re.compile(r"AuthSign=(.+?)&auto").findall(link)[0]

		return wms	

def getToken():
		req      = urllib2.Request(base64.b64decode('aHR0cHM6Ly9kb2NzLmdv­b2dsZS5jb20vdWM/­ZXhwb3J0PWRvd25sb2FkJ­mlkPTBCeE4wRHpGakllQ­2FPWGR1ZVc0MVJFMVBXb­XM='))
		response = urllib2.urlopen(req)
		token    = response.read()
		response.close()

		return token	
		
def openConfig():
		selfAddon.openSettings()
		menuPrincipal()

#######################################################################################################

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]                 
    return param

params    = get_params()
url       = None
name      = None
iconimage = None
mode      = None


try    : url = urllib.unquote_plus(params["url"])
except : pass
try    : name = urllib.unquote_plus(params["name"])
except : pass
try    : iconimage = urllib.unquote_plus(params["iconimage"])
except : pass
try    : mode = int(params["mode"])
except : pass

#print "Mode: "+str(mode).decode('utf-8')
#print "URL : "+str(url).decode('utf-8')
#print "Name: "+str(name).decode('utf-8')
#print "Icon: "+str(iconimage).decode('utf-8')

if mode == None  : menuPrincipal()

#TV
elif mode == 1   : getCategorias()
elif mode == 10  : getCanais(name)
elif mode == 11  : getCanais2()
elif mode == 12  : doCanais(name)
elif mode == 13  : getCanaisXXX()

#FILMES
elif mode == 2   : menuFilmes()
elif mode == 20  : getFilmes(url)
elif mode == 21  : getItems(url)

#VIDEOS
elif mode == 4   : menuVideos()
elif mode == 40  : getItems(url)

#PLAYER
elif mode == 100 : player(url, iconimage, name)
elif mode == 101 : player2(url, iconimage, name)

#INFO CONTA
elif mode == 99998:
    myAccount(url)

#CONFIG
elif mode == 99999:
    openConfig()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
