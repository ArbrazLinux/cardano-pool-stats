# how to use

when initializiation process is done, simply run file './newEpoch.sh' at the beginning of each epoch (once in an epoch)

within a epoch, you can distribute awards and then update data running './processBonus.sh'

you can setup cron tasks to automate :
+ newEpoch.sh ==> at the beginning of a new epoch
+ processBonus.sh ==> whenever within an epoch when you distribute awards (once a time)
+ processRewards.sh ==> less than 36 hours before the end of epoch


# AWARDS
in the case you distribute awards and assets you can edit 'data/awards.json' file with it

it will be integrated into database

example 1 :
in epoch 475 you distribute 30 &#8371; to a delegator, edit 'data/awards.json' as following:

[{"epoch": 475, "awards": [{"address": "stake_address_to_award", "amount": 30000000}], "assets": []}]

notabene : amount is in LOVELACE | address to award is the STAKE ADRRESS

example 2 :
in epoch 475 you giveaway 25 HOSK to a delegator, edit 'data/awards.json' as following :

[{"epoch": 475, "awards": [{"address": "stake_address_to_award", "amount": 1211111, "assets": [{"name": "HOSK", "amount": 25, "policyID": "98dc68b04026544619a251bc01aad2075d28433524ac36cbc75599a1", "name_hash": "686f736b", "fingerprint": "asset1tvh6cs0q40l6nlgf8a52les0jg94gzfuvl2e7q"}]}]}]
