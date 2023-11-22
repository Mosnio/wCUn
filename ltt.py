import requests,json,string
import time
import random
import sys
import colorama
from colorama import Fore, Back, Style


lblk7= Style.BRIGHT+Fore.LIGHTRED_EX+Back.LIGHTWHITE_EX


lblk6= Style.BRIGHT+Fore.LIGHTCYAN_EX+Back.LIGHTBLUE_EX

lblk5= Style.BRIGHT+Fore.LIGHTYELLOW_EX+Back.LIGHTBLACK_EX


lblk4=Style.BRIGHT+Fore.LIGHTMAGENTA_EX+Back.LIGHTWHITE_EX

lblk = Style.BRIGHT+Fore.CYAN+Back.LIGHTBLACK_EX

lblk2 = Style.BRIGHT+Fore.GREEN+Back.LIGHTBLACK_EX

lbllk = Style.BRIGHT+Fore.LIGHTWHITE_EX+Back.LIGHTBLACK_EX

lblk3 = Style.BRIGHT+Fore.LIGHTWHITE_EX+Back.LIGHTBLACK_EX

bcy = Style.BRIGHT+Fore.CYAN
bgrn = Style.BRIGHT+Fore.GREEN
res = Style.RESET_ALL
nwh = Style.NORMAL+Fore.WHITE
bwh = Style.BRIGHT+Fore.WHITE
mag = Style.NORMAL+Fore.MAGENTA
bmag = Style.BRIGHT+Fore.MAGENTA
ngr = Style.NORMAL+Fore.GREEN
nred = Style.NORMAL+Fore.RED
bblu = Style.BRIGHT+Fore.BLUE
bred = Style.BRIGHT+Fore.RED
byel = Style.BRIGHT+Fore.YELLOW
nyel = Style.NORMAL+Fore.YELLOW


myel=Style.BRIGHT+Fore.YELLOW+Back.LIGHTRED_EX

mgrn=Style.BRIGHT+Back.YELLOW+Fore.RED


#### CHANGING SEED ####
def cs():
	N=random.randint(10,64)
	res = ''.join(random.choices(string.ascii_lowercase+string.digits, k=N))
#	print(res)
	res1 = ''.join(random.choices(string.ascii_lowercase+string.digits, k=64))
#	print(res1)
	auth={
	"X-Requested-With": "XMLHttpRequest",
	"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1IiwianRpIjoiN2IwYTljNGE5ZGU4ZTc5ODgxMDFhZGQzZDllMTkwNWRjY2ViMTUxZDVmZGI1NjYwYTE4MTVlMzkyYmRkOGEyYTE2MTJlZDZlZDgyMTg0YjkiLCJpYXQiOjE2ODY0MjExMzAuMjE1OTQyLCJuYmYiOjE2ODY0MjExMzAuMjE1OTQ4LCJleHAiOjE3MTgwNDM1MzAuMjA5MDgxLCJzdWIiOiIzMjgyNzMiLCJzY29wZXMiOltdfQ.gk0ipHN6WITXAIoMpgAYFptLXs2uLNhA2SSPULFJE783grLo78bh-EfroZts7E7Z_FvGn_tvyhvj2oGkTu3_hs20mpD_o7O8Koov7NZj4sibJBhi-dS7PXYPtRqSqDb_X9FLP-T0ccNTxWHreGl4ZA1q8hhzYHQzfn6Jgh6WwZsutvyq0X5NMHsBasLypr4BftmuxGG-sN5kl_sU4iIa_DKmOkr30azBJ4o_sQQ7maEfcZNfqCSp2Z5D6rCscTa9glGwpt1dPIRVOshcg2LcvEIH47eOHQniELDWxqeYQakdmrrR67OQcQ6JhC3xmXJ0JKaQOZ7uunit5-cwME3VWF_vD_WBgu3j3Q4Murs71t4EiMBBzxFQRiazF1n9HdYq86wN2Unu0SSdoWCLRzaT5h65xWkbQWDudO2jcuhDGC787SVRKOfsKUotaVVjH4FmhusksYvn4SHYJ-5h89jdrn7UAdB81SUXobhtPb1pQufJnNqKffY-7xqmXhz_g6AjwklhNL7VspTPAJ_D14DURvy_o3Zif2hCKDCn_7HMg403TZsOf-LpNcUnGg2gw9QzDfsQabMmXUKi4wumJxRIww9xLY2zss18h7rEBRl5U0YRMmbmWz40x3VfLIp5GPit3tc8MErqS_k2x3OXcY7gE9cLZOHwBfAlnWRYr_TuJtw",
	"user-agent":"Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"
	}
	url = 'https://wolf.bet/api/v1/game/seed/refresh'
	url2='https://wolf.bet/api/v1/user/seed/refresh'
	payload={
	"server_seed_hashed": res1
	}
	data={
	"client_seed": res
	}
	r=requests.get(url=url,params=payload,headers=auth)
	dts=r.json()
#	print(dts)
	r4=requests.post(url=url2,data=data,headers=auth)
	dts1=r4.json()
	print("")
	print("SEED HAS CHANGED")
	print("")

#### SENDING MESSAGE ###1

mesg=['keep It green' , 'keep winning and play safe guys' , 'keep winning' ,' congrats all ' ,'lets go guys' , 'Goodluck all' ,' best of luck all ', 'keep It green guys' , 'stay green all' ,' Winners keep green','have fun guyss' ,' this is your day guys lets do it', 'more win Fellas' ,' more green frnds',' stay winning guys' ]

messag = random.choice(mesg)



c = requests.session()
url3="https://wolf.bet/api/v1/bet/place"
ua3={
"X-Requested-With": "XMLHttpRequest",
 "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1IiwianRpIjoiN2IwYTljNGE5ZGU4ZTc5ODgxMDFhZGQzZDllMTkwNWRjY2ViMTUxZDVmZGI1NjYwYTE4MTVlMzkyYmRkOGEyYTE2MTJlZDZlZDgyMTg0YjkiLCJpYXQiOjE2ODY0MjExMzAuMjE1OTQyLCJuYmYiOjE2ODY0MjExMzAuMjE1OTQ4LCJleHAiOjE3MTgwNDM1MzAuMjA5MDgxLCJzdWIiOiIzMjgyNzMiLCJzY29wZXMiOltdfQ.gk0ipHN6WITXAIoMpgAYFptLXs2uLNhA2SSPULFJE783grLo78bh-EfroZts7E7Z_FvGn_tvyhvj2oGkTu3_hs20mpD_o7O8Koov7NZj4sibJBhi-dS7PXYPtRqSqDb_X9FLP-T0ccNTxWHreGl4ZA1q8hhzYHQzfn6Jgh6WwZsutvyq0X5NMHsBasLypr4BftmuxGG-sN5kl_sU4iIa_DKmOkr30azBJ4o_sQQ7maEfcZNfqCSp2Z5D6rCscTa9glGwpt1dPIRVOshcg2LcvEIH47eOHQniELDWxqeYQakdmrrR67OQcQ6JhC3xmXJ0JKaQOZ7uunit5-cwME3VWF_vD_WBgu3j3Q4Murs71t4EiMBBzxFQRiazF1n9HdYq86wN2Unu0SSdoWCLRzaT5h65xWkbQWDudO2jcuhDGC787SVRKOfsKUotaVVjH4FmhusksYvn4SHYJ-5h89jdrn7UAdB81SUXobhtPb1pQufJnNqKffY-7xqmXhz_g6AjwklhNL7VspTPAJ_D14DURvy_o3Zif2hCKDCn_7HMg403TZsOf-LpNcUnGg2gw9QzDfsQabMmXUKi4wumJxRIww9xLY2zss18h7rEBRl5U0YRMmbmWz40x3VfLIp5GPit3tc8MErqS_k2x3OXcY7gE9cLZOHwBfAlnWRYr_TuJtw",
 "user-agent":"Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"
}
H='h'
L='l'
rol = random.choice([H, L])
hl= rol
chance=random.randint(96,97)

di =90
bb=float(0.00000001)
if hl=="l":
        di=int(chance)
        rule='under'
        chn=chance
        bs=bb
else:
        di=int(chance)
        chn=99.99-di
        rule='over'
        bbs=bb

data3 = {
  "currency": "usdt",
  "game": "dice",
  "amount": 0.000001,                                        "rule": rule,
  "multiplier": round(float(99/di),4),
  "bet_value": chn
  }


#r1 = requests.post(url,headers=ua,data=data)
#dts=r1.json()
#print(dts)

#########

prndm = random.uniform(0.000008, 0.00002)

nls=random.randint(1,3)
rnd1=random.randint(3,6)
rnd2=random.randint(6,8)
rnd3=random.randint(9,12)
rnd4=random.randint(13,15)
rnd5=random.randint(15,17)
rnd6=random.randint(18,20)
rnd7=random.randint(21,23)

act=0

hrnd=random.randint(60,68)
ranlo=random.uniform(0.0008, 0.0012)
c = requests.session()
#bdp=random.randint(4)
#nwif = random.randint(4)
dely=random.randint(5,10)

url2='https://wolf.bet/api/v1/user/balances'
#get balance#
url='https://wolf.bet/api/v1/bet/place'
ua = {
 'X-Requested-With': 'XMLHttpRequest',
 'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1IiwianRpIjoiN2IwYTljNGE5ZGU4ZTc5ODgxMDFhZGQzZDllMTkwNWRjY2ViMTUxZDVmZGI1NjYwYTE4MTVlMzkyYmRkOGEyYTE2MTJlZDZlZDgyMTg0YjkiLCJpYXQiOjE2ODY0MjExMzAuMjE1OTQyLCJuYmYiOjE2ODY0MjExMzAuMjE1OTQ4LCJleHAiOjE3MTgwNDM1MzAuMjA5MDgxLCJzdWIiOiIzMjgyNzMiLCJzY29wZXMiOltdfQ.gk0ipHN6WITXAIoMpgAYFptLXs2uLNhA2SSPULFJE783grLo78bh-EfroZts7E7Z_FvGn_tvyhvj2oGkTu3_hs20mpD_o7O8Koov7NZj4sibJBhi-dS7PXYPtRqSqDb_X9FLP-T0ccNTxWHreGl4ZA1q8hhzYHQzfn6Jgh6WwZsutvyq0X5NMHsBasLypr4BftmuxGG-sN5kl_sU4iIa_DKmOkr30azBJ4o_sQQ7maEfcZNfqCSp2Z5D6rCscTa9glGwpt1dPIRVOshcg2LcvEIH47eOHQniELDWxqeYQakdmrrR67OQcQ6JhC3xmXJ0JKaQOZ7uunit5-cwME3VWF_vD_WBgu3j3Q4Murs71t4EiMBBzxFQRiazF1n9HdYq86wN2Unu0SSdoWCLRzaT5h65xWkbQWDudO2jcuhDGC787SVRKOfsKUotaVVjH4FmhusksYvn4SHYJ-5h89jdrn7UAdB81SUXobhtPb1pQufJnNqKffY-7xqmXhz_g6AjwklhNL7VspTPAJ_D14DURvy_o3Zif2hCKDCn_7HMg403TZsOf-LpNcUnGg2gw9QzDfsQabMmXUKi4wumJxRIww9xLY2zss18h7rEBRl5U0YRMmbmWz40x3VfLIp5GPit3tc8MErqS_k2x3OXcY7gE9cLZOHwBfAlnWRYr_TuJtw',
 'user-agent': 'hd',
# 'Content type': 'application/json',
}

rd = c.get(url2,headers=ua)
jsn1 = json.loads(rd.text)


########STARTING BALANCE ######

for i in jsn1['balances']:
        x =i.get('currency')
        if x == 'usdt' :
                sbalance = float(i.get('amount'))
                sbl=(f'{sbalance:.8f}')
print('currency : ','usdt')
print('starting balance ' ,sbl)
sbbl=float(sbl)

slepprofit=0.1*sbbl

print('TARGET SLEEP PROFIT' ,slepprofit)

def sm():
	for i in range(20):
	   sys.stdout.write("\r{0}>".format("-"*i))
	   sys.stdout.flush()
	   time.sleep(0.5)



#rd = c.get(url1,headers=ua1)
#jsn1 = json.loads(rd.text)
H='h'
L='l'
rol = random.choice([H, L])
hl= rol
chance=random.randint(35,48)

di =90
bb=float(0.0000001)

######DEFINE#####
no_wins2 = 0
no_wins=0
no_win = 0

no_loser = 0
no_lose=0
not_los=0
no_lose2=0

bet_no=0
betno4=0
betno3=0


betnoslep=0

#########
hunt=False
mk=False
no_losses=0
total_wins=0
total_loses=0

actt=0

chang_los=0
rantime=random.randint(1,3)
chngech1=random.randint(93,98)
chngech2=random.randint(2,4)
betno2=0
slptm=random.randint(45,55)

wage=float(0.00000000)
bg=float(0.00000000)
rbt=1.3

crp=float(0.00000000)
crp1=float(0.00000000)
crp2=float(0.00000000)
crp3=float(0.00000000)
crp4=float(0.00000000)
crp5=float(0.00000000)
tprof=(0.00000000)
crpp=0
if hl=="l":
        di=int(chance)
        rule='under'
        chn=chance
        bbs=bb
else:
        di=int(chance)
        chn=99.99-di
        rule='over'
        bbs=bb

data = {
  "currency": "usdt",
  "game": "dice",
  "amount": bb,
  "rule": rule,
  "multiplier": round(float(99/di),4),
  "bet_value": chn
  }
#r1 = c.post(url,headers=ua,data=data)
#jsn = json.loads(r1.text)
#  print(jsn)
#lws= jsn['bet']['state']
#wl= jsn['bet']['state']

abort_after = rantime * 3
start = time.time()
ath=0
print('current chance >>>',chance)
sup=0

lrn=7
wnt=False
mull= False
df=0
rsk=2
prcnt=2





bb = 0.0000051
chance = 66
minc = 9
maxc = 66
bb = bb
bethigh = False
multi = 1.12
multi2 = 1.25
somu1f1 = 0
somu2f1 = 1
somu1f2 = 1.74
somu2f2 = 1.62
point1 = 10
point2 = 15
f1 = True
profitf1 = 0
nx1 = 1
f1stw = 0
f1stl = 0
f1x = True
f2 = False
profitf2 = 0
nx2 = 1
f2st = 0
resetIfProfit = 0.0000001
base=0.000002


def is_reset_profit_reached():
    return profitf1 >= resetIfProfit or profitf2 >= resetIfProfit


adc=0.1

count=0
while True  :
 # print(type(chance))
 
 
  cch1=[10,30]
  ch1=random.choice(cch1)
  lsc =  [10,8]
  ch2=random.choice(lsc)
  lscy =  [10,15]
  ch3=random.choice(lscy)
  lscyw = [21,27]
  ch4=random.choice(lscyw)
  
  
  
  
  
  lscywr = [50,35]
  ch5=random.choice(lscywr)
  lscywrs = [4,8]
  lr = [15,20]
  ch7=random.choice(lr)
  lscywrs=[15,21,28,10]
  ch10=random.choice(lscywrs)
  H=(ch1)
  L=(ch2)
  M=(ch3)
  N=(ch4)
  chch = (random.choice([H, L,M,N]))
  chch1 = (random.choice([H, L,M,N]))
  chch2 = (random.choice([H, L,M,N]))

  brnd = random.uniform(0.001, 0.00158)

######WAGERING#####

  wage += bg
  bg=bb
  wg=float(format(wage, '.8f'))
  fnl_wg =(f"{wg:.8f}")
  
  if hl=="l":
        di=int(chance)
        rule='under'
        chn=chance
        bbs=bb
  else:
        di=int(chance)
        chn=99.99-di
        rule='over'
        bbs=bb

  data = {
  "currency": "usdt",
  "game": "dice",
  "amount": bb,
  "rule": rule,
  "multiplier": round(float(99/di),4),
  "bet_value": chn
  }
  
  data3 = {
  "currency": "usdt",
  "game": "dice",
  "amount": 0.00000001,
  "rule": rule,
  "multiplier": round(float(99/di),4),
  "bet_value": chn
  }
  
  
  r1 = c.post(url,headers=ua,data=data)
  jsn = json.loads(r1.text)
  
 
 # print(jsn)
  lws= jsn['bet']['state']
  wl= jsn['bet']['state']


  if wl =='loss':
        chang_los +=1
  else:
        chang_los = 0

  if lws=='loss':
        wnt=False
        win=False
        no_lose2+= 1
   #     not_los+=1
        no_lose += 1
        no_loser+=1
        no_losses += 1
        no_wins=0
        lw=(res+bred+str('Loss')+res)
  else:
        wnt=True
        win=True
        no_wins2 += 1
        no_win +=1
        no_wins +=1
        no_losses=0
        lw=(res+bgrn+str('Win ')+res)

  if hl =='l':
        trg='>>'
  else:
        trg='<<'

  if lws == 'win' or lws == 'loss':
        bet_no +=1
        betno2 +=1
        betno3 =betno3+1
        betno4 +=1
        betnoslep +=1

  if no_wins > total_wins:
           stats_rolebet_win = True
           stats_rolebet_lose = False
           total_wins +=1
  #         chang_los =0

  if no_losses > total_loses:
           stats_rolebet_lose = True
           stats_rolebet_win = False
           total_loses +=1
   #        chang_los +=1
           no_lose2 += 1

  cur_prof=float(jsn['bet']['profit'])

  betam= float(jsn['bet']['amount'])
  beta= float(format(betam, '.8f'))
  betamo=(f"{beta:.8f}")
  
  crnc= jsn['bet']['currency']
  chnc=float(jsn['bet']['bet_value'])
  chnce=float(format(chnc, '.2f'))
  trgchnc =float(f"{chnce:.2f}")
  resl=jsn['bet']['result_value']
  user_bal= float(jsn['userBalance']['amount'])
  ub=float(format(user_bal, '.8f'))
  usr_bl =float(f"{ub:.8f}")

  profit=(usr_bl-sbbl)
  a=float(format(profit, '.8f'))
  prof=(f"{a:.8f}")

  
        
  cur_pro = float(format(cur_prof , '.8f'))
  cur_pr =(f"{cur_pro:.8f}")
#  print(cur_pr   )
  crp1=float(cur_pr)
  crp2 +=crp1
  crp3+=crp1
  crp   += crp1
  crp5 +=crp1
  crpp +=crp1
#  crp1=float(cur_pr)
#  crp3=float(format(crp, '.8f'))
 # crp4 =(f"{crp3:.8f}")
 # print(crp4)
 # crp5=float(crp4)
  tprf=((format(crp3, '.8f')))
  prft=((format(crp2, '.8f')))
  
  if float(prft) > 0.00000000:
        clr=(res+bgrn)
  else:
        clr=(res+bred)

  #### PRINTING RESULTS ####

 # print('')

  print(lw , '|', res+bcy+str(betamo)+res , '|', res+byel+'BL:',res+bwh+ str(usr_bl)+res, '|', res+bwh+'PF:',clr+str( prft)+res+' '+str(trgchnc)+''+ str(trg) +''+ str(resl)+' ')
  
  
  
  
#prof
#  print(res+bwh+'WS -'+res+bgrn+str( total_wins)+ '|'+ res+bwh+'LS -'+ res+bred+str(total_loses)+ '|' ,res+bwh+'Profit :',clr+str( prof)+res,'|', '|', res+lblk4+' Total Bet :',str(bet_no ) +res)

 # print(chang_los)


  
  
  rnm=random.randint(1,3)
  rnm2=random.randint(1,10)
  rnm3=random.randint(1,7)
  #adc=0.5
  
  if float(crp5)<=-0.001:
  	adc=adc+(random.uniform(0.1,0.59))
  	adc=float(adc)
  #	print(adc)
  else:
  	pass
  	
  if adc>=25:
  	adc=0.5
  else:
  	pass
  	
  ch55=[10,21]
  ch55=int(random.choice(ch55))
  ch1=5
  ch2=14
  ch3=8
  ch4=(ch55)
  chance = [ch1,ch2,ch3,ch4]
  selected_value = random.choices(chance, weights=[15, 3.5, 7, 1.4 + adc])[0]
  chance= float(selected_value)
  
  if chance==ch1 and wnt:
  	bb=bb*1.3
  	bb=float(format(bb, '.8f'))  	
  else:
  	pass
  	
  if chance==ch2 and wnt:
  	bb=bb*1.25
  	bb=float(format(bb, '.8f'))  	
  else:
  	pass
  	
  if chance==ch3 and wnt:
  	bb=bb*1.4
  	bb=float(format(bb, '.8f'))  	
  else:
  	
  	if float(prft)<=-0.0001 and bb>=0.0001:
  		if count < 5:
  			bb *= random.uniform(1,1.2)
  		elif 5 <= count < 15 :
  			bb += 0.000001
  		
  		else:
  			count = 0
  		bb = float(format(bb, '.8f'))
  		count += 1
  	else:
  		pass
  	
  	
 #######PROFIT RESET#######
 
 
  	
  
  	
  if crp5>=0:
     crp5=0.00000000
     print("RESET ACTIVATED")
     bb=0.00001
     random_choice = random.choice(['h', 'l'])
     hl=(random_choice)
     rbt=random.uniform(1.2,1.282)
     lrn=random.randint(5,10)
     rsk=random.randint(10,20)
     prcnt=random.randint(3,5)
  else:
  	pass
  	
  
  	
  sys.stdout.write(res+'  ' +res+bmag+str(crnc)+res+' | '+' '+bgrn+' Wagered :'+res+bwh+ str(fnl_wg) +res+res+bcy+' ' +'Bet: '+str(bet_no)+' ' +res+'total profit : '+ str(tprf)+' '+"\r")
  	
  if betno2>=random.randint(1011,1876):
  	betno2=0
  	cs()
  else:
  	pass
  	

  	
  	
  
  
  	
  if float(prft)>=0.00105:
        a=0.000000000
        crp2=0.00000000
        prft=0.00000000
        tprof+=float(prof)
        b=sbbl+float(prof)
        e=float(format(b, '.8f'))
        end_bl =(f"{e:.8f}")
        random_choice = random.choice(['h', 'l'])
        hl=(random_choice)
        print('')
        print('HEY !!! TARGET PROFIT HAS REACHED')
        print('STARTING BALANCE :', sbbl)
        print('ENDING BALANCE :' , end_bl)
        print('TOTAL PROFIT :', prof)
  #      print('TOTAL PROFIT :', tprof)
        print('TOTAL WAGERD :', fnl_wg)
   #     sm()
  #      time.sleep(random.randint(1,3))
        print('')
        
        print('READY FOR NEXT SESSION')
        print('')
        
    #    time.sleep(random.randint(20,50))
   
  else:
  	pass
  	
  if crpp>=float(slepprofit) :
  	crpp=0.00000000
  	slepprofit=0.1
  	print('GOT TARGET PROFIT AND ITZ TIME FOR SLEEP')
  	time.sleep(random.randint(10,30))
  	print('')
  	
  else:
  	pass
  	
  if betnoslep>=random.randint(28000,35000) and float(prft)>=0.0000001:
  	betnoslep=0
  	time.sleep(random.randint(120,280))
  	print('')
  	print('REACHED TAREGET BET NUMBER , AND ITZ TIME FOR SLEEP')
  else:
  	pass
  	
  	
  	
  	
  	
  	
 ###₹₹MAIN THING###₹#
 
  
        
   
  
        
        
'''
timeout = random.randint(67,98) # [seconds]
        timeout_start = time.time()
        
        while time.time() < timeout_start + timeout:
        	test = 0
        	if test == 5:
        		
        		prft=0.00000000
        		print('READY FOR NEXT SESSION')
        		break
        	test -= 1
        	r3= c.post(url,headers=ua,data=data3)
        	jsn3 = json.loads(r3.text)
        	wl3= jsn3['bet']['state']
        	betam3= float(jsn3['bet']['amount'])
        	beta3= float(format(betam3, '.8f'))
        	betamo3=(f"{beta3:.8f}")
        	print(wl3,' >> ',betamo3)
rnm=random.randint(1,99)
  if rnm >= 60:
  	mlt=1.8
  elif rnm <= 40:
  	mlt=1.2
#  elif rnm >= 21 and rnm <=50:
#  	mlt=1
  else:
  	mlt=1.22
  
  
  if betno3%random.randint(1,4)==0 and rnm<=50:
  	
  	mul=random.uniform(1.1,1.162)
  	bb1=(bb * mul)
  	bb=float(format(bb1, '.8f'))
  	
  	
#  	print('rnm1')
 # 	no_wins=0
  	bb1=(bb *(1.061))
#  	bb=float(format(bb1, '.8f'))
  	chance=ch1
  #	not_los+=1
  	
  elif betno3%2==0 and rnm>=80:
#  	print('rnm2')
  #	no_lose2=0
  	bb1=(bb * random.uniform(1.12,1.16))
#  	bb=float(format(bb1, '.8f'))
  	chance=random.randint(10,16)
  else:
  	chance=chance
  	
  	
  if float(usr_bl) >ath:
  	ath=float(usr_bl)
  else:
  	pass
  '''
 #  	bb=0.0001 #float(format(bb+random.uniform(0.000015,0.0001), '.8f')))))))))))))))8f'))))))))))))))))))))))))f'))))))))))))))))))))))))))))).uniform(0.000015,0.0001), '.8f')))))))))))))))8f'))))))))))))))))))))))))f'))))))))))))))))))))))))))))))))))))))))))).uniform(0.000015,0.0001), '.8f')))))))))))))))8f'))))))))))))))))))))))))f'))))))))))))))))))))))))))))))))))))))))8f')))))))))))))))8f'))))))))))))))))))))))))f'))))))))))))))))))))))))))))).uniform(0.000015,0.0001), '.8f')))))))))))))))8f'))))))))))))))))))))))))f'))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))f')))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))8f'))))))))))))))))))))))))f'))))))))))))))))))))))))))))))))))))))))))).uniform(0.000015,0.0001), '.8f')))))))))))))))8f'))))))))))))))))))))))))f'))))))))))))))))))))))))))))))))))))))))8f')))))))))))))))8f'))))))))))))))))))))))))f'))))))))))))))))))))))))))))).uniform(0.000015,0.0001), '.8f')))))))))))))))8f'))))))))))))))))))))))))f'))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))f'))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))f'))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))f')))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))