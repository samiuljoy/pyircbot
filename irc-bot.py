#!/usr/bin/env python3

# importing modules
import sys
import time
from time import ctime
import socket
import os
import requests
import ntplib
import re
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
#import ssl

server_address="irc.libera.chat"
server_port = 6667

botnick="yourbotnick"
channel_name="#yourchannelname"

#ctx = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#irc = ctx.wrap_socket(sock)

irc.connect((server_address,server_port))
irc.setblocking(False)

time.sleep(1)
irc.send(("USER "+botnick+" "+botnick+" "+botnick+" bot has joined the chat\r\n").encode())

irc.send(("NICK "+botnick+"\n").encode())

time.sleep(1)
# replace yourpassword on the line below with your password if you need to idenify yourself to the server

irc.send(("PRIVMSG"+" :NickServ IDENTIFY yourpassword"+"\n").encode())

time.sleep(2)

irc.send(("JOIN "+channel_name+"\n").encode())

# functions

def send_msg(msg):
	irc.send(bytes("PRIVMSG "+channel_name+" :"+msg+"\n", "UTF-8"))

def weather_msg():
	os.system("curl -s wttr.in | head -n7 > file.txt")
	file = open("file.txt", 'r')
	for line in file:
		send_msg(str(line))
	file.close()

def show_time():
	c = ntplib.NTPClient()
	response = c.request('time.google.com')
	time_now = ctime(response.tx_time)
	send_msg(str(time_now))

# while loop

while True:
	try:
		text = irc.recv(2048).decode("UTF-8")
		text = text.strip("\r\n")

	except Exception:
		pass
	if text.find("PRIVMSG") !=-1:

		user_name = re.sub("!.*","",text)
		clean_name = re.sub(":","",user_name)

		cmd_initial = text.split(":", maxsplit=3)[2]
		cmd_val = re.sub("\s.*","",cmd_initial)

		if cmd_val == "!weather":
			weather_msg()
			text=""
		elif cmd_val == "!time":
			show_time()
			text=""
		elif cmd_val == "!hello":
			send_msg("hello to you too! "+clean_name)
			text=""
		elif text.find('!what is your name?') !=-1:
			send_msg("My name is lamebot, what's yours?")
			text=""
		elif text.find('!what is the weather?') !=-1:
			weather_msg()
			text=""
		elif cmd_val == "!wiki":
			pre_wiki_term = text.split("!wiki", maxsplit=1)[1]

			def wiki_search():
				# prints out the introductory paragraph from wikipedia
				wiki_request = requests.get("https://en.wikipedia.org/wiki/"+wiki_search_term)
				wiki_text = wiki_request.text
				soup = BeautifulSoup(wiki_text, "html.parser")
				wiki_paragraph = soup.find_all('p')[1].get_text()
				wiki_final = re.sub("\[.\]","",wiki_paragraph)
				wiki_main = str(wiki_final)

				if len(wiki_main) < 10:
					send_msg("no article on "+wiki_search_term+" on wikipedia")
				else:
					send_msg("wikipedia "+wiki_search_term+"-> "+wiki_main)

			if pre_wiki_term == "":
				send_msg("empty search term, usage -> !wiki russia")
				text=""
			else:
				wiki_search_term = pre_wiki_term.strip()
				wiki_search()
				text=""

		elif cmd_val == "!google":

			pre_search_term = text.split("!google", maxsplit=1)[1]

			def google_search():
				# Build a service object for interacting with the API. Visit
				# the Google APIs Console <http://code.google.com/apis/console>
				# to get an API key for your own application.
				initial = 11
				final = 10

				service = build(
					"customsearch", "v1", developerKey="AIzaSyCy6tveUHlfNQDUtH0TJrF6PtU0h894S2I"
				)

				res = (
					service.cse()
					.list(
						q=search_term,
						#cx="017576662512468239146:omuauf_lfve",
						cx = '005983647730461686104:qfayqkczxfg',
					)
					.execute()
				)
				string_value = str(res)

				initial_value = string_value.find('snippet')
				final_value = string_value.find('htmlSnippet')
				result_value = string_value[initial_value+initial:final_value-final]
				result_value_clean = result_value.replace("\\","")
				search_term_new = re.sub("\s","+",search_term)

				if len(result_value_clean) < 6:
					send_msg("no google search results for "+search_term)
				else:
					send_msg("Google says -> "+result_value_clean+".....")
					send_msg("Further Reading https://google.com/search?q="+search_term_new)

			if pre_search_term == "":
				send_msg("empty search term")
				text=""
			else:
				search_term = pre_search_term.strip()
				google_search()
				text=""

		elif cmd_val == "!dic":
			pre_dic_term = text.split("!dic", maxsplit=1)[1]

			def dictionary_search():
				req = requests.get("https://www.dictionaryapi.com/api/v3/references/collegiate/json/"+dic_term+"?key=868c92dc-3439-49a8-a93b-385e419d20f5")

				req_text = req.text
				start_dic_pos = req_text.rfind("shortdef")
				initial_dic_word = req_text[start_dic_pos+11:]

				clean_dic_word = initial_dic_word.rstrip("]}")
				more_clean_dic_word = clean_dic_word.replace("\\u0027","'")

				if len(more_clean_dic_word) < 5:
					send_msg("no dictionary results for "+dic_term)
				else:
					send_msg("meaning of "+dic_term+"-> "+more_clean_dic_word)
					send_msg("Further Reading -> https://www.merriam-webster.com/dictionary/"+dic_term)

			if pre_dic_term == "":
				send_msg("empty word given")
				text=""
			else:
                dic_term = pre_dic_term.strip()
				dictionary_search()
				text=""

input()
