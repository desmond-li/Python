#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

def main():
	os.chdir(r'C:\Users\Desmond Li\Desktop\moedict\latex')

	data=open('moedict.txt','r',encoding='utf-8')
	output=open('output.txt','w',encoding='utf-8')

	processing(data,output)
	data.close()

	output=open('output.txt','r',encoding='utf-8')
	missing_character_replace(output)
	output.close()

	output_new=open('output_new.txt','r',encoding='utf-8')
	file_segmentation(output_new)
	output_new.close()

	print('LaTeX files are created successfully.')

	return 0

def processing(data,output): #read dictionary file and create LaTeX code
	character=['','']
	radical=['','']
	stroke=['','']
	pinyin=['','']
	index_order=['','']
	meaning=['','']
	item=[]

	each_line=data.readline()
	while each_line:
		(character[1],radical[1],stroke[1],pinyin[1],index_order[1],meaning[1])=each_line.split('\t')
		item=meaning[1].split('|')

		if radical[1]!=radical[0]: #add new radical
			if character[0]!='': #finish multicolumn environment
				output.writelines('\n\end{multicols}\n')
				print(radical[0]+'部 finished')
			output.writelines('\n\specialsectioning\n\chapter{'+radical[1]+'\ \ 部}\n\n\\begin{multicols}{2}\n')
			print(radical[1]+'部 start')
		
		if (radical[1]!=radical[0] or stroke[1]!=stroke[0]): #add new stroke
				output.writelines('\n\section{'+to_chinese(stroke[1])+'\ \ 畫}\n')

		output.writelines('\n\entry{'+character[1]+'}{'+pinyin[1]+'}{'+index_order[1]+'}\n') #add character
		output.writelines('{\n')

		if re.match('\[.\]',item[0]): #at least one enumerate/itemize environment needed
			_i=0
			while (item[_i]!='\n'):
				if re.match('\[.\]',item[_i]): #check grammar mark
					_enumerate=0
					_itemize=0
					output.writelines('\circled{\\texttt{'+item[_i][1]+'}}\n')
					
				else:
					if re.match('\d+',item[_i]): #enumerate environment
						if _enumerate==0:
							output.writelines('\\begin{enumerate}[label=\\arabic*,leftmargin=*]\n')
							_enumerate=1
						output.writelines(r'\item '+re.findall('[^\d\.].*',item[_i])[0]+'\n')
						if re.match('(\[.\])|(\n)',item[_i+1]):
							output.writelines('\end{enumerate}\n')
							_enumerate=0
					else: #itemize environment
						if _itemize==0:
							output.writelines('\\begin{itemize}[leftmargin=*]\n')
							_itemize=1
						output.writelines(r'\item '+re.findall('.*',item[_i])[0]+'\n')
						if re.match('(\[.\])|(\n)',item[_i+1]):
							output.writelines('\end{itemize}\n')
							_itemize=0
				_i+=1
			output.writelines('}\n')
			print(character[1])

		else:
			output.writelines(item[0]+'\n}\n')

		character[0]=character[1]
		radical[0]=radical[1]
		stroke[0]=stroke[1]
		pinyin[0]=pinyin[1]
		meaning[0]=meaning[1]
		each_line=data.readline()

	output.writelines('\n\end{multicols}\n')
	print(radical[0]+'部 finished')
	return 0

def to_chinese(num): #transfer storke (<100) to Chinese
	chinese_no=('零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十')

	num=int(num)
	if (num>=0 and num<=10):
		return chinese_no[num]
	else:
		decade=num//10
		mod=num%10
		if (num>=11 and num<=19):
			return chinese_no[10]+chinese_no[mod]
		else:
			if (mod==0):
				return chinese_no[decade]+chinese_no[10]
			else:
				return chinese_no[decade]+chinese_no[10]+chinese_no[mod]

def file_segmentation(output): #separate output.txt according to radicals
	file_name=('one','line','dot','slash','second','hook','two','lid','man','legs','enter','eight','down_box',
		'cover','ice','table','open_box','knife','power','wrap','spoon','right_open_box','hiding_enclosure',
		'ten','divination','seal','cliff','private','again','mouth','enclosure','earth','scholar','go','go_slowly',
		'evening','big','woman','child','roof','inch','small','lame','corpse','sprout','mountain','river','work',
		'oneself','turban','dry','short_thread','dotted_cliff','long_stride','two_hands','shoot','bow','snout',
		'bristle','step','heart','halberd','door','hand','branch','rap','script','dipper','axe','square','not',
		'sun','say','moon','tree','lack','stop','death','weapon','do_not','compare','fur','clan','steam','water',
		'fire','claw','father','double_x','half_tree_trunk','slice','fang','cow','dog','profound','jade','melon',
		'tile','sweet','life','use','field','bolt_of_cloth','sickness','dotted_tent','white','skin','dish','eye',
		'spear','arrow','stone','spirit','track','grain','cave','stand','bamboo','rice','silk','jar','net','sheep',
		'feather','old','and','plow','ear','brush','meat','minister','self','arrive','mortar','tongue','oppose',
		'boat','stopping','color','grass','tiger','insect','blood','walk_enclosure','clothes','west','see','horn',
		'speech','valley','bean','pig','badger','shell','red','run','foot','body','cart','bitter','morning','walk',
		'city','wine','distinguish','village','gold','long','gate','mound','slave','short_tailed_bird','rain',
		'blue','wrong','face','leather','tanned_leather','leek','sound','leaf','wind','fly','eat','head','fragrant',
		'horse','bone','tall','hair','fight','sacrificial_wine','cauldron','ghost','fish','bird','salt','deer',
		'wheat','hemp','yellow','millet','black','embroidery','frog','tripod','drum','rat','nose','even','tooth',
		'dragon','turtle','flute')

	_j=0
	_write=0

	each_line=output.readline()

	while each_line:
		if re.search('(specialsectioning)',each_line):
			segment=open(file_name[_j]+'.tex','w',encoding='utf-8')
			_write=1
		
		if _write==1:
			segment.writelines(each_line)

		if re.search('(end{multicols})',each_line):
			segment.close()
			print(file_name[_j]+'.tex is segmented.')
			_write=0
			_j+=1

		each_line=output.readline()

	return 0

def missing_character_replace(output): #replace the fonts for some missing characters to make it shown in PDF file
	segoe_ui_symbol=('☰','☷','☴','☳','☵','☲','☱','☶','⚋','⚊') #the Eight Diagrams in I-Ching
	pmingliu=('丂','丩','玍','乣','䢵','佊','倝','倽','䱷','䦯','倸','傉','翶','㑿','冣','戞','鞼','砊','礚',
		'㓦','㔩','卐','䩦','㕒','㕙','叕','㴆','呝','䁆','咵','哰','㯶','唕','閄','㖪','槅','嘚','噇','嚈',
		'㘔','坄','晐','鼃','陿','夨','奞','㛂','鮌','内','鵕','尀','㞞','屵','㟏','硣','皃','崡','嵸','嶾',
		'岹','巜','幐','㢝','弆','鉂','攧','㵣','愗','䯱','恑','忼','帀','㥄','㥏','扅','䦟','㧙','掆','厷',
		'掿','聄','摣','㧗','飰','撧','㩐','㩳','辬','㫃','㺜','侌','蒕','㬊','曃','杘','㩍','衺','枊','栙',
		'䉶','磶','㔶','㣥','䄙','殜','殹','䍽','㲪','㲯','䰐','氎','埛','爥','䞟','肹','㡛','㵒','㵝','㵞',
		'溭','㶁','㵠','愺','䬠','㶟','焿','㸌','㸙','犼','㹜','狧','獕','勔','叀','䆉','疁','痆','黣','䀇',
		'䀠','䀢','閴','䁑','瞖','䶕','瞤','㳌','䃴','僃','禼','䅳','䆿','竱','䚻','眡','篗','篅','䉛','䈰',
		'醿','䈾','㩴','簺','籋','餦','䪻','虵','緫','䰖','匶','䍡','魪','䍦','䍪','曕','䏿','腨','㕹','尗',
		'莂','旊','蘽','䪤','䗊','蝲','䖵','蛼','蟩','鼅','鼄','螠','裑','裓','䘿','襀','帬','襵','説','藴',
		'鞓','觵','髤','藳','䛟','䱇','匌','㹠','䟫','䞤','躃','輨','輢','辡','犫','逩','鰧','蜹','䍤','鉳',
		'䫉','阫','廵','颰','䇓','䨲','靧','絥','䋶','䫜','䫄','頢','䫏','䬀','餶','飿','繦','饆','饠','駊',
		'騀','䐶','鬇','鬡','䰀','䰰','魭','鯶','鱇','䏽','鮻','㗘','䴈','鷧','齭','猍','硶','苄','骲','煏',
		'韠','礴','羓','膪','韂','閦','鑔','茝','憁','鑹','垡','銱','侊','餜','擀','剨','劐','鉷','睺','敫',
		'垍','皀','揢','瞘','臁','瓓','倈','嫏','傈','鑥','腼','憹','硇','黁','㕷','孴','筢','鉕','臤','鵮',
		'叒','蒒','睃','遬','螋','凇','䠷','媠','疃','㒓','鍮','夲','謟','氽','㭘','卂','嚱','厓','㖡','癔',
		'唫','鮋','鐭','媖','滺','嗻','㑳','衠','砈','妸','揞','鮟') #characters in BMP
	pmingliu_extb=('𥳑','𠐍','𠗌','𡩋','𢠳','𡧮','𦞂','𨃓','𧴄','𣝓','𡙇','𦸅','𥒜','𤎖','𤍿','𧳵','𥲤','𦬊',
		'𥢧','𥫱','𠟪','𪰋','𦇎','𦁊','𦌊','𦞦','𧮫','𧂭','𢬵','𨄅','𨉣','𢓳','𥽈','𩂣','𤺺','𩢷','𩮜','𤫶','𤨕','𤬁') 
		#characters in SMP

	output_old=open('output_old.txt','w',encoding='utf-8') #copy the content of output.txt to _old
	for each_line in output:
		output_old.writelines(each_line)
	output_old.close()

	output_old=open('output_old.txt','r',encoding='utf-8')
	output_new=open('output_new.txt','w',encoding='utf-8')

	for _k in range(0,len(segoe_ui_symbol)): #complete missing characters
		for each_line in output_old:
			if each_line.find(segoe_ui_symbol[_k])+1:
				output_new.writelines(re.sub(segoe_ui_symbol[_k],r'{\\texttt{'+segoe_ui_symbol[_k]+'}}',each_line))
			else:
				output_new.writelines(each_line)
		print(segoe_ui_symbol[_k],'replaced')
		output_old=open('output_old.txt','w',encoding='utf-8')
		output_new=open('output_new.txt','r',encoding='utf-8')
		for each_line in output_new: #update _old
			output_old.writelines(each_line)
		output_old=open('output_old.txt','r',encoding='utf-8')
		output_new=open('output_new.txt','w',encoding='utf-8')
		
	for _k in range(0,len(pmingliu)): #complete missing characters
		for each_line in output_old:
			if each_line.find(pmingliu[_k])+1:
				output_new.writelines(re.sub(pmingliu[_k],r'{\\textsf{'+pmingliu[_k]+'}}',each_line))
			else:
				output_new.writelines(each_line)
		print(pmingliu[_k],'replaced')
		output_old=open('output_old.txt','w',encoding='utf-8')
		output_new=open('output_new.txt','r',encoding='utf-8')
		for each_line in output_new: #update _old
			output_old.writelines(each_line)
		output_old=open('output_old.txt','r',encoding='utf-8')
		output_new=open('output_new.txt','w',encoding='utf-8')

	for _k in range(0,len(pmingliu_extb)): #complete missing characters
		for each_line in output_old:
			if each_line.find(pmingliu_extb[_k])+1:
				output_new.writelines(re.sub(pmingliu_extb[_k],r'{\\textbf{\\textsf{'+pmingliu_extb[_k]+'}}}',each_line))
			else:
				output_new.writelines(each_line)
		print(pmingliu_extb[_k],'replaced')
		output_old=open('output_old.txt','w',encoding='utf-8')
		output_new=open('output_new.txt','r',encoding='utf-8')
		for each_line in output_new: #update _old
			output_old.writelines(each_line)
		output_old=open('output_old.txt','r',encoding='utf-8')
		output_new=open('output_new.txt','w',encoding='utf-8')

	output_old.close()
	output_new.close()

	os.remove('output_new.txt')
	os.rename('output_old.txt','output_new.txt')
	print('output.txt is updated to output_new.txt')
	return 0


if __name__ == '__main__':
    main()