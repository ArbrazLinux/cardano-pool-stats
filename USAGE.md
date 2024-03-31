# how to use

once initializiation process is done, simply run file ./new_epoch.sh at the beginning of each epoch

within a epoch, you can update data running ./update.sh


# AWARDS
in the case you distribute rewards and giveaway some assets you can edit data/awards.json file with it

it will be integrated into database

example :
in epoch 475 you distribute 30 &#8371; to a delegator, edit data/awards.json as following:

{"awards": {"epoch": 475, "awarded_delegators": [{"address": "stake_address_to_award", "amount": 30000000}]}}


in epoch 475 you giveaway 25 HOSK to a delegator, edit data/awards.json as following :

{"awards": {"epoch": 475, "awarded_delegators": [{"address": "stake_address_to_award", "amount": 1211111, "assets": ["name": "HOSK", "amount": 25, "policyID": "", "name_hash": "", "": ""}]}]}}
