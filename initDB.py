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

import datetime
import json
from config import REGISTRATION_EPOCH, PRUNE_NB
from colors import colors
import mysql.connector

mydb = mysql.connector.connect(
	host="YOUR-HOST",
	port="YOUR-PORT",
	user="YOUR-USERNAME",
	password="YOUR-PASSWORD",
	database="pool_DB"
)

mycursor = mydb.cursor();


def getFileData(Nepoch):
	currentEpoch = 479
	distC = int(float((currentEpoch - REGISTRATION_EPOCH - 2)/PRUNE_NB))

	distE = int(float((currentEpoch - Nepoch)/PRUNE_NB))

	distH = distC - distE

	sEH = (REGISTRATION_EPOCH + 2) + distH*PRUNE_NB
	eEH = sEH + (PRUNE_NB - 1)


	if (distE < 1):
		if (Nepoch == currentEpoch):
			print(Nepoch, "0", "epoch en cours")
			with open('data/pool_data.json') as json_file:
				z = json.load(json_file)
				json_file.close()
				oh = ", 'history': "+str(z["history"])
				data_H = str(z).replace(oh, "")
		elif (Nepoch >= sEH):
			with open('data/pool_data.json') as json_file:
				z = json.load(json_file)
				json_file.close()
			print(Nepoch, "1", sEH, eEH, "within pool_data")
			index = currentEpoch - Nepoch - 1
			data_H = z["history"][index]
		elif (Nepoch < sEH):
			sEH = sEH - PRUNE_NB; eEH = eEH - PRUNE_NB
			file = "data/history/pooldata_{}_{}.json".format(sEH, eEH)
			with open(file) as json_file:
				z = json.load(json_file)
				json_file.close()
			print(Nepoch, "2", file)
			index = eEH - Nepoch
			data_H = z[index]
	else:
		if (Nepoch > eEH or Nepoch < sEH):
			sEH = sEH - PRUNE_NB; eEH = eEH - PRUNE_NB

		file = "data/history/pooldata_{}_{}.json".format(sEH, eEH)
		with open(file) as json_file:
			z = json.load(json_file)
			json_file.close()
		print(Nepoch, "3", file)
		index = eEH - Nepoch
		data_H = z[index]
#	print(data_H)
	return data_H

#getFileData(254)
#getFileData(478)
#getFileData(474)
#getFileData(475)
#getFileData(479)
############### SET DATA HISTORY ####################
def setDataHistory(data_H):

	ds_back_sum=0;

	oh = data_H;
	e = oh["epoch"];
	print(colors.fg.green, "----------- UPDATING EPOCH", colors.reset, e, colors.fg.green, " IN PROGRESS ----------", colors.reset);
	ds_back_sum=getPoolDataHistory(oh, e, ds_back_sum);
	getOwnersDataHistory(oh, e);
	getDelegatorsDataHistory(oh, e);
	getBlocksDataHistory(oh, e);
	print(colors.fg.green, "----------- EPOCH", colors.reset, e, colors.fg.green, "DONE ----------", colors.reset);
	print("=========================================================================================");


############### GET POOL DATA #######################
def getPoolDataHistory(x, y, w):

	p = x["pool"];
	os = x["owners"];
	ds = x["delegators"];
	bns = x["bonuses"];
	blk = x["blocks"];
	epoch = y;
	##### pool #########
	p_StakeStrg = p["stake"];
	p_RewardsStrg = p["rewards"];
	p_LostStrg = p["lost"];
	p_ROAStrg = p["ROA"];
	p_Stake_current = p_StakeStrg["_epoch_"];
	p_Stake_previous = p_StakeStrg["_previous_"];
	p_Stake_sum = p_StakeStrg["_sum_"];
	p_Stake_diff = p_StakeStrg["_diff_"];
	p_Stake_max = p_StakeStrg["_lifetime_max_"];
	p_Stake_min = p_StakeStrg["_lifetime_min_"];
	p_Stake_inputs = p_StakeStrg["_inputs_sum_"];
	p_Stake_outputs = p_StakeStrg["_outputs_sum_"];
	p_Lost_stake = p_LostStrg["lost_stake"];
	p_Lost_stake_sum = p_LostStrg["lost_stake_sum"];
	p_Lost_delegs = p_LostStrg["lost_delegs_nb"];
	p_Lost_delegs_sum = p_LostStrg["lost_delegs_sum"];
	p_Rewards_current = p_RewardsStrg["_epoch_"];
	p_Rewards_sum = p_RewardsStrg["_sum_"];
	p_ROA_current = p_ROAStrg["_lifetime_"];
	p_ROA_max = p_ROAStrg["_max_"];
	##### owners #######
	os_StakeStrg = os["pledge"];
	os_RewardsStrg = os["rewards"];
	os_ROAStrg = os["ROA"];
	os_number = os["ownersNb"];
	os_Stake_current = os_StakeStrg["_epoch_"];
	os_Stake_previous = os_StakeStrg["_previous_"];
	os_Stake_sum = os_StakeStrg["_sum_"];
	os_Stake_diff = os_StakeStrg["_diff_"];
	os_Stake_max = os_StakeStrg["_lifetime_max_"];
	os_Stake_min = os_StakeStrg["_lifetime_min_"];
	os_Stake_inputs = os_StakeStrg["_inputs_sum_"];
	os_Stake_outputs = os_StakeStrg["_outputs_sum_"];
	p_biggest_pledge = os_StakeStrg["_biggest_ever_"];
	os_Rewards_current = os_RewardsStrg["_epoch_"];
	os_Rewards_sum = os_RewardsStrg["_sum_"];
	os_ROA_current = os_ROAStrg["_lifetime_"];
	os_ROA_max = os_ROAStrg["_max_"];
	##### delegators ####
	ds_StakeStrg = ds["stake"];
	ds_RewardsStrg = ds["rewards"];
	ds_ROAStrg = ds["ROA"];
	ds_number = ds["delegsNb"];
	ds_back = ds["back_delegs"];
	ds_back_sum = w + ds_back;
	ds_Stake_current = ds_StakeStrg["_epoch_"];
	ds_Stake_previous = ds_StakeStrg["_previous_"];
	ds_Stake_sum = ds_StakeStrg["_sum_"];
	ds_Stake_diff = ds_StakeStrg["_diff_"];
	ds_Stake_max = ds_StakeStrg["_lifetime_max_"];
	ds_Stake_min = ds_StakeStrg["_lifetime_min_"];
	ds_Stake_inputs = ds_StakeStrg["_inputs_sum_"];
	ds_Stake_outputs = ds_StakeStrg["_outputs_sum_"];
	p_biggest_stake = ds_StakeStrg["_biggest_ever_"];
	ds_Rewards_current = ds_RewardsStrg["_epoch_"];
	ds_Rewards_sum = ds_RewardsStrg["_sum_"];
	ds_ROA_current = ds_ROAStrg["_lifetime_"];
	ds_ROA_max = ds_ROAStrg["_max_"];
	ds_ROA_bonusincluded = ds_ROAStrg["_bonuses_included_"];
	##### bonuses ########
	bns_Bonus_current = bns["amount"];
	bns_Bonus_sum = bns["_sum_"];
	##### blocks #########
	blk_blocks_current = blk["epoch"];
	blk_blocks_sum = blk["total_blocks"];


	sqlEpoch = "INSERT INTO epoch (epoch_number, pool_stake, pool_stake_previous, pool_stake_sum, pool_stake_diff, pool_stake_max, pool_stake_min, pool_stake_inputs_sum, pool_stake_outputs_sum, biggest_single_owner_pledge, biggest_single_delegator_stake, pool_rewards, pool_rewards_sum, pool_ROA_current, pool_ROA_max, owners_nb, pledge, pledge_previous, pledge_sum, pledge_diff, pledge_max, pledge_min, pledge_inputs_sum, pledge_outputs_sum, owners_rewards, owners_rewards_sum, owners_ROA_current, owners_ROA_max, delegators_nb, delegators_back_count, delegators_back_sum, delegators_lost_count, delegators_lost_sum, delegators_stake, delegators_stake_previous, delegators_stake_sum, delegators_stake_diff, delegators_stake_max, delegators_stake_min, delegators_stake_inputs_sum, delegators_stake_outputs_sum, delegators_lost_stake, delegators_lost_stake_sum, delegators_rewards, delegators_rewards_sum, delegators_ROA_current, delegators_ROA_max, delegators_ROA_bonusincluded, blocks, blocks_sum, bonuses, bonuses_sum) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE pool_stake = %s, pool_stake_previous = %s, pool_stake_sum = %s, pool_stake_diff = %s, pool_stake_max = %s, pool_stake_min = %s, pool_stake_inputs_sum = %s, pool_stake_outputs_sum = %s, biggest_single_owner_pledge = %s, biggest_single_delegator_stake = %s, pool_rewards = %s, pool_rewards_sum = %s, pool_ROA_current = %s, pool_ROA_max = %s, owners_nb = %s, pledge = %s, pledge_previous = %s, pledge_sum = %s, pledge_diff = %s, pledge_max = %s, pledge_min = %s, pledge_inputs_sum = %s, pledge_outputs_sum = %s, owners_rewards = %s, owners_rewards_sum = %s, owners_ROA_current = %s, owners_ROA_max = %s, delegators_nb = %s, delegators_back_count = %s, delegators_back_sum = %s, delegators_lost_count = %s, delegators_lost_sum = %s, delegators_stake = %s, delegators_stake_previous = %s, delegators_stake_sum = %s, delegators_stake_diff = %s, delegators_stake_max = %s, delegators_stake_min = %s, delegators_stake_inputs_sum = %s, delegators_stake_outputs_sum = %s, delegators_lost_stake = %s, delegators_lost_stake_sum = %s, delegators_rewards = %s, delegators_rewards_sum = %s, delegators_ROA_current = %s, delegators_ROA_max = %s, delegators_ROA_bonusincluded = %s, blocks = %s, blocks_sum = %s, bonuses = %s, bonuses_sum = %s";
	valEpochA = (epoch,p_Stake_current,p_Stake_previous,p_Stake_sum,p_Stake_diff,p_Stake_max,p_Stake_min,p_Stake_inputs,p_Stake_outputs,p_biggest_pledge,p_biggest_stake,p_Rewards_current,p_Rewards_sum,p_ROA_current,p_ROA_max,os_number,os_Stake_current,os_Stake_previous,os_Stake_sum,os_Stake_diff,os_Stake_max,os_Stake_min,os_Stake_inputs,os_Stake_outputs,os_Rewards_current,os_Rewards_sum,os_ROA_current,os_ROA_max,ds_number,ds_back, ds_back_sum,p_Lost_delegs,p_Lost_delegs_sum,ds_Stake_current,ds_Stake_previous,ds_Stake_sum,ds_Stake_diff,ds_Stake_max,ds_Stake_min,ds_Stake_inputs,ds_Stake_outputs,p_Lost_stake,p_Lost_stake_sum,ds_Rewards_current,ds_Rewards_sum,ds_ROA_current,ds_ROA_max,ds_ROA_bonusincluded,blk_blocks_current,blk_blocks_sum,bns_Bonus_current,bns_Bonus_sum);
	valEpochB = (p_Stake_current,p_Stake_previous,p_Stake_sum,p_Stake_diff,p_Stake_max,p_Stake_min,p_Stake_inputs,p_Stake_outputs,p_biggest_pledge,p_biggest_stake,p_Rewards_current,p_Rewards_sum,p_ROA_current,p_ROA_max,os_number,os_Stake_current,os_Stake_previous,os_Stake_sum,os_Stake_diff,os_Stake_max,os_Stake_min,os_Stake_inputs,os_Stake_outputs,os_Rewards_current,os_Rewards_sum,os_ROA_current,os_ROA_max,ds_number,ds_back, ds_back_sum,p_Lost_delegs,p_Lost_delegs_sum,ds_Stake_current,ds_Stake_previous,ds_Stake_sum,ds_Stake_diff,ds_Stake_max,ds_Stake_min,ds_Stake_inputs,ds_Stake_outputs,p_Lost_stake,p_Lost_stake_sum,ds_Rewards_current,ds_Rewards_sum,ds_ROA_current,ds_ROA_max,ds_ROA_bonusincluded,blk_blocks_current,blk_blocks_sum,bns_Bonus_current,bns_Bonus_sum);
	valEpoch = valEpochA + valEpochB;
	mycursor.execute(sqlEpoch, valEpoch)
	mydb.commit()
	return ds_back_sum

############## GET OWNERS DATA ######################
def getOwnersDataHistory(x, y):

	os = x["owners"];
	epoch = y;
	o_Strg = os["owner"];
	lo = len(o_Strg);
	k = 0
	while k < lo :
		o_Address = o_Strg[k]["stake_address"];
		if not o_Address :
			k += 1;
			continue;
		o_SinceEpoch = o_Strg[k]["since_epoch"];

		o_GoneEpoch = 0 #o_Strg[k]["gone_epoch"];
		o_epoch_count = o_Strg[k]["epoch_count"];
		o_Score = o_Strg[k]["loyalty"];

		o_StakeStrg = o_Strg[k]["stake"];
		o_Stake_current = o_StakeStrg["_epoch_"]; 
		o_Stake_previous = o_StakeStrg["_previous_"];

		o_Stake_sum = o_StakeStrg["_sum_"];

		o_Stake_diff = o_StakeStrg["_diff_"];

		o_Stake_max = o_StakeStrg["_lifetime_max_"];

		o_Stake_min = o_StakeStrg["_lifetime_min_"];

		o_Stake_inputs = o_StakeStrg["_inputs_sum_"];

		o_Stake_outputs = o_StakeStrg["_outputs_sum_"];

		o_RewardsStrg = o_Strg[k]["rewards"];
		o_Rewards_current = o_RewardsStrg["_epoch_"];

		o_Rewards_sum = o_RewardsStrg["_sum_"];
		o_ROAStrg = o_Strg[k]["ROA"];
		o_ROA_current = o_ROAStrg["_lifetime_"];
		o_ROA_max= o_ROAStrg["_max_"];

		print(colors.fg.blue,"EPOCH :",colors.reset, epoch, colors.fg.cyan, "POOL OPERATOR address :", colors.reset, o_Address);


		#### ENTREE dans la table OWNER #########
		sqlOwner = "INSERT INTO owner (stake_address, since_epoch, gone_epoch, epoch_count, loyalty, pledge, pledge_sum, pledge_previous, pledge_diff, pledge_max, pledge_min, rewards, rewards_sum, inputs_sum, outputs_sum, ROA_current, ROA_max) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE since_epoch = %s, gone_epoch = %s, epoch_count = %s, loyalty = %s, pledge = %s, pledge_sum = %s, pledge_previous = %s, pledge_diff = %s, pledge_max = %s, pledge_min = %s, rewards = %s, rewards_sum = %s, inputs_sum = %s, outputs_sum = %s, ROA_current = %s, ROA_max = %s  ";
		valOwner = (o_Address, o_SinceEpoch, o_GoneEpoch, o_epoch_count, o_Score, o_Stake_current, o_Stake_sum, o_Stake_previous, o_Stake_diff, o_Stake_max, o_Stake_min, o_Rewards_current, o_Rewards_sum, o_Stake_inputs, o_Stake_outputs, o_ROA_current, o_ROA_max, o_SinceEpoch, o_GoneEpoch, o_epoch_count, o_Score, o_Stake_current, o_Stake_sum, o_Stake_previous, o_Stake_diff, o_Stake_max, o_Stake_min, o_Rewards_current, o_Rewards_sum, o_Stake_inputs, o_Stake_outputs, o_ROA_current, o_ROA_max);
		mycursor.execute(sqlOwner, valOwner);
		mydb.commit();

		#### ENTREE dans la table PLEDGE ########
		sqlOwnerPledge = "INSERT INTO pledge (owner_stake_address, epoch_epoch_number, amount, sum, previous, diff, max, min, inputs_sum, outputs_sum, ROA_current, ROA_max) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE amount = %s, sum = %s, previous = %s, diff = %s, max = %s, min = %s, inputs_sum = %s, outputs_sum = %s, ROA_current = %s, ROA_max = %s";
		valOwnerPledgeA =(o_Address, epoch, o_Stake_current, o_Stake_sum, o_Stake_previous, o_Stake_diff, o_Stake_max, o_Stake_min, o_Stake_inputs, o_Stake_outputs, o_ROA_current, o_ROA_max);
		valOwnerPledgeB = (o_Stake_current, o_Stake_sum, o_Stake_previous, o_Stake_diff, o_Stake_max, o_Stake_min, o_Stake_inputs, o_Stake_outputs, o_ROA_current, o_ROA_max);
		valOwnerPledge = valOwnerPledgeA + valOwnerPledgeB;
		mycursor.execute(sqlOwnerPledge, valOwnerPledge);
		mydb.commit();

		if o_Rewards_current > 0 :
			#### ENTREE dans la table OWNER_REWARDS #####
			sqlORewards = "INSERT INTO owner_rewards (amount, sum, epoch_epoch_number, owner_stake_address) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE amount = %s, sum = %s";
			valORewards = (o_Rewards_current, o_Rewards_sum, y, o_Address, o_Rewards_current, o_Rewards_sum);
			mycursor.execute(sqlORewards, valORewards);
			mydb.commit();
		print("---------------------------------------------------------------", colors.fg.green, "DONE", colors.reset);
		k += 1

############## GET DELEGATORS DATA ######################
def getDelegatorsDataHistory(x, y):
	ds = x["delegators"];
	epoch = y;
	d_Strg = ds["delegator"];
	ld=len(d_Strg);
	print(ld, "DELEGATORS this epoch");

	j = 0
	while j < ld :
		i = 0;
		d_Address = d_Strg[j]["stake_address"];
		d_SinceEpoch = d_Strg[j]["since_epoch"];
		d_epoch_count = d_Strg[j]["epoch_count"];
		d_loyalty = d_Strg[j]["loyalty"];
		d_comeback = d_Strg[j]["comeback"];
		if (d_comeback == "False"):
			d_comeback = 0
		else:
			d_comeback = 1
		d_comeback_count = d_Strg[j]["comeback_count"];
		d_StakeStrg = d_Strg[j]["stake"];
		d_Stake_current = d_StakeStrg["_epoch_"];
		d_Stake_previous = d_StakeStrg["_previous_"];
		d_Stake_sum = d_StakeStrg["_sum_"];
		d_Stake_diff = d_StakeStrg["_diff_"];
		d_Stake_inputs = d_StakeStrg["_inputs_sum_"];
		d_Stake_outputs = d_StakeStrg["_outputs_sum_"];
		d_Stake_max = d_StakeStrg["_lifetime_max_"];
		d_Stake_min = d_StakeStrg["_lifetime_min_"];
		d_ROAStrg = d_Strg[j]["ROA"];
		d_ROA_current = d_ROAStrg["_lifetime_"];
		d_ROA_max = d_ROAStrg["_max_"];
		d_ROA_bonusincluded = d_ROAStrg["_bonuses_included_"];
		d_bonusStrg = d_Strg[j]["bonuses"];
		d_bonus_amount = d_bonusStrg["amount"];
		d_bonus_sum = d_bonusStrg["_sum_"];
		d_rewardsStrg = d_Strg[j]["rewards"];
		d_rewards_sum = d_rewardsStrg["_sum_"];
		d_rewards_current = d_rewardsStrg["_epoch_"]


		#### ENTREE dans la table DELEGATOR ####
		sqlDelegator = "INSERT INTO delegator (stake_address, since_epoch, epoch_count, loyalty, comeback, comeback_count, stake, stake_sum, stake_previous, stake_diff, stake_max, stake_min, inputs_sum, outputs_sum, ROA_current, ROA_max, ROA_bonus_included, bonus, bonus_sum, rewards, rewards_sum) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE since_epoch=%s, epoch_count = %s, loyalty = %s, comeback = %s, comeback_count = %s, stake = %s, stake_sum = %s, stake_previous = %s, stake_diff = %s, stake_max = %s, stake_min = %s, inputs_sum = %s, outputs_sum = %s, ROA_current = %s, ROA_max = %s, ROA_bonus_included = %s, bonus = %s, bonus_sum = %s, rewards = %s, rewards_sum = %s";
		valDeleg = (d_Address, d_SinceEpoch, d_epoch_count, d_loyalty, d_comeback, d_comeback_count, d_Stake_current, d_Stake_sum, d_Stake_previous, d_Stake_diff, d_Stake_max, d_Stake_min, d_Stake_inputs, d_Stake_outputs, d_ROA_current, d_ROA_max, d_ROA_bonusincluded, d_bonus_amount, d_bonus_sum, d_rewards_current, d_rewards_sum, d_SinceEpoch, d_epoch_count, d_loyalty, d_comeback, d_comeback_count, d_Stake_current, d_Stake_sum, d_Stake_previous, d_Stake_diff, d_Stake_max, d_Stake_min, d_Stake_inputs, d_Stake_outputs, d_ROA_current, d_ROA_max, d_ROA_bonusincluded, d_bonus_amount, d_bonus_sum, d_rewards_current, d_rewards_sum)
		mycursor.execute(sqlDelegator, valDeleg);
		mydb.commit();

		#### ENTREE dans la table STAKE ########
		sqlDelegatorStake = "INSERT INTO stake (delegator_stake_address, epoch_epoch_number, amount, sum, previous, diff, max, min, inputs_sum, outputs_sum) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE amount = %s, sum = %s, previous = %s, diff = %s, max = %s, min = %s, inputs_sum = %s, outputs_sum = %s";
		valDelegStakeA =(d_Address, epoch, d_Stake_current, d_Stake_sum, d_Stake_previous, d_Stake_diff, d_Stake_max, d_Stake_min, d_Stake_inputs, d_Stake_outputs);
		valDelegStakeB = (d_Stake_current, d_Stake_sum, d_Stake_previous, d_Stake_diff, d_Stake_max, d_Stake_min, d_Stake_inputs, d_Stake_outputs);
		valDelegStake = valDelegStakeA + valDelegStakeB;
		mycursor.execute(sqlDelegatorStake, valDelegStake);
		mydb.commit();

		if d_bonus_amount > 0 :
			#### ENTREE dans la table BONUS #######
			sqlBonus = "INSERT INTO bonus (amount, sum, epoch_epoch_number, delegator_stake_address) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE amount = %s, sum = %s";
			valBonusA = (d_bonus_amount, d_bonus_sum, y, d_Address);
			valBonusB = (d_bonus_amount, d_bonus_sum);
			valBonus = valBonusA + valBonusB;
			mycursor.execute(sqlBonus, valBonus);
			mydb.commit();
			d_AssetStrg = d_bonusStrg["assets"];
			l_Assets=len(d_AssetStrg);
			a=0;
			while a < l_Assets :
				d_asset_name = d_AssetStrg[a]["name"];
				d_asset_amount = d_AssetStrg[a]["amount"];
				d_asset_policy = d_AssetStrg[a]["policyID"];
				d_asset_hashname = d_AssetStrg[a]["name_hash"];
				d_asset_fingerprint = d_AssetStrg[a]["fingerprint"];
				sqlAsset = "INSERT INTO assets (epoch_epoch_number, delegator_stake_address, name, amount, policyID, name_hash, fingerprint) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = %s, amount = %s, policyID = %s, name_hash = %s, fingerprint = %s";
				valAssetA = (y, d_Address, d_asset_name, d_asset_amount, d_asset_policy, d_asset_hashname, d_asset_fingerprint);
				valAssetB = (d_asset_name, d_asset_amount, d_asset_policy, d_asset_hashname, d_asset_fingerprint);
				valAsset = valAssetA + valAssetB;
				mycursor.execute(sqlAsset, valAsset);
				mydb.commit();
				a+=1;


		if d_rewards_current > 0 :
			#### ENTREE dans la table REWARDS #####
			sqlRewards = "INSERT INTO rewards (amount, sum, epoch_epoch_number, delegator_stake_address) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE amount = %s, sum = %s";
			valRewards = (d_rewards_current, d_rewards_sum, y, d_Address, d_rewards_current, d_rewards_sum);
			mycursor.execute(sqlRewards, valRewards);
			mydb.commit();

		print(colors.fg.blue, "EPOCH: ",colors.reset, epoch, colors.fg.cyan, 'STAKEHOLDER address:', colors.reset, d_Address);
		print("---------------------------------------------------------------", colors.fg.green, "DONE", colors.reset);

		j += 1



################ GET BLOCKS HISTORY ###################
def getBlocksDataHistory(x, y):

	bStrg = x["blocks"];
	blkNB = bStrg["epoch"];
	print("nb blocks : ", blkNB);
	if blkNB != 0 :
		h = len(bStrg["block"]);
		print("===> ", h, "BLOCK this epoch ---------");
		k = 0;
		while k < h :
			blkHASH = bStrg["block"][k]["hash"];
			blkEPOCH_SLOT = bStrg["block"][k]["epoch_slot"];
			blkABS_SLOT = bStrg["block"][k]["slot"];
			blkHEIGHT = bStrg["block"][k]["height"];
			blkPREV_HASH = bStrg["block"][k]["previous_block"];
			blkNEXT_HASH = bStrg["block"][k]["next_block"];
			blkTX_COUNT = bStrg["block"][k]["tx_count"];
			blkVALUE = bStrg["block"][k]["output"];
			blkFEES = bStrg["block"][k]["fees"];
			blkTIME = bStrg["block"][k]["time"];
			b_TIME=datetime.datetime.fromtimestamp(blkTIME);
			blkEPOCH = y;

			sqlBLOCKS = "INSERT IGNORE INTO blocks (epoch_epoch_number, hash, height, absolute_slot, epoch_slot, time, previous_block_hash, next_block_hash, tx_count, fees, value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)";
			valBLOCKS = (blkEPOCH, blkHASH, blkHEIGHT, blkABS_SLOT, blkEPOCH_SLOT, b_TIME, blkPREV_HASH, blkNEXT_HASH, blkTX_COUNT, blkFEES, blkVALUE);
			mycursor.execute(sqlBLOCKS, valBLOCKS);
			mydb.commit();
			k += 1;


############### GET GONE DELEGATORS #####################
def getGoneDelegators():
	with open('data/gone_delegators.json') as json_file:
		gd = json.load(json_file)

	gd_length = len(gd["gone_delegators"]);
	print("GONE DELEGATORS", gd_length);
	g = 0;
	while g < gd_length :
		gd_holder = gd["gone_delegators"][g]["gone"];
		gd_goneEpoch  = gd["gone_delegators"][g]["last_epoch"];
		gd_firstEpoch = gd["gone_delegators"][g]["first_epoch"];
		gd_backCount = gd["gone_delegators"][g]["back_count"];
		gd_sinceEpoch = gd["gone_delegators"][g]["since_epoch"];
		print("HOLDER", gd_holder, "GONE EPOCH", gd_goneEpoch);
		sqlGone="INSERT IGNORE INTO gone_delegators (delegator_stake_address, epoch_epoch_number, first_epoch, since_epoch, back_count) VALUES (%s, %s, %s, %s, %s)";
		valGone=(gd_holder, gd_goneEpoch, gd_firstEpoch, gd_sinceEpoch, gd_backCount);
		mycursor.execute(sqlGone, valGone);
		mydb.commit();
		g += 1;


i = 245
while (i < 479):
	data_H = getFileData(i)
	setDataHistory(data_H);
#	getGoneDelegators();
	i += 1

mycursor.close()
mydb.close()
