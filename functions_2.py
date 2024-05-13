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

from config import REGISTRATION_EPOCH, PRUNE_NB
import json

def getHistFile(goneE, currentEpoch):
	backDeleg_goneEpoch = goneE
	DistC = float((currentEpoch - REGISTRATION_EPOCH - 2)/PRUNE_NB)
	DistE = float((currentEpoch - goneE)/PRUNE_NB)
	DistH = DistC - DistE
	sEH = (REGISTRATION_EPOCH + 2) + int(DistH)*PRUNE_NB
	eEH = sEH + (PRUNE_NB - 1)

	if (DistE < 1):
		if (goneE >= sEH and currentEpoch <= eEH):
			file ="data/pool_data.json"
			history = False
			historyIndex = currentEpoch - goneE - 1
		else:
			file = "data/history/pooldata_{}_{}.json".format(sEH, eEH)
			history = True
			historyIndex = eEH - goneE
	else:
		if (goneE > eEH or goneE < sEH):
			sEH = sEH - PRUNE_NB; eEH = eEH - PRUNE_NB

		file = "data/history/pooldata_{}_{}.json".format(sEH, eEH)
		history = True
		historyIndex = eEH - goneE
	print("Gone :",goneE, "Back :",currentEpoch)
	result = history, file, historyIndex
#	print(result)
	return result
#test(249,254)
#test(249,255)
