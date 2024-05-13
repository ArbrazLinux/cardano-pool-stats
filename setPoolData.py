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
from functions import getRewards, checkBonus, setROA, checkGoneAndLost, checkBlocks, checkBiggest
from config import POOL_ID, POOL_TICKER, REGISTRATION_EPOCH, OWNERS_STAKE_ADDRESS, PRUNE_NB
from colors import colors

######################### HEADER DATA SETTING ###################################################################################
def setHeader(NewEpoch):
	pool_epochCount = NewEpoch - REGISTRATION_EPOCH - 1; xx='"'
	first_active_epoch = REGISTRATION_EPOCH + 2
	header_STRG = '{ "current_epoch": '+str(NewEpoch)+', "ticker": '+xx+POOL_TICKER+xx+', "pool_id": '+xx+POOL_ID+xx+', "since_epoch": '+str(first_active_epoch)+', "epoch_count": '+str(pool_epochCount)+','
	return header_STRG

######################### OWNERS INDEX SETTING ##################################################################################
def setOwnersIndex(NewEpoch):
	with open("data/epoch/Epoch_{}.json".format(NewEpoch)) as json_file:
		holders_list = json.load(json_file)
		json_file.close()
	holders_N = len(holders_list)
	owner_index=[];	index=0
	for owner in OWNERS_STAKE_ADDRESS:
		i=0
		while (i < holders_N):
			holder_address = holders_list[i]["address"]
			if (owner == holder_address):
				owner_index.insert(index, i)
				index+=1
				break
			i+=1
	return owner_index

######################### DELEGATORS INDEX SETTING ###############################################################################
def setDelegsIndex(NewEpoch):
	with open("data/epoch/Epoch_{}.json".format(NewEpoch)) as json_file:
		holders_list = json.load(json_file)
		json_file.close()
	holders_N = len(holders_list)
	holder_index=[]
	index=0; i=0
	while (i < holders_N):
		holder_address = holders_list[i]["address"]
		if (holder_address not in OWNERS_STAKE_ADDRESS):
			holder_index.insert(index, i)
			index+=1
			i+=1
			continue
		i+=1
	return holder_index
#	print(holder_index)

######################### DELEGATORS DATA SETTING ################################################################################
def setDelegsData(NewEpoch, deleg_index, bonus_list, countEpoch):
	print(colors.fg.orange, "\n======================= DELEGATORS DATA SETTING =====================================", colors.reset)
	CountingEpoch = countEpoch
	poolEpochCount = NewEpoch - REGISTRATION_EPOCH - 1
	Oepoch = NewEpoch - 1
	################## definition des variables
	deleg_N = len(deleg_index); maxN = deleg_N
	i = 0
	nI=[];
	deleg_address = []; deleg_stake = []; deleg_stake_previous = []; deleg_stake_diff = []; deleg_stake_sum = [];
	deleg_stake_max = []; deleg_stake_min = []; deleg_stake_inputs = []; deleg_stake_outputs = [];
	deleg_rewards = []; deleg_rewards_sum = []; deleg_bonus = []; deleg_bonus_previous = []; deleg_bonus_sum = [];
	deleg_ROA = []; deleg_ROA_max = []; deleg_ROA_bonus = [];
	deleg_status = []; deleg_firstEpoch = []; deleg_sinceEpoch = []; deleg_lastEpoch = []; deleg_epochCount = [];
	deleg_comeBack = []; deleg_comeBack_count = []
	deleg_STRG = []
	previousEpoch_bonusAmount = []; previousEpoch_bonusAssets = []
	backDeleg_address = []; backDeleg_goneEpoch = []; backDeleg_index = []; backDelegs_N = 0; backStake = 0
	delegators_stake = 0; delegators_rewards = 0; delegators_bonus_sum = 0
	################## initialisation des tableaux
	while (i < deleg_N):
		nI.insert(i, 0)
		deleg_address.insert(i,''); deleg_stake.insert(i, 0);
		deleg_stake_previous.insert(i, 0); deleg_stake_diff.insert(i, 0); deleg_stake_sum.insert(i, 0);
		deleg_stake_max.insert(i, 0); deleg_stake_min.insert(i, 0); deleg_stake_inputs.insert(i, 0); deleg_stake_outputs.insert(i, 0);
		deleg_rewards.insert(i, 0); deleg_rewards_sum.insert(i, 0); deleg_bonus.insert(i, 0); deleg_bonus_previous.insert(i, 0); deleg_bonus_sum.insert(i, 0);
		deleg_ROA.insert(i, 0); deleg_ROA_max.insert(i, 0); deleg_ROA_bonus.insert(i, 0);
		deleg_status.insert(i,''); deleg_firstEpoch.insert(i, 0); deleg_sinceEpoch.insert(i, 0); deleg_epochCount.insert(i, 0); deleg_comeBack.insert(i, ''); deleg_comeBack_count.insert(i, 0)
		deleg_STRG.insert(i, '')
		previousEpoch_bonusAmount.insert(i, 0); previousEpoch_bonusAssets.insert(i, '')
		backDeleg_address.insert(i,''); backDeleg_goneEpoch.insert(i, 0); deleg_lastEpoch.insert(i, 0); backDeleg_index.insert(i, 0)
		i += 1


	l=0; i=0
	while (i < deleg_N):
		l = int(deleg_index[i])
		r = 0
		with open("data/epoch/Epoch_{}.json".format(NewEpoch)) as json_file:
			deleg_json = json.load(json_file)
			json_file.close()
		deleg_address[i] = deleg_json[l]["address"]

		with open("data/pool_data.json") as json_file:
			pooldata = json.load(json_file)
			json_file.close()
		deleg_list = pooldata["delegators"]["delegator"]
		deleg_pN = len(deleg_list)
		pD=[]
		while (r < deleg_pN):
			pD.insert(r, '')
			r += 1
		r=0
		deleg_status[i] = deleg_json[l]["status"]

		while (r < deleg_pN):
			pD[r] = deleg_list[r]["stake_address"]

			if (pD[r] == deleg_address[i]):
				print(colors.fg.green, "INDEX RETRIEVED", colors.reset, "---> STAKEHOLDER :", deleg_address[i], colors.fg.green, deleg_status[i], colors.reset)
				nI[i] = r
				maxN-=1
				break
			r+=1
			if (r == deleg_pN):

				s = deleg_N + maxN
				nI[i] = s
				print(colors.fg.blue, "NEW INDEX", colors.reset, "---> STAKEHOLDER :", deleg_address[i], colors.fg.blue, deleg_status[i], colors.reset)
				maxN-=1
				break
		deleg_stake[i] = deleg_json[l]["current_stake"]

		#-----------
		if (deleg_status[i] == "BACK"):
			w=0
			deleg_lastEpoch[i] = deleg_json[l]["gone_epoch"]
			with open("data/gone_delegators.json") as json_file:
				gones_json = json.load(json_file)
				gones = gones_json["gone_delegators"]
				json_file.close()
			w = int(len(gones))
			w -= 1
			while (w >= 0):
				backDeleg_address[i] = gones[w]["gone"]
				if (backDeleg_address[i] == deleg_address[i]):
					backDeleg_goneEpoch[i] = gones[w]["last_epoch"]
					if (backDeleg_goneEpoch[i] < NewEpoch):
						backDeleg_index[i] = int(gones[w]["last_index"])
						backDelegs_N += 1
						print("===	COMING BACK	===")
						break
				w -= 1
			pruneDist = float((NewEpoch - REGISTRATION_EPOCH - 2)/PRUNE_NB)
			pruneD = (REGISTRATION_EPOCH + 2) + int(pruneDist)*PRUNE_NB
			pruneF = pruneD + (PRUNE_NB - 1)
			if (backDeleg_goneEpoch[i] < pruneF):

				distD = float((int(backDeleg_goneEpoch[i]) - 245)/PRUNE_NB)
				dH = 245 + int(distD)*PRUNE_NB
				fH = dH + (PRUNE_NB - 1)

				historyIndex = fH - int(backDeleg_goneEpoch[i])

				with open("data/history/pooldata_{}_{}.json".format(dH, fH)) as json_file:
					pooldata = json.load(json_file)
					json_file.close()
				history_data = pooldata[int(historyIndex)]["delegators"]["delegator"][int(backDeleg_index[i])]

			else:
				history_data = pooldata["history"][int(historyIndex)]["delegators"]["delegator"][int(backDeleg_index[i])]
			deleg_stake_previous[i] = history_data["stake"]["_epoch_"]
			deleg_stake_sum[i] = history_data["stake"]["_sum_"]
			deleg_stake_max[i] = history_data["stake"]["_lifetime_max_"]
			deleg_stake_min[i] = history_data["stake"]["_lifetime_min_"]
			deleg_stake_inputs[i] = history_data["stake"]["_inputs_sum_"]
			deleg_stake_outputs[i] = history_data["stake"]["_outputs_sum_"]
			deleg_rewards_sum[i] = history_data["rewards"]["_sum_"]
			previousEpoch_bonusAmount[i] = 0
			previousEpoch_bonusAssets[i] = "[]"
			deleg_bonus_previous[i] = '[]' #history_data["bonuses"]["_previous_"]
			deleg_bonus_sum[i] = history_data["bonuses"]["_sum_"]
			deleg_epochCount[i] = int(history_data["epoch_count"])
			deleg_firstEpoch[i] = history_data["first_epoch"]
			deleg_sinceEpoch[i] = NewEpoch
			deleg_ROA_max[i] = history_data["ROA"]["_max_"]
			deleg_comeBack[i] = True;
			deleg_comeBack_count[i] = int(history_data["comeback_count"]) + 1
			backStake = backStake + deleg_stake[i]

		elif (deleg_status[i] == "NEW"):
			deleg_stake_previous[i] = 0
			deleg_stake_sum[i] = 0
			deleg_stake_max[i] = 0
			deleg_stake_min[i] = 0
			deleg_stake_inputs[i] = 0
			deleg_stake_outputs[i] = 0
			deleg_rewards_sum[i] = 0
			previousEpoch_bonusAmount[i] = 0
			previousEpoch_bonusAssets[i] = "[]"
			deleg_bonus_previous[i] = "[]"
			deleg_bonus_sum[i] = 0
			deleg_ROA_max[i] = 0
			deleg_firstEpoch[i] = NewEpoch
			deleg_sinceEpoch[i] = NewEpoch
			deleg_epochCount[i] = 0;
			deleg_comeBack[i] = False;
			deleg_comeBack_count[i] = 0;

		else:
			deleg_data = deleg_list[nI[i]]
			deleg_stake_previous[i] = deleg_data["stake"]["_epoch_"]
			deleg_stake_sum[i] = deleg_data["stake"]["_sum_"]
			deleg_stake_max[i] = deleg_data["stake"]["_lifetime_max_"]
			deleg_stake_min[i] = deleg_data["stake"]["_lifetime_min_"]
			deleg_stake_inputs[i] = deleg_data["stake"]["_inputs_sum_"]
			deleg_stake_outputs[i] = deleg_data["stake"]["_outputs_sum_"]
			if not deleg_stake_outputs[i]:
				deleg_stake_outputs[i] = 0
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

		if (deleg_stake_min[i] == 0):
			deleg_stake_min[i] = deleg_stake[i]

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

		if (CountingEpoch):
			deleg_epochCount[i] = deleg_epochCount[i] + 1

		deleg_stake_diff[i] = deleg_stake[i] - deleg_stake_previous[i]
		deleg_stake_sum[i] = deleg_stake_sum[i] + deleg_stake[i]
		if (deleg_stake[i] > deleg_stake_max[i]):
			deleg_stake_max[i] = deleg_stake[i]
		elif (deleg_stake[i] < deleg_stake_min[i]):
			deleg_stake_min[i] = deleg_stake[i]

		if (deleg_stake_diff[i] > 0):
			deleg_stake_inputs[i] = int(deleg_stake_inputs[i]) + deleg_stake_diff[i];
		elif (deleg_stake_diff[i] < 0):
			deleg_stake_outputs[i] = int(deleg_stake_outputs[i]) + deleg_stake_diff[i];

		deleg_rewards[i] = deleg_json[l]["rewards"]
		deleg_rewards_sum[i] = int(deleg_rewards_sum[i]) + int(deleg_rewards[i])
		ROA = setROA(deleg_epochCount[i], deleg_stake_sum[i], deleg_rewards_sum[i], deleg_bonus_sum[i])

		deleg_ROA[i] = ROA[0]
		deleg_ROA_bonus[i] = ROA[1]
		if (deleg_ROA[i] > deleg_ROA_max[i]):
			deleg_ROA_max[i] = deleg_ROA[i]
		deleg_loyalty=0

		deleg_STRG[i] = '{ "stake_address": '+xx+deleg_address[i]+xx+', "first_epoch": '+str(deleg_firstEpoch[i])+', "since_epoch": '+str(deleg_sinceEpoch[i])+', "epoch_count": '+str(deleg_epochCount[i])+', "loyalty": '+str(deleg_loyalty)+', "comeback": '+xx+str(deleg_comeBack[i])+xx+', "comeback_count": '+str(deleg_comeBack_count[i])+', "stake": { "_epoch_": '+str(deleg_stake[i])+', "_previous_": '+str(deleg_stake_previous[i])+', "_diff_": '+str(deleg_stake_diff[i])+', "_sum_": '+str(deleg_stake_sum[i])+', "_lifetime_max_": '+str(deleg_stake_max[i])+', "_lifetime_min_": '+str(deleg_stake_min[i])+', "_inputs_sum_": '+str(deleg_stake_inputs[i])+', "_outputs_sum_": '+str(deleg_stake_outputs[i])+'}, "rewards": { "_epoch_": '+str(deleg_rewards[i])+', "_sum_": '+str(deleg_rewards_sum[i])+'}, "ROA": { "_lifetime_": '+str(deleg_ROA[i])+', "_max_": '+str(deleg_ROA_max[i])+', "_bonuses_included_": '+str(deleg_ROA_bonus[i])+'}, "bonuses": '+deleg_bonusSTRG+'}'
		print(deleg_STRG[i])
		delegators_stake = delegators_stake + deleg_stake[i]
		delegators_bonus_sum = delegators_bonus_sum + deleg_bonus_sum[i]
		delegators_rewards = delegators_rewards + deleg_rewards[i]

		print("======================================================================================")
		i+=1
	with open("data/pool_data.json") as json_file:
		pooldata = json.load(json_file)
		json_file.close()
	delegators_data = pooldata["delegators"]

	backDelegs_sum = delegators_data["back_delegs_sum"]
	backDelegs_sum = backDelegs_sum + backDelegs_N

	delegators_stake_previous = delegators_data["stake"]["_epoch_"]
	delegators_stake_sum = delegators_data["stake"]["_sum_"]
	delegators_stake_max = delegators_data["stake"]["_lifetime_max_"]
	delegators_stake_min = delegators_data["stake"]["_lifetime_min_"]
	delegators_stake_inputs = delegators_data["stake"]["_inputs_sum_"]
	delegators_stake_outputs = delegators_data["stake"]["_outputs_sum_"]
	delegators_N = deleg_N
	delegators_N_previous = delegators_data["delegsNb"]
	delegators_N_max = delegators_data["lifetime_max_delegsNb"]
	delegators_N_min = delegators_data["lifetime_min_delegsNb"]
	delegators_rewards_sum = delegators_data["rewards"]["_sum_"]

	delegators_stake_sum = delegators_stake_sum + delegators_stake
	delegators_stake_diff = delegators_stake - delegators_stake_previous
	delegators_rewards_sum = delegators_rewards_sum + delegators_rewards

	if (delegators_stake_diff > 0):
		delegators_stake_inputs = delegators_stake_inputs + delegators_stake_diff
	elif (delegators_stake_diff < 0):
		delegators_stake_outputs = delegators_stake_outputs + delegators_stake_diff

	if (delegators_stake > delegators_stake_max):
		delegators_stake_max = delegators_stake
	elif (delegators_stake < delegators_stake_min or delegators_stake_min == 0):
		delegators_stake_min = delegators_stake

	if (delegators_N > delegators_N_max):
		delegators_N_max = delegators_N
	elif (delegators_N < delegators_N_min or delegators_N_min == 0):
		delegators_N_min = delegators_N

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

	delegators_stakeSTRG = '{ "_epoch_": '+str(delegators_stake)+', "_previous_": '+str(delegators_stake_previous)+', "_diff_": '+str(delegators_stake_diff)+', "_sum_": '+str(delegators_stake_sum)+', "_lifetime_max_": '+str(delegators_stake_max)+', "_lifetime_min_": '+str(delegators_stake_min)+', "_inputs_sum_": '+str(delegators_stake_inputs)+', "_outputs_sum_": '+str(delegators_stake_outputs)+', "_biggest_ever_": '+str(delegs_biggest_ever)+'}'
	delegators_rewardsSTRG = '{ "_epoch_": '+str(delegators_rewards)+', "_sum_": '+str(delegators_rewards_sum)+'}'
	delegators_ROASTRG = '{ "_lifetime_": '+str(delegators_ROA)+', "_max_": '+str(delegators_ROA_max)+', "_bonuses_included_": '+str(delegators_ROA_bonus)+'}'
	delegators_STRG = '"delegators": { "delegsNb": '+str(delegators_N)+', "previous_delegsNb": '+str(delegators_N_previous)+', "lifetime_max_delegsNb": '+str(delegators_N_max)+', "lifetime_min_delegsNb": '+str(delegators_N_min)+', "back_delegs": '+str(backDelegs_N)+', "back_delegs_sum": '+str(backDelegs_sum)+', "stake": '+delegators_stakeSTRG+', "rewards": '+delegators_rewardsSTRG+', "ROA": '+delegators_ROASTRG+', "delegator": [\n'+delegsStrg+']}'
	print("===================================================================",colors.fg.green,"DELEGATORS DONE",colors.reset)
	return delegators_STRG

######################### OWNERS DATA SETTING ###################################################################################
def setOwnersData(NewEpoch, owner_index, countEpoch):
	print(colors.fg.orange,"\n======================== OWNERS DATA SETTING ========================================",colors.reset)
	CountingEpoch = countEpoch
	poolEpochCount = NewEpoch - REGISTRATION_EPOCH - 1
	Oepoch = NewEpoch - 1
	################## definition des variables
	owner_N = len(owner_index); maxN = owner_N; xx = '"'
	i = 0
	nI=[];
	deleg_address = []; deleg_stake = []; deleg_stake_previous = []; deleg_stake_diff = []; deleg_stake_sum = [];
	deleg_stake_max = []; deleg_stake_min = []; deleg_stake_inputs = []; deleg_stake_outputs = [];
	deleg_rewards = []; deleg_rewards_sum = [];
	deleg_ROA = []; deleg_ROA_max = [];
	deleg_status = []; deleg_firstEpoch = []; deleg_sinceEpoch = []; deleg_lastEpoch = []; deleg_epochCount = [];
	deleg_comeBack = []; deleg_comeBack_count = []
	deleg_STRG = []
	backDeleg_address = []; backDeleg_goneEpoch = []; backDeleg_index = []; backDelegs_N = 0; backStake = 0
	delegators_stake = 0; delegators_rewards = 0; delegators_bonus_sum = 0
	################## initialisation des tableaux
	while (i < owner_N):
		nI.insert(i, 0)
		deleg_address.insert(i,''); deleg_stake.insert(i, 0);
		deleg_stake_previous.insert(i, 0); deleg_stake_diff.insert(i, 0); deleg_stake_sum.insert(i, 0);
		deleg_stake_max.insert(i, 0); deleg_stake_min.insert(i, 0); deleg_stake_inputs.insert(i, 0); deleg_stake_outputs.insert(i, 0);
		deleg_rewards.insert(i, 0); deleg_rewards_sum.insert(i, 0);
		deleg_ROA.insert(i, 0); deleg_ROA_max.insert(i, 0);
		deleg_status.insert(i,''); deleg_firstEpoch.insert(i, 0); deleg_sinceEpoch.insert(i, 0); deleg_epochCount.insert(i, 0); deleg_comeBack.insert(i, ''); deleg_comeBack_count.insert(i, 0)
		deleg_STRG.insert(i, '')

		backDeleg_address.insert(i,''); backDeleg_goneEpoch.insert(i, 0); deleg_lastEpoch.insert(i, 0); backDeleg_index.insert(i, 0)
		i += 1


	l=0; i=0
	while (i < owner_N):
		l = int(owner_index[i])
		r = 0
		with open("data/epoch/Epoch_{}.json".format(NewEpoch)) as json_file:
			owner_json = json.load(json_file)
			json_file.close()
		deleg_address[i] = owner_json[l]["address"]

		with open("data/pool_data.json") as json_file:
			pooldata = json.load(json_file)
			json_file.close()
		owner_list = pooldata["owners"]["owner"]
		owner_pN = len(owner_list)
		pD=[]
		while (r < owner_pN):
			pD.insert(r, '')
			r += 1
		r=0
		deleg_status[i] = owner_json[l]["status"]

		while (r < owner_pN):
			pD[r] = owner_list[r]["stake_address"]

			if (pD[r] == deleg_address[i]):
				print(colors.fg.green, "INDEX RETRIEVED", colors.reset, "---> OPERATOR :", deleg_address[i], colors.fg.green, deleg_status[i], colors.reset)
				nI[i] = r
				maxN-=1
				break
			r+=1
			if (r == owner_pN):

				s = owner_N + maxN
				nI[i] = s
				print(colors.fg.blue, "NEW INDEX", colors.reset, "---> OPERATOR :", deleg_address[i], colors.fg.blue, deleg_status[i], colors.reset)
				maxN-=1
				break
		deleg_stake[i] = owner_json[l]["current_stake"]

		#-----------
		if (deleg_status[i] == "BACK"):
			w=0
			deleg_lastEpoch[i] = owner_json[l]["gone_epoch"]
			with open("data/gone_delegators.json") as json_file:
				gones_json = json.load(json_file)
				gones = gones_json["gone_delegators"]
				json_file.close()
			w = int(len(gones))
			w -= 1
			while (w >= 0):
				backDeleg_address[i] = gones[w]["gone"]
				if (backDeleg_address[i] == deleg_address[i]):
					backDeleg_goneEpoch[i] = gones[w]["last_epoch"]
					if (backDeleg_goneEpoch[i] < NewEpoch):
						backDeleg_index[i] = int(gones[w]["last_index"])
						backDelegs_N += 1
						print("===	COMING BACK	===")
						break
				w -= 1
			pruneDist = float((NewEpoch - REGISTRATION_EPOCH - 2)/PRUNE_NB)
			pruneD = (REGISTRATION_EPOCH + 2) + int(pruneDist)*PRUNE_NB
			pruneF = pruneD + (PRUNE_NB - 1)
			if (backDeleg_goneEpoch[i] < pruneF):

				distD = float((int(backDeleg_goneEpoch[i]) - 245)/PRUNE_NB)
				dH = 245 + int(distD)*PRUNE_NB
				fH = dH + (PRUNE_NB - 1)

				historyIndex = fH - int(backDeleg_goneEpoch[i])

				with open("data/history/pooldata_{}_{}.json".format(dH, fH)) as json_file:
					pooldata = json.load(json_file)
					json_file.close()
				history_data = pooldata[int(historyIndex)]["owners"]["owner"][int(backDeleg_index[i])]

			else:
				history_data = pooldata["history"][int(historyIndex)]["owners"]["owner"][int(backDeleg_index[i])]

			deleg_stake_previous[i] = history_data["stake"]["_epoch_"]
			deleg_stake_sum[i] = history_data["stake"]["_sum_"]
			deleg_stake_max[i] = history_data["stake"]["_lifetime_max_"]
			deleg_stake_min[i] = history_data["stake"]["_lifetime_min_"]
			deleg_stake_inputs[i] = history_data["stake"]["_inputs_sum_"]
			deleg_stake_outputs[i] = history_data["stake"]["_outputs_sum_"]
			deleg_rewards_sum[i] = history_data["rewards"]["_sum_"]
			deleg_epochCount[i] = int(history_data["epoch_count"])
			deleg_firstEpoch[i] = history_data["first_epoch"]
			deleg_sinceEpoch[i] = Nepoch
			deleg_ROA_max[i] = history_data["ROA"]["_max_"]
			deleg_comeBack[i] = True;
			deleg_comeBack_count[i] = int(history_data["comeback_count"]) + 1
			backStake = backStake + deleg_stake[i]

		elif (deleg_status[i] == "NEW"):
			deleg_stake_previous[i] = 0
			deleg_stake_sum[i] = 0
			deleg_stake_max[i] = 0
			deleg_stake_min[i] = 0
			deleg_stake_inputs[i] = 0
			deleg_stake_outputs[i] = 0
			deleg_rewards_sum[i] = 0
			deleg_ROA_max[i] = 0
			deleg_firstEpoch[i] = NewEpoch
			deleg_sinceEpoch[i] = NewEpoch
			deleg_epochCount[i] = 0;
			deleg_comeBack[i] = False;
			deleg_comeBack_count[i] = 0;

		else:
			deleg_data = owner_list[nI[i]]
			deleg_stake_previous[i] = deleg_data["stake"]["_epoch_"]
			deleg_stake_sum[i] = deleg_data["stake"]["_sum_"]
			deleg_stake_max[i] = deleg_data["stake"]["_lifetime_max_"]
			deleg_stake_min[i] = deleg_data["stake"]["_lifetime_min_"]
			deleg_stake_inputs[i] = deleg_data["stake"]["_inputs_sum_"]
			deleg_stake_outputs[i] = deleg_data["stake"]["_outputs_sum_"]
			if not deleg_stake_outputs[i]:
				deleg_stake_outputs[i] = 0
			deleg_rewards_sum[i] = deleg_data["rewards"]["_sum_"]
			deleg_ROA_max[i] = deleg_data["ROA"]["_max_"]
			deleg_epochCount[i] = int(deleg_data["epoch_count"])
			deleg_firstEpoch[i] = deleg_data["first_epoch"]
			deleg_sinceEpoch[i] = deleg_data["since_epoch"]
			deleg_comeBack[i] = deleg_data["comeback"]
			deleg_comeBack_count[i] = deleg_data["comeback_count"]

		#------------

		if (deleg_stake_min[i] == 0):
			deleg_stake_min[i] = deleg_stake[i]

		if (CountingEpoch):
			deleg_epochCount[i] = deleg_epochCount[i] + 1

		deleg_stake_diff[i] = deleg_stake[i] - deleg_stake_previous[i]
		deleg_stake_sum[i] = deleg_stake_sum[i] + deleg_stake[i]
		if (deleg_stake[i] > deleg_stake_max[i]):
			deleg_stake_max[i] = deleg_stake[i]
		elif (deleg_stake[i] < deleg_stake_min[i]):
			deleg_stake_min[i] = deleg_stake[i]

		if (deleg_stake_diff[i] > 0):
			deleg_stake_inputs[i] = int(deleg_stake_inputs[i]) + deleg_stake_diff[i];
		elif (deleg_stake_diff[i] < 0):
			deleg_stake_outputs[i] = int(deleg_stake_outputs[i]) + deleg_stake_diff[i];

		deleg_rewards[i] = owner_json[l]["rewards"]
		deleg_rewards_sum[i] = int(deleg_rewards_sum[i]) + int(deleg_rewards[i])
		ROA = setROA(deleg_epochCount[i], deleg_stake_sum[i], deleg_rewards_sum[i], 0)

		deleg_ROA[i] = ROA[0]
		if (deleg_ROA[i] > deleg_ROA_max[i]):
			deleg_ROA_max[i] = deleg_ROA[i]

		deleg_loyalty=0

		deleg_STRG[i] = '{ "stake_address": '+xx+deleg_address[i]+xx+', "first_epoch": '+str(deleg_firstEpoch[i])+', "since_epoch": '+str(deleg_sinceEpoch[i])+', "epoch_count": '+str(deleg_epochCount[i])+', "loyalty": '+str(deleg_loyalty)+', "comeback": '+xx+str(deleg_comeBack[i])+xx+', "comeback_count": '+str(deleg_comeBack_count[i])+', "stake": { "_epoch_": '+str(deleg_stake[i])+', "_previous_": '+str(deleg_stake_previous[i])+', "_diff_": '+str(deleg_stake_diff[i])+', "_sum_": '+str(deleg_stake_sum[i])+', "_lifetime_max_": '+str(deleg_stake_max[i])+', "_lifetime_min_": '+str(deleg_stake_min[i])+', "_inputs_sum_": '+str(deleg_stake_inputs[i])+', "_outputs_sum_": '+str(deleg_stake_outputs[i])+'}, "rewards": { "_epoch_": '+str(deleg_rewards[i])+', "_sum_": '+str(deleg_rewards_sum[i])+'}, "ROA": { "_lifetime_": '+str(deleg_ROA[i])+', "_max_": '+str(deleg_ROA_max[i])+'}}'
		print(deleg_STRG[i])
		delegators_stake = delegators_stake + deleg_stake[i]

		delegators_rewards = delegators_rewards + deleg_rewards[i]


		i+=1
		print("======================================================================================")

	with open("data/pool_data.json") as json_file:
		pooldata = json.load(json_file)
		json_file.close()
	delegators_data = pooldata["owners"]

	backDelegs_sum = delegators_data["back_owners_sum"]
	backDelegs_sum = backDelegs_sum + backDelegs_N

	delegators_stake_previous = delegators_data["pledge"]["_epoch_"]
	delegators_stake_sum = delegators_data["pledge"]["_sum_"]
	delegators_stake_max = delegators_data["pledge"]["_lifetime_max_"]
	delegators_stake_min = delegators_data["pledge"]["_lifetime_min_"]
	delegators_stake_inputs = delegators_data["pledge"]["_inputs_sum_"]
	delegators_stake_outputs = delegators_data["pledge"]["_outputs_sum_"]
	delegators_N = owner_N
	delegators_N_previous = delegators_data["ownersNb"]
	delegators_N_max = delegators_data["lifetime_max_ownersNb"]
	delegators_N_min = delegators_data["lifetime_min_ownersNb"]
	delegators_rewards_sum = delegators_data["rewards"]["_sum_"]

	delegators_stake_sum = delegators_stake_sum + delegators_stake
	delegators_stake_diff = delegators_stake - delegators_stake_previous
	delegators_rewards_sum = delegators_rewards_sum + delegators_rewards

	if (delegators_stake_diff > 0):
		delegators_stake_inputs = delegators_stake_inputs + delegators_stake_diff
	elif (delegators_stake_diff < 0):
		delegators_stake_outputs = delegators_stake_outputs + delegators_stake_diff

	if (delegators_stake > delegators_stake_max):
		delegators_stake_max = delegators_stake
	elif (delegators_stake < delegators_stake_min or delegators_stake_min == 0):
		delegators_stake_min = delegators_stake

	if (delegators_N > delegators_N_max):
		delegators_N_max = delegators_N
	elif (delegators_N < delegators_N_min or delegators_N_min == 0):
		delegators_N_min = delegators_N


	dROA = setROA(poolEpochCount, delegators_stake_sum, delegators_rewards_sum, delegators_bonus_sum)
	delegators_ROA = dROA[0]
	delegators_ROA_bonus = dROA[1]
	delegators_ROA_max = delegators_data["ROA"]["_max_"]

	if (delegators_ROA > delegators_ROA_max):
		delegators_ROA_max = delegators_ROA

	o = 0
	delegsStrg = ""
	while (o < owner_N):
		if (o < owner_N - 1):
			delegsStrg = delegsStrg+deleg_STRG[o]+',\n'
		else:
			delegsStrg = delegsStrg+deleg_STRG[o]
		o += 1
	owners_biggest_ever = delegators_data["pledge"]["_biggest_ever_"]
	owners_biggest = checkBiggest(delegsStrg)
	if (owners_biggest > owners_biggest_ever):
		owners_biggest_ever = owners_biggest


	delegators_stakeSTRG = '{ "_epoch_": '+str(delegators_stake)+', "_previous_": '+str(delegators_stake_previous)+', "_diff_": '+str(delegators_stake_diff)+', "_sum_": '+str(delegators_stake_sum)+', "_lifetime_max_": '+str(delegators_stake_max)+', "_lifetime_min_": '+str(delegators_stake_min)+', "_inputs_sum_": '+str(delegators_stake_inputs)+', "_outputs_sum_": '+str(delegators_stake_outputs)+', "_biggest_ever_": '+str(owners_biggest_ever)+'}'
	delegators_rewardsSTRG = '{ "_epoch_": '+str(delegators_rewards)+', "_sum_": '+str(delegators_rewards_sum)+'}'
	delegators_ROASTRG = '{ "_lifetime_": '+str(delegators_ROA)+', "_max_": '+str(delegators_ROA_max)+', "_bonuses_included_": '+str(delegators_ROA_bonus)+'}'
	delegators_STRG = '"owners": { "ownersNb": '+str(delegators_N)+', "previous_ownersNb": '+str(delegators_N_previous)+', "lifetime_max_ownersNb": '+str(delegators_N_max)+', "lifetime_min_ownersNb": '+str(delegators_N_min)+', "back_owners": '+str(backDelegs_N)+', "back_owners_sum": '+str(backDelegs_sum)+', "pledge": '+delegators_stakeSTRG+', "rewards": '+delegators_rewardsSTRG+', "ROA": '+delegators_ROASTRG+', "owner": [\n'+delegsStrg+']}'

	print("===================================================================",colors.fg.green,"OWNERS DONE",colors.reset)
	return delegators_STRG

######################### POOL DATA SETTING #####################################################################################
def setPoolData(Nepoch, owners_STRG, delegators_STRG, bonus_list, blocks_list, countEpoch):
	CountingEpoch = countEpoch
	epochCount = Nepoch - REGISTRATION_EPOCH - 1
	print(colors.fg.orange,"\n======================== POOL DATA SETTING ==========================================",colors.reset)
	with open("data/pool_data.json") as json_file:
		pooldata = json.load(json_file)
		json_file.close()

	d_STRG = str('{'+delegators_STRG+'}')
	d_json = json.loads(d_STRG)
	o_STRG = str('{'+owners_STRG+'}')
	o_json = json.loads(o_STRG)

	dd_stake = d_json["delegators"]["stake"]["_epoch_"]
	oo_pledge = o_json["owners"]["pledge"]["_epoch_"]
	pool_stake = dd_stake + oo_pledge
	pool_stake_previous = pooldata["pool"]["stake"]["_epoch_"]
	pool_stake_diff = pool_stake - pool_stake_previous
	pool_stake_sum = pooldata["pool"]["stake"]["_sum_"]
	pool_stake_sum = pool_stake_sum + pool_stake
	pool_stake_max = pooldata["pool"]["stake"]["_lifetime_max_"]
	pool_stake_min = pooldata["pool"]["stake"]["_lifetime_min_"]
	if (pool_stake > pool_stake_max):
		pool_stake_max = pool_stake
	elif (pool_stake < pool_stake_min or pool_stake_min == 0):
		pool_stake_min = pool_stake
	pool_stake_inputs = pooldata["pool"]["stake"]["_inputs_sum_"]
	pool_stake_outputs = pooldata["pool"]["stake"]["_outputs_sum_"]
	if (pool_stake_diff > 0):
		pool_stake_inputs = pool_stake_inputs + pool_stake_diff
	elif (pool_stake < 0):
		pool_stake_outputs = pool_stake_outputs + pool_stake_diff
	dd_rewards = d_json["delegators"]["rewards"]["_epoch_"]
	oo_rewards = o_json["owners"]["rewards"]["_epoch_"]
	pool_rewards = dd_rewards + oo_rewards
	pool_rewards_sum = pooldata["pool"]["rewards"]["_sum_"]
	pool_rewards_sum = pool_rewards_sum + pool_rewards
	p_ROA = setROA(epochCount, pool_stake_sum, pool_rewards_sum, 0)
	pool_ROA = p_ROA[0]
	pool_ROA_max = pooldata["pool"]["ROA"]["_max_"]
	if (pool_ROA > pool_ROA_max):
		pool_ROA_max = pool_ROA

	pool_lost = checkGoneAndLost(Nepoch)
	pool_gone_N_sum = pooldata["pool"]["lost"]["lost_delegs_sum"]
	pool_stake_lost_sum = pooldata["pool"]["lost"]["lost_stake_sum"]
	pool_gone_N = pool_lost[0]
	pool_stake_lost = pool_lost[1]
	pool_gone_N_sum = pool_gone_N_sum + pool_gone_N
	pool_stake_lost_sum = pool_stake_lost_sum + pool_stake_lost

	pool_STRG = '"pool": { "stake": { "_epoch_": '+str(pool_stake)+', "_previous_": '+str(pool_stake_previous)+', "_diff_": '+str(pool_stake_diff)+', "_sum_": '+str(pool_stake_sum)+', "_lifetime_max_": '+str(pool_stake_max)+', "_lifetime_min_": '+str(pool_stake_min)+', "_inputs_sum_": '+str(pool_stake_inputs)+', "_outputs_sum_": '+str(pool_stake_outputs)+'}, "rewards": { "_epoch_": '+str(pool_rewards)+', "_sum_": '+str(pool_rewards_sum)+'}, "lost": { "lost_delegs_nb": '+str(pool_gone_N)+', "lost_delegs_sum": '+str(pool_gone_N_sum)+', "lost_stake": '+str(pool_stake_lost)+', "lost_stake_sum": '+str(pool_stake_lost_sum)+'}, "ROA": { "_lifetime_" : '+str(pool_ROA)+', "_max_": '+str(pool_ROA_max)+'} }'
#	print(pool_STRG)
	print("===================================================================",colors.fg.green,"POOL DONE",colors.reset)
	return pool_STRG

######################### MAIN FUNCTION #########################################################################################
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

def setHistory(Nepoch):
	Oepoch = Nepoch - 1
	cc = "'"
	xx = '"'
	with open("data/pool_data.json") as json_file:
		data_json = json.load(json_file)
		json_file.close()
	history_data = data_json["history"]
	history_N = len(history_data)
	pool_data = data_json["pool"]
	owners_data = data_json["owners"]
	delegators_data = data_json["delegators"]
	deleg_data = delegators_data["delegator"]
	dHH = str(delegators_data).replace(str(deleg_data), '')
	dHH = dHH[0:-1]
	Nd = len(deleg_data)
	n = 0; NDD = '['
	while (n < Nd):
		bd = ', "_previous_": '.replace(xx,cc)
		bd = bd+str(deleg_data[n]["bonuses"]["_previous_"])
		ndd = str(deleg_data[n]).replace(bd, '')
		if (n < Nd - 1):
			NDD = NDD+ndd+','
		else:
			NDD = NDD+ndd+']'
		n += 1
	dHH = dHH+NDD+'}'
	blocks_data = data_json["blocks"]
	blH_data = blocks_data["history"]
	blH = ", 'history': "+str(blH_data)
	blHH = str(blocks_data).replace(blH, '')
	bonus_data = data_json["bonuses"]
	bH_data = bonus_data["history"]
	bH = ', "history": '.replace(xx,cc)+str(bH_data)
	bHH = str(bonus_data).replace(bH,'')

	if (Oepoch >= REGISTRATION_EPOCH + 2):
		history_STRG = '{ "epoch": '+str(Oepoch)+', "pool": '+str(pool_data)+', "owners": '+str(owners_data)+', "delegators": '+str(dHH)+', "blocks": '+str(blHH)+', "bonuses": '+str(bHH)+'}'
		if (history_N < PRUNE_NB and Oepoch > REGISTRATION_EPOCH + 2 and history_data):
			history_STRG = history_STRG+','+str(history_data)[1:-1]
		history_STRG = '['+history_STRG.replace(cc, xx)+']'
	else:
		history_STRG = '[]'

	return history_STRG

######################### MAIN FUNCTION #########################################################################################
def setData(Nepoch):
	cc = "'"
	xx = '"'
	Oepoch = Nepoch - 1

	header_STRG = setHeader(Nepoch)
	owner_index = setOwnersIndex(Nepoch)
	deleg_index = setDelegsIndex(Nepoch)
	bonus_list = checkBonus(Nepoch)
	bonus_STRG = setBonus(Nepoch, bonus_list)
	blocks_STRG = checkBlocks(Nepoch).replace(cc, xx)
	delegators_STRG = setDelegsData(Nepoch, deleg_index, bonus_list, True)
	owners_STRG = setOwnersData(Nepoch, owner_index, True)
	pool_STRG = setPoolData(Nepoch, owners_STRG, delegators_STRG, bonus_list, 0, True)
	history_STRG = setHistory(Nepoch)
	if (str(history_STRG) != "[]"):

		history_J = json.loads(str(history_STRG))
		if (len(history_J) == 10):
			Nhist = float((Nepoch - REGISTRATION_EPOCH - 2)/10)
			dH = (REGISTRATION_EPOCH + 2) + (int(Nhist)-1)*10
			dF = dH + 9
			with open("data/history/pooldata_{}_{}.json".format(dH, dF), "w") as file:
				file.write(history_STRG)
				file.close()
			data_STRG = header_STRG +'\n '+str(blocks_STRG)+',\n "bonuses": '+str(bonus_STRG)+',\n'+pool_STRG+',\n'+owners_STRG+',\n'+delegators_STRG+',\n "history": []}'
		else:
			data_STRG = header_STRG +'\n '+str(blocks_STRG)+',\n "bonuses": '+str(bonus_STRG)+',\n'+pool_STRG+',\n'+owners_STRG+',\n'+delegators_STRG+',\n "history": '+history_STRG+'}'

	else:

		data_STRG = header_STRG +'\n '+str(blocks_STRG)+',\n "bonuses": '+str(bonus_STRG)+',\n'+pool_STRG+',\n'+owners_STRG+',\n'+delegators_STRG+',\n "history": '+history_STRG+'}'

	with open("data/pool_data.json", "w") as file:
		file.write(data_STRG)
		file.close()


#setDelegsIndex(468)
