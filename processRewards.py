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

import pycurl
import json
from initEpoch import initEpoch
from setPoolData import setOwnersIndex, setDelegsIndex
from functions import getRewards, checkBonus, setROA, checkGoneAndLost, checkBlocks, checkBiggest
from functions_2 import getHistFile
from config import POOL_ID, POOL_TICKER, REGISTRATION_EPOCH, OWNERS_STAKE_ADDRESS
from colors import colors


def checkRewardedEpoch(Epoch):
	with open("data/blocksList.json") as json_file:
		b_list = json.load(json_file)
		json_file.close()
	check=[]; check.insert(0,0)
	a=0; b=0
	blocks_N = len(b_list["block"])
	i = blocks_N - 1
	while (i > 0):
		bl_epoch = b_list["block"][i]["epoch"]
		if (bl_epoch >= Epoch - 2 and bl_epoch <= Epoch):
			if (check[a] == bl_epoch):
				i -=1
				continue
			else:
				if (a > 0 or b == 1):
					a+=1
					check.insert(a, bl_epoch)
				else:
					check[a]= bl_epoch
					b = 1

				i-=1
				continue
		elif (bl_epoch > Epoch):
			i-=1
			continue
		else:
			i-=1
			break
	print(check)
	return check

def checkRewardsStatus(currentEpoch):
	block_check = checkRewardedEpoch(currentEpoch)
	updating = []; uEpoch = []; uFile = []; uIndex = []

	if (block_check[0] != 0):
		bl_N = len(block_check) - 1
		u = 0
		while (bl_N >= 0):
			bl_epoch = block_check[bl_N]
			uEpoch.insert(u, bl_epoch)
			updating.insert(u, False)
			hist = getHistFile(bl_epoch, currentEpoch)
			print(hist)
			Hfile = hist[1]
			uFile.insert(u, Hfile)
			Hindex = hist[2]
			uIndex.insert(u, Hindex)
			with open(Hfile) as json_file:
				Hdata = json.load(json_file)
				json_file.close()

			if (hist[0] is False):
				print("in current data --> file :", hist[1]," | index :", hist[2])
				R_Hdata = Hdata["history"][Hindex]
			else:
				print("in history data --> file :", hist[1]," | index :", hist[2])
				R_Hdata = Hdata[Hindex]
			Hepoch = R_Hdata["epoch"]
			print(Hepoch)
			Hrewards = R_Hdata["pool"]["rewards"]["_epoch_"]
			if (Hrewards == 0):
				print("pas encore reçu les rewards")
				O_add = R_Hdata["owners"]["owner"][0]["stake_address"]
				O_rewards = getRewards(str(O_add), Hepoch)
				if (int(O_rewards) > 0):
					print("rewards dispos")
			#		initEpoch(Hepoch)
					updating[u] = True
				else:
					print("rewards pas encore dispos")
			else:
				print("rewards déjà calculés")
				print("total rewards :", Hrewards)
			bl_N -= 1
			u += 1
	else:
		print("pas de blocs ==> pas de rewards !")
	upd = updating, uEpoch, uFile, uIndex
	print(upd)
	return upd

def processRewards(currentEpoch):
	updatingList = checkRewardsStatus(currentEpoch)
	updatingNext = False
	updatedLast = [False, '', 0]
	N = len(updatingList[0])
	i = 0
	while (i < N):
		if (updatingList[0][i] != False or updatingNext == True):
			update_epoch = updatingList[1][i]
			update_file = updatingList[2][i]
			update_index = updatingList[3][i]
			print("updating epoch", update_epoch)
			updatingNext = True
			updateRewardsHistory(update_epoch, update_file, update_index, updatedLast)
			updatedLast = [True, update_file, update_index]
		else:
			print("not updating epoch", updatingList[1][i])
		i += 1




def updateRewardsHistory(epoch, file, index, previousUpdated):
	cc = "'"
	xx = '"'
	with open(file) as json_file:
		history_data = json.load(json_file)
		json_file.close()
	if (file == "data/pool_data.json"):
		H_data = history_data["history"][index]
	else:
		H_data = history_data[index]

	with open("data/epoch/Epoch_{}.json".format(epoch)) as json_file:
		epoch_data = json.load(json_file)
		json_file.close()
	D_strg = ''; O_strg = ''; D_rewards = 0; D_rewards_sum = 0; D_bonus_sum = 0; P_rewards = 0; P_rewards_sum = 0; O_rewards = 0; O_rewards_sum = 0
	N = len(epoch_data)
	i = 0; d_list = []
	Nh = len(H_data["delegators"]["delegator"])
	dH_data = H_data["delegators"]["delegator"]
	delegators_H_data = H_data["delegators"]
	Oh = len(H_data["owners"]["owner"])
	oH_data = H_data["owners"]["owner"]
	owners_H_data = H_data["owners"]
	while (i < N):
		d_list.insert(i, '')
		d_list[i] = epoch_data[i]["address"]
		i += 1
	i = 0
	while (i < Nh):
		stk = H_data["delegators"]["delegator"][i]["stake_address"]
		if stk in d_list:
			d_index = d_list.index(stk)
		H_STRG = H_data["delegators"]["delegator"][i]

		if (previousUpdated[0] == False):
			print("epoch précédente non-mise à jour")
			d_rewards_sum = H_STRG["rewards"]["_sum_"]

		else:
			print("epoch précédente mise à jour")
			Uepoch = epoch - 1
			p_file = previousUpdated[1]
			with open(p_file) as json_file:
				pH_data = json.load(json_file)
				json_file.close()
			if (p_file == "data/pool_data.json"):
				upH_data = pH_data["history"][previousUpdated[2]]
				print("current")
			else:
				upH_data = pH_data[previousUpdated[2]]
				print("history")

			Uepoch_data = upH_data["delegators"]["delegator"]

			N = len(Uepoch_data)
			d = 0; ud_list = []
			while (d < N):
				ud_list.insert(d, '')
				d += 1
			d=0
			while (d <N):
				ud_list[d] = Uepoch_data[d]["stake_address"]
				d += 1

			print(ud_list)
			if stk in ud_list:
				ud_index = ud_list.index(stk)
				print("in list")
				d_rewards_sum = upH_data["delegators"]["delegator"][ud_index]["rewards"]["_sum_"]
				testA = upH_data["delegators"]["delegator"][ud_index]["stake_address"]
				testS = upH_data["delegators"]["delegator"][ud_index]["stake"]["_epoch_"]
				print(stk, testA, testS, d_rewards_sum)
			else:
				print("not in list")
				print(stk, d_rewards_sum)
				#check if NEW delegator or BACK delegator
				d_status = epoch_data[d_index]["status"]
				if (d_status == "NEW"):
					d_rewards_sum = 0
					print("NEW DELEGATOR")
				elif (d_status == "BACK"):
					bd_lastIndex = 0
					bd_lastEpoch = epoch_data[d_index]["gone_epoch"]
					with open("data/gone_delegators.json") as json_file:
						gones_json = json.load(json_file)
						json_file.close()
					gones = gones_json["gone_delegators"]
					GN = int(len(gones)) - 1
					while (GN >= 0):
						backD_addr = gones[GN]["gone"]
						if (backD_addr == stk and bd_lastEpoch == gones[GN]["last_epoch"]):
							bd_lastIndex = gones[GN]["last_index"]
							break
						GN -= 1
					pruneDist = float((epoch - REGISTRATION_EPOCH - 2)/PRUNE_NB)
					pruneD = (REGISTRATION_EPOCH + 2) + int(pruneDist)*PRUNE_NB
					pruneF = pruneD + (PRUNE_NB - 1)
					if (backD_lastEpoch < pruneF):
						distD = float((int(backD_lastEpoch) - REGISTRATION_EPOCH - 2)/PRUNE_NB)
						dH = 245 + int(distD)*PRUNE_NB
						fH = dH + (PRUNE_NB - 1)
						bd_hIndex = fH - int(backD_lastEpoch)
						with open("data/history/pooldata_{}_{}.json".format(dH, fH)) as json_file:
							bd_data = json.load(json_file)
							json_file.close()
						bd_H_data = bd_data[int(bd_hIndex)]["delegators"]["delegator"][int(backD_lastIndex)]
					else:
						bd_H_data = bd_data["history"][int(bd_hIndex)]["delegators"]["delegator"][int(backD_lastIndex)]

					d_rewards_sum = bd_H_data["rewards"]["_sum_"]
					print("BACK DELEGATOR")

		d_rewards = epoch_data[d_index]["rewards"]
		d_rewards_sum = int(d_rewards_sum) + int(d_rewards)
		d_rewards_STRG = "{ '_epoch_': "+str(d_rewards)+", '_sum_': "+str(d_rewards_sum)+"}"
		H_rewards_STRG = H_STRG["rewards"]
		d_STRG = str(H_STRG).replace(str(H_rewards_STRG), d_rewards_STRG)
		d_stake_sum = H_STRG["stake"]["_sum_"]
		d_bonus_sum = H_STRG["bonuses"]["_sum_"]
		d_epochCount = H_STRG["epoch_count"]
		d_ROA = setROA(d_epochCount, d_stake_sum, d_rewards_sum, d_bonus_sum)
		H_ROA_max = H_STRG["ROA"]["_max_"]
		if (d_ROA[0] > H_ROA_max):
			d_ROA_max = d_ROA[0]
		else:
			d_ROA_max = H_ROA_max

		d_ROA_STRG = "{ '_lifetime_': "+str(d_ROA[0])+", '_max_': "+str(d_ROA_max)+", '_bonus_included_': "+str(d_ROA[1])+"}"
		H_ROA_STRG = H_STRG["ROA"]
		d_STRG = str(d_STRG).replace(str(H_ROA_STRG), d_ROA_STRG)

#		print(d_STRG)
		D_strg = D_strg+d_STRG+",\n"
		D_rewards = D_rewards + d_rewards
		D_rewards_sum = D_rewards_sum + d_rewards_sum
		D_bonus_sum = D_bonus_sum + d_bonus_sum
		i += 1
	j = 0
	while (j < Oh):
		stk = H_data["owners"]["owner"][j]["stake_address"]
		if stk in d_list:
			d_index = d_list.index(stk)
		H_STRG = H_data["owners"]["owner"][j]

		if (previousUpdated[0] == False):
			print("epoch précédente non-mise à jour")
			o_rewards_sum = H_STRG["rewards"]["_sum_"]

		else:
			print("epoch précédente mise à jour")
			Uepoch = epoch - 1
			p_file = previousUpdated[1]
			with open(p_file) as json_file:
				pH_data = json.load(json_file)
				json_file.close()
			if (p_file == "data/pool_data.json"):
				upH_data = pH_data["history"][previousUpdated[2]]
				print("current")
			else:
				upH_data = pH_data[previousUpdated[2]]
				print("history")


			Uepoch_data = upH_data["owners"]["owner"]

			N = len(Uepoch_data)
			d = 0; ud_list = []
			while (d < N):
				ud_list.insert(d, '')
				d += 1
			d=0
			while (d <N):
				ud_list[d] = Uepoch_data[d]["stake_address"]
				d += 1

			if stk in ud_list:
				ud_index = ud_list.index(stk)
				print("in list")
				o_rewards_sum = upH_data["owners"]["owner"][ud_index]["rewards"]["_sum_"]
				testA = upH_data["owners"]["owner"][ud_index]["stake_address"]
				testS = upH_data["owners"]["owner"][ud_index]["stake"]["_epoch_"]
				print(stk, testA, testS, d_rewards_sum)
			else:
				print("not in list")
				print(stk, d_rewards_sum)
				#check if NEW delegator or BACK delegator
				o_status = epoch_data[d_index]["status"]
				if (o_status == "NEW"):
					o_rewards_sum = 0
					print("NEW DELEGATOR")
				elif (o_status == "BACK"):
					bo_lastIndex = 0
					bo_lastEpoch = epoch_data[d_index]["gone_epoch"]
					with open("data/gone_delegators.json") as json_file:
						gones_json = json.load(json_file)
						json_file.close()
					gones = gones_json["gone_delegators"]
					GN = int(len(gones)) - 1
					while (GN >= 0):
						backO_addr = gones[GN]["gone"]
						if (backO_addr == stk and bo_lastEpoch == gones[GN]["last_epoch"]):
							bo_lastIndex = gones[GN]["last_index"]
							break
						GN -= 1
					pruneDist = float((epoch - REGISTRATION_EPOCH - 2)/PRUNE_NB)
					pruneD = (REGISTRATION_EPOCH + 2) + int(pruneDist)*PRUNE_NB
					pruneF = pruneD + (PRUNE_NB - 1)
					if (backO_lastEpoch < pruneF):
						distD = float((int(backO_lastEpoch) - REGISTRATION_EPOCH - 2)/PRUNE_NB)
						dH = 245 + int(distD)*PRUNE_NB
						fH = dH + (PRUNE_NB - 1)
						bd_hIndex = fH - int(backO_lastEpoch)
						with open("data/history/pooldata_{}_{}.json".format(dH, fH)) as json_file:
							bo_data = json.load(json_file)
							json_file.close()
						bo_H_data = bo_data[int(bd_hIndex)]["owners"]["owner"][int(backO_lastIndex)]
					else:
						bo_H_data = bo_data["history"][int(bd_hIndex)]["owners"]["owner"][int(backO_lastIndex)]

					o_rewards_sum = bo_H_data["rewards"]["_sum_"]
					print("BACK DELEGATOR")

		o_rewards = epoch_data[d_index]["rewards"]
		o_rewards_sum = int(o_rewards_sum) + int(o_rewards)
		o_rewards_STRG = "{ '_epoch_': "+str(o_rewards)+", '_sum_': "+str(o_rewards_sum)+"}"
		H_rewards_STRG = H_STRG["rewards"]
		o_STRG = str(H_STRG).replace(str(H_rewards_STRG), o_rewards_STRG)
		o_stake_sum = H_STRG["stake"]["_sum_"]
		o_epochCount = H_STRG["epoch_count"]
		o_ROA = setROA(o_epochCount, o_stake_sum, o_rewards_sum, 0)
		H_ROA_max = H_STRG["ROA"]["_max_"]
		if (d_ROA[0] > H_ROA_max):
			o_ROA_max = o_ROA[0]
		else:
			o_ROA_max = H_ROA_max

		o_ROA_STRG = "{ '_lifetime_': "+str(o_ROA[0])+", '_max_': "+str(o_ROA_max)+", '_bonus_included_': "+str(o_ROA[1])+"}"
		H_ROA_STRG = H_STRG["ROA"]
		o_STRG = str(o_STRG).replace(str(H_ROA_STRG), o_ROA_STRG)
#		print(o_STRG)
		O_strg = O_strg + o_STRG+",\n"
		O_rewards = O_rewards + o_rewards
		O_rewards_sum = O_rewards_sum + o_rewards_sum

		j += 1

	P_rewards = D_rewards + O_rewards
	P_rewards_sum = D_rewards_sum + O_rewards_sum
	delegators_rewards_STRG = "{ '_epoch_': "+str(D_rewards)+", '_sum_': "+str(D_rewards_sum)+"}"
	owners_rewards_STRG = "{ '_epoch_': "+str(O_rewards)+", '_sum_': "+str(O_rewards_sum)+"}"
	pool_rewards_STRG = "{ '_epoch_': "+str(P_rewards)+", '_sum_': "+str(P_rewards_sum)+"}"
	D_strg = "["+D_strg[0:-2]+"]"
	O_strg = "["+O_strg[0:-2]+"]"
	H_data_STRG = str(H_data).replace(str(dH_data),D_strg)
	H_data_STRG = H_data_STRG.replace(str(oH_data),O_strg)
	H_data_STRG = H_data_STRG.replace(str(H_data["delegators"]["rewards"]), delegators_rewards_STRG)
	H_data_STRG = H_data_STRG.replace(str(H_data["owners"]["rewards"]), owners_rewards_STRG)
	H_data_STRG = H_data_STRG.replace(str(H_data["pool"]["rewards"]), pool_rewards_STRG)
	history_data_STRG = str(history_data).replace(str(H_data), H_data_STRG)
	history_data_STRG = history_data_STRG.replace(cc, xx)

	with open(file, "w") as w_file:
		w_file.write(history_data_STRG)
		w_file.close()
#	print(H_data_STRG)


#processRewards(327)
