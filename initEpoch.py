# this tool is provided free of charges by BREIZHSTAKEPOOL.IO [BZH], proud member of Cardano Single Pool Alliance (CSPA)
# to help us improve our work, PLEASE CONSIDER A DONATION and/or DELEGATION to our pool [BZH]
#
# [BZH] pool ID : 9b9ad921921db31ca91cd6dfdf11f5efee8c1ab94671a6b4a8edc748
#
# Cardano donation address : addr1qxm3yvr95pvdm3zzjs6mtqagqzz9yvjt0tr9sqgkte7nzk857qxww9fmak8jkfyr04jzvfra5cxnsrdurmueqy7spdwsmezjvm
#
# Bitcoin donation address : bc1qm3gjk0e9c9weqg4dtc5lpk9vs3nd0380d5cw4e
#
# report bugs and issues at : https://github.com/ArbrazLinux
# join our telegram chat room : t.me/bzhpool
# website : https://breizhstakepool.io

from os.path import exists as file_exists
import pycurl
import json
import array
from functions import getRewards
from config import POOL_ID, PROJECT_ID
from colors import colors

def initEpoch(NewEpoch):
	Nepoch = NewEpoch
	Oepoch = Nepoch - 1
	xx='"'
#POOL_ID = 'pool1nwddjgvjrke3e2gu6m0a7y04alhgcx4egec6dd9gahr5sz0p5u9'
#PROJECT_ID = "mainnetHmhzKZwL7qCKqG1srdmrq3WH6hC6It0Y"

	urlQuery1 = "https://cardano-mainnet.blockfrost.io/api/v0/epochs/{}/stakes/{}".format(Nepoch,POOL_ID)

	if not (file_exists("data/list/list_{}.json".format(Nepoch))):
		print("NEW EPOCH")
		with open("data/list/list_{}.json".format(Nepoch), "wb") as outfile:
			curl = pycurl.Curl()
			curl.setopt(curl.HTTPHEADER, ['-H',"project_id:{}".format(PROJECT_ID)])
			curl.setopt(curl.URL, "{}".format(urlQuery1))
			curl.setopt(curl.WRITEDATA, outfile)
			curl.perform()
			curl.close()
		outfile.close()

	if (file_exists("data/list/list_{}.json".format(Oepoch))):
		with open("data/list/list_{}.json".format(Oepoch)) as json_file:
			OldList = json.load(json_file)
			OldDeleg=[]
			Ol = len(OldList)
			a = 0
			while (a < Ol):
				add = OldList[a]["stake_address"]
				OldDeleg.insert(a,add)
				a+=1
		json_file.close()
	else:
		OldDeleg=[]
		Ol=0

	with open("data/list/list_{}.json".format(Nepoch)) as json_file:
		NewList = json.load(json_file)
		json_file.close()

	Nl = len(NewList)
	NewDeleg=[]
	NewDeleg_string=[]
	a = 0

	while (a < Nl):
		add = NewList[a]["stake_address"]
		NewDeleg.insert(a,add)
		NewDeleg_string.insert(a,'')
		a+=1
	k=0
	i=0
	IncomingDeleg=[]

	for d in NewDeleg:
		if d in OldDeleg:
#			print(d, "STAYING")
			e=0
		else:
#			print(d, "INCOMING")
			i=NewDeleg.index(d)
			IncomingDeleg.insert(k,i)
			k+=1
	print("__________________________________________")
	k=0
	i=0
	LeavingDeleg=[]

	for d in OldDeleg:
		if d in NewDeleg:
#			print(d, "STAYING")
			e=0
		else:
#			print(d, "LEAVING") 
			i=OldDeleg.index(d)
			LeavingDeleg.insert(k,i)
			k+=1

	if (Nl >= Ol):
		maxI=Nl
	else:
		maxI=Ol

	deleg_address=[]
	deleg_stake_current=[]
	deleg_stake_previous=[]
	deleg_stake_diff=[]
	deleg_stake_lost=[]
	deleg_rewards=[]
	deleg_sinceEpoch=[]
	deleg_firstEpoch=[]
	deleg_lastEpoch=[]
	deleg_status=[]
	backCount=[]

	i=0
	while (i < maxI):
		deleg_address.insert(i,'')
		deleg_stake_current.insert(i,0)
		deleg_stake_previous.insert(i,0)
		deleg_stake_diff.insert(i,0)
		deleg_stake_lost.insert(i,0)
		deleg_rewards.insert(i,0)
		deleg_sinceEpoch.insert(i,0)
		deleg_firstEpoch.insert(i,0)
		deleg_lastEpoch.insert(i,0)
		deleg_status.insert(i,'')
		backCount.insert(i,0)
		i+=1
	i = 0
	j = Ol - 1
	k = Nl - 1
	check = 0
	check_numb = Ol
	newindex = 0

	h=0
	if (file_exists("data/epoch/Epoch_{}.json".format(Oepoch))):
		with open("data/epoch/Epoch_{}.json".format(Oepoch)) as json_file:
			OldEpoch = json.load(json_file)
			json_file.close()
	else:
		epoch_file = open("data/epoch/Epoch_{}.json".format(Oepoch), "w")
		epoch_file.write("[]")
		epoch_file.close()

	n=0
	while (i <= j):
		a=0
		b=n
		OldDeleg_address=OldList[i]["stake_address"]
		NewDeleg_address=NewList[n]["stake_address"]

		for g in LeavingDeleg:
			if (g == i):
#				OldDeleg_address=OldList[i]["stake_address"]

				deleg_address[i]=OldDeleg_address
				deleg_stake_lost[i]=str(OldList[i]["amount"])
				deleg_sinceEpoch[i]=OldEpoch[i]["since_epoch"]
				if (file_exists("data/gone_delegators.json")):
					with open("data/gone_delegators.json") as json_file:
						Gones = json.load(json_file)
						json_file.close()
					GoneL = len(Gones["gone_delegators"])
					gL = GoneL - 1
					Gone_address=[]
					c=0
					while (c<GoneL):
						Gone_address.insert(c,'')
						c+=1
					while (gL >= 0):
						Gone_address[gL]=Gones["gone_delegators"][gL]["gone"]

						if (Gone_address[gL] == OldDeleg_address):
							backCount[i]=Gones["gone_delegators"][gL]["back_count"]+1
							deleg_firstEpoch[i]=Gones["gone_delegators"][gL]["first_epoch"]

							break
						else:
							backCount[i]=0
							deleg_firstEpoch[i]=deleg_sinceEpoch[i]

						gL-=1
				else:
					backCount[i]=0
				if (backCount[i] > 0):
					print(colors.fg.blue,"\n STAKEHOLDER",colors.reset, deleg_address[i],colors.fg.red, "LEAVING AGAIN : ",colors.reset, backCount[i], "times")
				else:
					print(colors.fg.blue,"\n STAKEHOLDER",colors.reset, deleg_address[i],colors.fg.red, "LEAVING",colors.reset)
				deleg_lastEpoch[i]=str(Oepoch)
				deleg_sinceEpoch[i]=str(deleg_sinceEpoch[i])
				deleg_firstEpoch[i]=str(deleg_firstEpoch[i])
				backCount[i]=str(backCount[i])
				deleg_status[i]="GONE"
				check_numb-=1
#				i+=1
				break
#		print(NewDeleg_address)
#		print(OldDeleg_address)
		if (NewDeleg_address != OldDeleg_address):
			a=0
			while (NewDeleg_address != OldDeleg_address and a < k):
				a+=1
#				print(a)
				NewDeleg_address=NewList[a]["stake_address"]
			b=a
		if (NewDeleg_address == OldDeleg_address):
			check+=1
			print("CHECK :", check,"/",check_numb)
			print(colors.fg.blue,"STAKEHOLDER :",colors.reset, NewDeleg_address, colors.fg.green,"STAY",colors.reset)
#			print(deleg_address)
			deleg_address[i]=NewDeleg_address
			deleg_stake_current[i]=NewList[b]["amount"]
			deleg_stake_previous[i]=OldList[i]["amount"]
			dsc=int(deleg_stake_current[i])
			dsp=int(deleg_stake_previous[i])
			deleg_stake_diff[i]=dsc-dsp
			deleg_stake_diff[i]=str(deleg_stake_diff[i])
			deleg_rewards[i]=str(getRewards(NewDeleg_address, Nepoch))
			deleg_sinceEpoch[i]=str(OldEpoch[i]["since_epoch"])
			deleg_lastEpoch[i]=str(OldEpoch[i]["gone_epoch"])
			deleg_status[i]="STAY"
			if (i == 0):
				newEpoch_string="["
			g=0
			dG=[]

			while ( g < Nl ):
				dG.insert(g, NewList[g]["stake_address"])

				if (dG[g] == NewDeleg_address):
					NewDeleg_string[g]='{"address":'+xx+deleg_address[i]+xx+', "current_stake": '+deleg_stake_current[i]+', "previous_stake": '+deleg_stake_previous[i]+', "diff": '+deleg_stake_diff[i]+', "rewards": '+deleg_rewards[i]+', "since_epoch": '+deleg_sinceEpoch[i]+', "gone_epoch": '+deleg_lastEpoch[i]+', "status": '+xx+deleg_status[i]+xx+"}"
					break
				g+=1
			n+=1
		i+=1
	i=0
	LeavingDelegN=len(LeavingDeleg)

	if (LeavingDelegN > 0):
		if (file_exists("data/gone_delegators.json")):
			with open("data/gone_delegators.json") as file:
				gone_string=json.load(file)
				gone_string=json.dumps(gone_string)
				gone_string=gone_string[0:-2]+","
			file.close()
		else:
			gone_string='{"gone_delegators": ['
	else:
		gone_string=''
	i=0
	maxG=LeavingDelegN - 1

	while (i < LeavingDelegN):
		print("STAKEHOLDER :",deleg_address[LeavingDeleg[i]])
		deleg_status[i]="GONE"
		if (i < maxG):
			gone_string=gone_string+'{"gone":'+xx+deleg_address[LeavingDeleg[i]]+xx+',"back_count":'+backCount[LeavingDeleg[i]]+',"first_epoch":'+deleg_firstEpoch[LeavingDeleg[i]]+',"since_epoch":'+deleg_sinceEpoch[LeavingDeleg[i]]+',"last_epoch":'+deleg_lastEpoch[LeavingDeleg[i]]+',"last_index":'+str(LeavingDeleg[i])+',"lost_stake":'+deleg_stake_lost[LeavingDeleg[i]]+"},"
		else:
			gone_string=gone_string+'{"gone":'+xx+deleg_address[LeavingDeleg[i]]+xx+',"back_count":'+backCount[LeavingDeleg[i]]+',"first_epoch":'+deleg_firstEpoch[LeavingDeleg[i]]+',"since_epoch":'+deleg_sinceEpoch[LeavingDeleg[i]]+',"last_epoch":'+deleg_lastEpoch[LeavingDeleg[i]]+',"last_index":'+str(LeavingDeleg[i])+',"lost_stake":'+deleg_stake_lost[LeavingDeleg[i]]+"}]}"
		i+=1
	if (LeavingDelegN > 0):
		with open("data/gone_delegators.json", "w") as file:
			file.write(gone_string)
			file.close()

	i=0
	IncomingDelegN=len(IncomingDeleg)

	goneDeleg=[]
	goneEpoch=[]
	backDeleg=[]
	backDeleg_lastEpoch=[]
	backDeleg_lastIndex=[]
	backDeleg_lastStake=[]
	newindex=0
	incomingDeleg_stake=0
	incomingDeleg_status=''

	while (i < IncomingDelegN):
		check+=1
		check_numb+=1
		print("CHECK :",check,"/",check_numb)
		delegB=NewList[IncomingDeleg[i]]["stake_address"]
		backDeleg.insert(i,'')
		backDeleg_lastEpoch.insert(i,0)
		backDeleg_lastIndex.insert(i,0)
		backDeleg_lastStake.insert(i,0)

		if (file_exists("data/gone_delegators.json")):
#			print("CHECK COMING BACK")
			with open("data/gone_delegators.json") as json_file:
				Gones = json.load(json_file)
				json_file.close()
			GoneL=len(Gones["gone_delegators"])
			cb=GoneL - 1
			w=0
			while (w < GoneL):
				goneDeleg.insert(w,'')
				goneEpoch.insert(w,0)
				w+=1
			while (cb >= 0):
				goneDeleg[cb]=Gones["gone_delegators"][cb]["gone"]
				if (delegB == goneDeleg[cb]):
					goneEpoch[cb]=Gones["gone_delegators"][cb]["last_epoch"]
					if (goneEpoch[cb] < Nepoch):
						backDeleg[i]=goneDeleg[cb]
						backDeleg_lastEpoch[i]=goneEpoch[cb]
						backDeleg_lastIndex[i]=Gones["gone_delegators"][cb]["last_index"]
						backDeleg_lastStake[i]=Gones["gone_delegators"][cb]["lost_stake"]
						break
				cb-=1
		if (delegB == backDeleg[i]):
			print(colors.fg.blue,"STAKEHOLDER",colors.reset, delegB,colors.fg.purple, "COMING BACK",colors.reset)
			incomingDeleg_status="BACK"
			lastEpoch=int(backDeleg_lastEpoch[i])
			diffEpoch=Nepoch-lastEpoch
			previous=int(backDeleg_lastStake[i])
		else:
			print(colors.fg.blue,"STAKEHOLDER",colors.reset, delegB,colors.fg.orange, "NEW DELEGATOR",colors.reset)
			incomingDeleg_status="NEW"
			previous=0

		stake=int(NewList[IncomingDeleg[i]]["amount"])
		diff=stake-previous
		since=str(Nepoch)
		rewards=str(getRewards(delegB, Nepoch))
		g=0
		ndG=[]
		while (g < Nl):
			ndG.insert(g, NewDeleg[g])
			if (ndG[g] == delegB):
				NewDeleg_string[g]='{"address":'+xx+delegB+xx+', "current_stake": '+str(stake)+', "previous_stake": '+str(previous)+', "diff": '+str(diff)+', "rewards": '+rewards+', "since_epoch": '+since+', "gone_epoch": '+str(deleg_lastEpoch[i])+', "status": '+xx+incomingDeleg_status+xx+"}"
				break
			g+=1

		i+=1
		newindex+=1


	epoch_string=str(NewDeleg_string).replace("'","")


	data_file = open("data/epoch/Epoch_{}.json".format(Nepoch), "w")
	data_file.write(epoch_string)
	data_file.close()

