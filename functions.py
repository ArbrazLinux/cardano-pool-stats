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
from config import PROJECT_ID, POOL_ID
from os.path import exists as file_exists
import subprocess


def getRewards(address, epoch):
	urlQuery="https://cardano-mainnet.blockfrost.io/api/v0/accounts/{}/rewards".format(address)
	with open("tmp/tmpR.json", "wb") as out_file:
		curl = pycurl.Curl()
		curl.setopt(curl.HTTPHEADER, ['H', "project_id:{}".format(PROJECT_ID)])
		curl.setopt(curl.URL, "{}".format(urlQuery))
		curl.setopt(curl.WRITEDATA, out_file)
		curl.perform()
		curl.close()
	out_file.close()
	with open("tmp/tmpR.json") as json_file:
		rewardsList = json.load(json_file)
		rewardsN = len(rewardsList)
	i = rewardsN - 1
	epoch_rewards = 0
	while (i >= 0):
		Repoch = rewardsList[i]["epoch"]
		if (Repoch < epoch):
			return epoch_rewards
			break
		if (Repoch == epoch):
			epoch_rewards = rewardsList[i]["amount"]
			return epoch_rewards
			break
		i-=1
	return epoch_rewards

#add="stake1u9gf45qgsjzfcl9f4ywx5hejcmxx3efsz6q2re006xkxzzc7tzsm7"
#reward=getRewards(add,478)
#print(reward)

def checkBonus(epoch):
	Bepoch = epoch
	bonusN = 0
	epochBonus = 0
	xx='"'
	if (file_exists("data/awards.json")):
		with open("data/awards.json") as json_file:
			bonus_json = json.load(json_file)
			json_file.close()
		with open("data/epoch/Epoch_{}.json".format(Bepoch)) as json_file:
			deleg_list = json.load(json_file)
			json_file.close()
		awardsCount = len(bonus_json)
		i=awardsCount - 1
		asa = []; b_STRG = []
		while (i >= 0):
			awardsEpoch = bonus_json[i]["epoch"]
			if (awardsEpoch == Bepoch):
				bonusN = len(bonus_json[i]["awards"])
				bonus_data = bonus_json[i]["awards"]
				ii=0;  awa = []; dl = []; posD = [];
				dN = len(deleg_list)
				d = 0
				while (d < dN):
					dl.insert(d, deleg_list[d]["address"])
					d += 1
				while (ii < bonusN):
					asa.insert(ii, ''); awa.insert(ii, 0); posD.insert(ii, 0); b_STRG.insert(i, '')
					ii += 1
				ii = 0
				while (ii < bonusN):
					asa[ii] = bonus_data[ii]["address"]
#					print(asa[ii])
					awa[ii] = bonus_data[ii]["amount"]
					if asa[ii] in dl:
						posD[ii] = dl.index(asa[ii])
						b_amount = bonus_data[ii]["amount"]
						if (bonus_data[ii]["assets"]):
							assetsN = len(bonus_data[ii]["assets"])
						else:
							assetsN = 0
						a_STRG = []
						if (assetsN > 0):
							assets = bonus_data[ii]["assets"]
							q = 0

							while (q < assetsN):
								a_name = assets[q]["name"]
								a_amount = assets[q]["amount"]
								a_policy = assets[q]["policyID"]
								a_nameHash = assets[q]["name_hash"]
								a_fingerprint = assets[q]["fingerprint"]
								a_STRG.insert(q, '{"name":'+xx+a_name+xx+', "amount":'+str(a_amount)+', "policyID":'+xx+a_policy+xx+', "name_hash":'+xx+a_nameHash+xx+', "fingerprint":'+xx+a_fingerprint+xx+'}')
								q += 1
#						print(a_STRG)
						b_STRG[ii] = '{"stake_address":'+xx+asa[ii]+xx+', "bonus_amount":'+str(awa[ii])+', "assets":' + str(a_STRG).replace("'","") +"}"
						epochBonus = epochBonus + awa[ii]
					ii += 1
				break
			i -= 1
	ooo = epochBonus, asa, b_STRG
	with open("tmp/tB.json", "w") as file:
		file.write(str(ooo))
		file.close()
	return epochBonus, asa, b_STRG

#dd=checkBonus(255)
#print(dd)

#z="stake1ux7znv7muj73q94kz0v7a27jcqrljall55chdg4ukvnuy0sl3jgw5"
#if (z in dd[1]):
#	i = dd[1].index(z)
#	print("address", dd[1][i], "index", dd[2][i])

def setROA(epochCount, stakeSum, rewardsSum, bonusSum):
	averageStake = float(stakeSum / epochCount)
	yearCount = float(epochCount / 73)

	if (rewardsSum > 0):
		lifetimeROA = round(float(rewardsSum / averageStake * 100 / yearCount),2)
		bonusROA = round(float((rewardsSum + bonusSum) / averageStake * 100 / yearCount),2)
	elif (bonusSum > 0):
		lifetimeROA = 0
		bonusROA = round(float(bonusSum / averageStake * 100 / yearCount),2)
	else:
		lifetimeROA = 0
		bonusROA = 0

	return lifetimeROA, bonusROA

def checkGoneAndLost(Nepoch):
	pool_lost_stake = 0;
	gone_delegs = 0;
	if (file_exists("data/gone_delegators.json")):
		with open("data/gone_delegators.json") as json_file:
			gones = json.load(json_file)
			json_file.close()

		Oepoch = Nepoch - 1
		gones_N = len(gones["gone_delegators"])
		i = gones_N - 1
		while (i > 0):
			lost_stake = 0;
			G_epoch = gones["gone_delegators"][i]["last_epoch"]
			if (G_epoch == Oepoch):
				lost_stake = gones["gone_delegators"][i]["lost_stake"]
				pool_lost_stake = pool_lost_stake + lost_stake
				gone_delegs += 1
			elif (G_epoch < Oepoch):
				break
			i -= 1
	return gone_delegs, pool_lost_stake

def checkBlocks(Nepoch):
	cc = "'"
	xx = '"'
	urlQuery="https://cardano-mainnet.blockfrost.io/api/v0/epochs/{}/blocks/{}".format(Nepoch, POOL_ID)
	with open("tmp/tmpB.json", "wb") as out_file:
		curl = pycurl.Curl()
		curl.setopt(curl.HTTPHEADER, ['H', "project_id:{}".format(PROJECT_ID)])
		curl.setopt(curl.URL, "{}".format(urlQuery))
		curl.setopt(curl.WRITEDATA, out_file)
		curl.perform()
		curl.close()
	out_file.close()
	with open("tmp/tmpB.json") as json_file:
		epoch_blocks = json.load(json_file)
		json_file.close()
	blocks_N = len(epoch_blocks)
	with open("data/pool_data.json") as json_file:
		pooldata = json.load(json_file)
		json_file.close()
	blocks_sum = pooldata["blocks"]["total_blocks"]
	blocks_max = pooldata["blocks"]["lifetime_max"]
	blocks_previous = pooldata["blocks"]["block"]
	blocks_history = pooldata["blocks"]["history"]
	epoch_blocksSTRG = ""
	if (blocks_N > 0):
		print("======================= !! BLOCKS !! ==========================")
		B_counter = blocks_sum
		i = 0; hash_list=[]
		if (file_exists("data/blocksList.json")):
			with open("data/blocksList.json") as json_file:
				blocks_list = json.load(json_file)
				json_file.close()
			while (i < len(blocks_list["block"])):
				hash_list.insert(i, blocks_list["block"][i]["hash"])
				i += 1
			blocksSTRG = str(blocks_list)[0:-2]
		else:
			blocksSTRG = "{'block': ["
			blocks_list = []
#		print(blocks_list)
		i = 0
		k = len(blocks_list) - 1; j = k; a = 0

		while (i < blocks_N):
			block_STRG = ''
			block_hash = epoch_blocks[i]
			if (block_hash not in hash_list):
				urlQuery="https://cardano-mainnet.blockfrost.io/api/v0/blocks/{}".format(block_hash)
				with open("tmp/tmpB_h.json", "wb") as out_file:
					curl = pycurl.Curl()
					curl.setopt(curl.HTTPHEADER, ['H', "project_id:{}".format(PROJECT_ID)])
					curl.setopt(curl.URL, "{}".format(urlQuery))
					curl.setopt(curl.WRITEDATA, out_file)
					curl.perform()
					curl.close()
				with open("tmp/tmpB_h.json") as json_file:
					block_data = json.load(json_file)
					json_file.close()
				block_conf = block_data["confirmations"]
				block_STRG = str(block_data).replace(", 'confirmations': {}".format(block_conf), "")
				block_STRG = str(block_STRG).replace(", 'slot_leader': '{}'".format(POOL_ID), "")
			else:
				block_STRG = str(blocks_list["block"][j])
#				print(block_STRG)
			if (a > 0):
				if (block_hash not in hash_list):
					blocksSTRG = blocksSTRG+','+block_STRG
				epoch_blocksSTRG = epoch_blocksSTRG+','+block_STRG
			else:
				if (B_counter > 0 and block_hash not in hash_list):
					blocksSTRG = blocksSTRG+','+block_STRG
				elif (block_hash not in hash_list):
					blocksSTRG = blocksSTRG+''+block_STRG
				epoch_blocksSTRG = epoch_blocksSTRG+''+block_STRG
				a += 1

			j -= 1
			B_counter += 1
			print("block N° : ", B_counter, "---->", block_hash)
			i += 1
		blocksSTRG = blocksSTRG+']}'

		blocksSTRG = blocksSTRG.replace(cc, xx)
		blocksSTRG = blocksSTRG.replace('None', '""')
#		print(epoch_blocksSTRG)
		with open("data/blocksList.json", "w") as out_file:
			out_file.write(blocksSTRG)
			out_file.close()


	blocks_historySTRG = str(blocks_history)
	blocks_Np = len(blocks_previous)
	if (blocks_Np >0):
		blocks_previousSTRG = str(blocks_previous)[1:-1]
		blocks_historySTRG = str(blocks_history)[0:-1]
		if (blocks_sum > 1):
			blocks_historySTRG = blocks_historySTRG+','+blocks_previousSTRG+']'
		else:
			blocks_historySTRG = blocks_historySTRG+''+blocks_previousSTRG+']'
#		print(blocks_historySTRG)
	if (blocks_N > blocks_max):
		blocks_max = blocks_N
	blocks_sum = blocks_sum + blocks_N
	blocks_S = "'blocks': { 'epoch': "+str(blocks_N)+", 'total_blocks': "+str(blocks_sum)+", 'lifetime_max': "+str(blocks_max)+", 'block': ["+str(epoch_blocksSTRG)+"], 'history': "+str(blocks_historySTRG)+"}"
#	print(blocks_S)
	blocks_S = blocks_S.replace('None', '"0"')
	return blocks_S

def checkBiggest(STRG):
	strg = str('['+STRG+']')
	big_json = json.loads(strg)
#	print(big_json)
	i = 0; bigN = 0; biggest = 0
	N = len(big_json)
	while (i < N):
		bigN = big_json[i]["stake"]["_epoch_"]
		if (bigN > biggest):
			biggest = bigN
		i += 1
	return biggest

def getLiveStake(Nepoch):
	a = 0
#getLiveStake(245)
