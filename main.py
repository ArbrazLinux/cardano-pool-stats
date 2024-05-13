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

from initEpoch import initEpoch
from setPoolData import setData
from config import REGISTRATION_EPOCH

def init(currentEpoch):
	i=REGISTRATION_EPOCH + 2
	while (i <= currentEpoch):
		initEpoch(i)
		setData(i)
		print("Epoch", i, "DONE =============")
		i+=1

def newEpoch(epoch):
	initEpoch(epoch)
	setData(epoch)
	print("Epoch", epoch, "DONE =============")

