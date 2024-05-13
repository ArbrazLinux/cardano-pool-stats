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
from functions import checkBonus, setROA, checkGoneAndLost, checkBiggest
from functions_2 import getHistFile
from config import POOL_ID, POOL_TICKER, REGISTRATION_EPOCH, OWNERS_STAKE_ADDRESS
from colors import colors


################################################################################
def processBonus(Epoch, bonus_list):
	print(colors.fg.orange, "\n======================= DELEGATORS DATA SETTING =====================================", colors.reset)

	poolEpochCount = Epoch - REGISTRATION_EPOCH - 1

	################## definition des variables
	with open("data/pool_data.json") as json_file:
		pooldata = json.load(json_file)
		json_file.close()
	deleg_list = pooldata["delegators"]["delegator"]
	deleg_N = len(deleg_list)
	i = 0

	deleg_address = []; deleg_stake = []; deleg_stake_previous = []; deleg_stake_diff = []; deleg_stake_sum = [];
	deleg_stake_max = []; deleg_stake_min = []; deleg_stake_inputs = []; deleg_stake_outputs = [];
	deleg_rewards = []; deleg_rewards_sum = []; deleg_bonus = []; deleg_bonus_previous = []; deleg_bonus_sum = [];
	deleg_ROA = []; deleg_ROA_max = []; deleg_ROA_bonus = [];
	deleg_status = []; deleg_firstEpoch = []; deleg_sinceEpoch = []; deleg_lastEpoch = []; deleg_epochCount = [];
	deleg_comeBack = []; deleg_comeBack_count = []
	deleg_STRG = []
	previousEpoch_bonusAmount = []; previousEpoch_bonusAssets = []

	delegators_stake = 0; delegators_rewards = 0; delegators_bonus_sum = 0
	################## initialisation des tableaux
	while (i < deleg_N):

		deleg_address.insert(i,''); deleg_stake.insert(i, 0);
		deleg_stake_previous.insert(i, 0); deleg_stake_diff.insert(i, 0); deleg_stake_sum.insert(i, 0);
		deleg_stake_max.insert(i, 0); deleg_stake_min.insert(i, 0); deleg_stake_inputs.insert(i, 0); deleg_stake_outputs.insert(i, 0);
		deleg_rewards.insert(i, 0); deleg_rewards_sum.insert(i, 0); deleg_bonus.insert(i, 0); deleg_bonus_previous.insert(i, 0); deleg_bonus_sum.insert(i, 0);
		deleg_ROA.insert(i, 0); deleg_ROA_max.insert(i, 0); deleg_ROA_bonus.insert(i, 0);
		deleg_status.insert(i,''); deleg_firstEpoch.insert(i, 0); deleg_sinceEpoch.insert(i, 0); deleg_epochCount.insert(i, 0); deleg_comeBack.insert(i, ''); deleg_comeBack_count.insert(i, 0)
		deleg_STRG.insert(i, '')
		previousEpoch_bonusAmount.insert(i, 0); previousEpoch_bonusAssets.insert(i, '')

		i += 1

	l=0; i=0
	while (i < deleg_N):

		deleg_data = deleg_list[i]
		deleg_address[i] = deleg_data["stake_address"]
		deleg_stake[i] = deleg_data["stake"]
		deleg_stake_sum[i] = deleg_data["stake"]["_sum_"]
		deleg_rewards_sum[i] = deleg_data["rewards"]["_sum_"]
		previousEpoch_bonusAmount[i] = deleg_data["bonuses"]["amount"]
		previousEpoch_bonusAssets[i] = deleg_data["bonuses"]["assets"]
		deleg_bonus_previous[i] = deleg_data["bonuses"]["_previous_"]
		deleg_bonus_sum[i] = deleg_data["bonuses"]["_sum_"]
		deleg_ROA_max[i] = deleg_data["ROA"]["_max_"]
		deleg_epochCount[i] = int(deleg_data["epoch_count"])
		deleg_firstEpoch[i] = deleg_data["first_epoch"]
		deleg_sinceEpoch[i] = deleg_data["since_epoch"]
		deleg_comeBack[i] = deleg_data["comeback"]
		deleg_comeBack_count[i] = deleg_data["comeback_count"]

		#------------

		if deleg_address[i] in bonus_list[1]:
			bb = bonus_list[1].index(deleg_address[i])
			print("====> awarded delegator ----> BONUS")

			j = json.loads(bonus_list[2][bb])
			amountB = j["bonus_amount"]
			assetsB = j["assets"]

		else:
			amountB = 0
			assetsB = "[]"

		if (previousEpoch_bonusAmount[i] > 0):
			cc="'"
			xx='"'
			previousEpoch_bonusSTRG = '{ "epoch":'+str(Oepoch)+', "bonus_amount":'+str(previousEpoch_bonusAmount[i])+', "assets":'+str(previousEpoch_bonusAssets[i]).replace(cc, xx)+'}'

			previousEpoch_bonusSTRG = json.loads(previousEpoch_bonusSTRG)
		else:
			previousEpoch_bonusSTRG = ''
		if (len(deleg_bonus_previous[i]) > 0):
			bonus_previousSTRG = str(deleg_bonus_previous[i])
			lBP = len(bonus_previousSTRG) - 1
			bonus_previousSTRG = bonus_previousSTRG[1:lBP]
			if (previousEpoch_bonusSTRG):
				deleg_bonus_previous[i] = '['+str(previousEpoch_bonusSTRG)+','+bonus_previousSTRG+']'
			else:
				deleg_bonus_previous[i] = '['+bonus_previousSTRG+']'
			xx = '"'

		else:
			deleg_bonus_previous[i] = '['+str(previousEpoch_bonusSTRG)+']'
#			print("pas de précédents bonus")
		cc = "'"
		xx = '"'
		deleg_bonus_previous[i]=str(deleg_bonus_previous[i]).replace(cc, xx)
		deleg_bonus_sum[i]=amountB+deleg_bonus_sum[i]
		deleg_bonusSTRG = '{"amount":'+str(amountB)+', "assets":'+str(assetsB).replace(cc, xx)+', "_previous_":'+deleg_bonus_previous[i]+', "_sum_":'+str(deleg_bonus_sum[i])+'}'
		deleg_rewards[i] = deleg_data["rewards"]

		ROA = setROA(deleg_epochCount[i], deleg_stake_sum[i], deleg_rewards_sum[i], deleg_bonus_sum[i])

		deleg_ROA[i] = ROA[0]
		deleg_ROA_bonus[i] = ROA[1]
		if (deleg_ROA[i] > deleg_ROA_max[i]):
			deleg_ROA_max[i] = deleg_ROA[i]
		deleg_loyalty=0

		deleg_STRG[i] = '{ "stake_address": '+xx+deleg_address[i]+xx+', "first_epoch": '+str(deleg_firstEpoch[i])+', "since_epoch": '+str(deleg_sinceEpoch[i])+', "epoch_count": '+str(deleg_epochCount[i])+', "loyalty": '+str(deleg_loyalty)+', "comeback": '+xx+str(deleg_comeBack[i])+xx+', "comeback_count": '+str(deleg_comeBack_count[i])+', "stake": '+str(deleg_stake[i]).replace(cc, xx)+', "rewards": '+str(deleg_rewards[i]).replace(cc,xx)+', "ROA": { "_lifetime_": '+str(deleg_ROA[i])+', "_max_": '+str(deleg_ROA_max[i])+', "_bonuses_included_": '+str(deleg_ROA_bonus[i])+'}, "bonuses": '+deleg_bonusSTRG+'}'
		print(deleg_STRG[i])

		delegators_bonus_sum = delegators_bonus_sum + deleg_bonus_sum[i]

		print("======================================================================================")
		i+=1

	delegators_data = pooldata["delegators"]

	backDelegs_sum = delegators_data["back_delegs_sum"]
	backDelegs_N = delegators_data["back_delegs"]

	delegators_stake = delegators_data["stake"]
	delegators_stake_sum = delegators_data["stake"]["_sum_"]
	delegators_N = deleg_N
	delegators_N_previous = delegators_data["previous_delegsNb"]
	delegators_N_max = delegators_data["lifetime_max_delegsNb"]
	delegators_N_min = delegators_data["lifetime_min_delegsNb"]
	delegators_rewards_sum = delegators_data["rewards"]["_sum_"]
	delegators_rewards = delegators_data["rewards"]

	dROA = setROA(poolEpochCount, delegators_stake_sum, delegators_rewards_sum, delegators_bonus_sum)
	delegators_ROA = dROA[0]
	delegators_ROA_bonus = dROA[1]
	delegators_ROA_max = delegators_data["ROA"]["_max_"]

	if (delegators_ROA > delegators_ROA_max):
		delegators_ROA_max = delegators_ROA

	o = 0
	delegsStrg = ""
	while (o < deleg_N):
		if (o < deleg_N - 1):
			delegsStrg = delegsStrg+deleg_STRG[o]+',\n'
		else:
			delegsStrg = delegsStrg+deleg_STRG[o]
		o += 1
	delegs_biggest_ever = delegators_data["stake"]["_biggest_ever_"]
	delegs_biggest = checkBiggest(delegsStrg)
	if (delegs_biggest > delegs_biggest_ever):
		delegs_biggest_ever = delegs_biggest

	delegators_ROASTRG = '{ "_lifetime_": '+str(delegators_ROA)+', "_max_": '+str(delegators_ROA_max)+', "_bonuses_included_": '+str(delegators_ROA_bonus)+'}'
	delegators_STRG = '"delegators": { "delegsNb": '+str(delegators_N)+', "previous_delegsNb": '+str(delegators_N_previous)+', "lifetime_max_delegsNb": '+str(delegators_N_max)+', "lifetime_min_delegsNb": '+str(delegators_N_min)+', "back_delegs": '+str(backDelegs_N)+', "back_delegs_sum": '+str(backDelegs_sum)+', "stake": '+str(delegators_stake)+', "rewards": '+str(delegators_rewards)+', "ROA": '+delegators_ROASTRG+', "delegator": [\n'+delegsStrg+']}'
	print("===================================================================",colors.fg.green,"DELEGATORS DONE",colors.reset)
#	print(delegators_STRG)
	D_replacedSTRG = "'delegators': "+str(delegators_data)
	pooldata_STRG = str(pooldata).replace(D_replacedSTRG, delegators_STRG.replace(xx,cc))
	bonusSTRG = setBonus(Epoch, bonus_list)
	B_replacedSTRG = str(pooldata["bonuses"])
#	print(bonusSTRG)
	pooldata_STRG = str(pooldata_STRG).replace(B_replacedSTRG, bonusSTRG.replace(xx,cc))

	with open("data/pool_data.json", "w") as file:
		file.write(pooldata_STRG.replace(cc,xx))
		file.close()

#########################################################################################
def setBonus(Nepoch, bonus_list):
	xx = '"'
	cc = "'"
	Oepoch = Nepoch - 1
	with open("data/pool_data.json") as json_file:
		bdata = json.load(json_file)
		json_file.close()
	bonus_data = bdata["bonuses"]
	bonus_amount = bonus_list[0]
	bonus_sum = bonus_data["_sum_"]
	bonus_sum = bonus_sum + bonus_amount
	bonus_assets = bonus_data["assets"]
	bonus_history = bonus_data["history"]
	previous_bonus_amount = bonus_data["amount"]
	if (previous_bonus_amount > 0):
		if (len(bonus_history) > 0):
			bonus_historySTRG = '[{ "epoch": '+str(Oepoch)+', "amount": '+str(previous_bonus_amount)+', "assets": '+str(bonus_assets)+'},'+str(bonus_history)[1:-1]+']'
		else:
			bonus_historySTRG = '[{ "epoch": '+str(Oepoch)+', "amount": '+str(previous_bonus_amount)+', "assets": '+str(bonus_assets)+'}]'
	else:
		bonus_historySTRG = str(bonus_history)
#	print(bonus_historySTRG)
	bonusStrg = bonus_list[2]
	bonusN = len(bonus_list[2])
	indexA = 0; bA_name = []; bA = []; bA_amount = []; bA_fingerprint = []; awardedSTRG = ''
	i = 0

	while (i < bonusN):
		bS = '['+bonus_list[2][i]+']'
		bS = json.loads(bS)
		bSA = bS[0]["assets"]
#		print(bSA)
		bSA_N = len(bSA)
		j = 0
		while (j < bSA_N):
			bSA_name = bSA[j]["name"]
			bSA_amount = bSA[j]["amount"]
			bSA_fingerprint = bSA[j]["fingerprint"]
			if bSA_name in bA_name:
				indexN = bA_name.index(bSA_name)
				bA_amount[indexN] += bSA_amount
			else:
				bA_name.insert(indexA, bSA_name)
				bA_amount.insert(indexA, bSA_amount)
				bA_fingerprint.insert(indexA, bSA_fingerprint)
				indexA += 1
			j += 1
		if ( i == 0 ):
			awardedSTRG = str(bS[0])
		else:
			awardedSTRG = awardedSTRG+','+str(bS[0])
		i += 1
	bA = bA_name, bA_amount, bA_fingerprint
	N = len(bA_name)
	i = 0
	assetsSTRG = ''
	while (i < N):
		if ( i == 0 ):
			assetsSTRG = '{"name": '+xx+str(bA[0][i])+xx+', "amount": '+str(bA[1][i])+', "fingerprint": '+xx+str(bA[2][i])+xx+'}'
		else:
			assetsSTRG = assetsSTRG+',{"name": '+xx+str(bA[0][i])+xx+', "amount": '+str(bA[1][i])+', "fingerprint": '+xx+str(bA[2][i])+xx+'}'
		i += 1

	bonusSTRG = '{ "amount": '+str(bonus_amount)+', "_sum_": '+str(bonus_sum)+', "awarded_delegators": ['+awardedSTRG.replace(cc, xx)+'], "assets": ['+assetsSTRG.replace(cc, xx)+'], "history": '+str(bonus_historySTRG).replace(cc, xx)+'}'
	return bonusSTRG

#bonus_list = checkBonus(481)
#processBonus(481, bonus_list)
