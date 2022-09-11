import requests
from collections import defaultdict

def get_transactions(action, 
                    address, 
                    start_block, 
                    end_block,
                    api_key="VY8NCHRVIG3E8RD37Q293183QSTF39Y3ET"):
    """
    Get action transactions of an address between [start_block, end_block].
    Args:
      action = String. Possible values are txlist, txlistinternal and tokentx.
      address = String address hash.
      start_block = Integer start block.
      end_block = Integer end block.
    Returns:
      Dict with error and data keys.
    """
    if action not in ["txlist", "txlistinternal", "tokentx"]:
        print("Action does not match any of the the following action list: txlist, txlistinternal, tokentx")
        return {"error": 1, "data": list()}

    api_url_payload = {'module': 'account', 'action': action, 'address': address, 'startblock': start_block,
                       'endblock': end_block, 'sort': 'desc', 'apikey': api_key}
    api_url = 'https://api.etherscan.com/api'

    txs_json = []

    try:
        r = requests.get(api_url, params=api_url_payload)
        txs_json = r.json()["result"]
        error_json = r.json()["status"]
        assert error_json == "1"
        # df = pd.DataFrame(txs_json)
        res = {"error": 0, "data": txs_json}

    except AssertionError:
        print(txs_json)
        res = {"error": 1, "data": list()}

    except:
        print("Something happened when requesting data.")
        res = {"error": 1, "data": list()}

    return res
def get_huge_transactions(action, address, target_block, present_block):
    """
    Execute several times get_transactions to get all transactions between target_block and present_block
    """
    var_block = present_block
    aux_block = 0
    total_action_trans_dict = {}
    action_trans = [0]
    while (target_block != var_block) and (action_trans) and var_block!= aux_block:
        #print(action_trans)
        aux_block = var_block
        action_trans = get_transactions(action, address, target_block, var_block)["data"]
        action_trans_byhash = {trans["hash"]: trans for trans in action_trans}
        total_action_trans_dict.update(action_trans_byhash)
            
        var_block = int(action_trans[-1]["blockNumber"])
    total_action_trans = sorted(total_action_trans_dict.values(), key=(lambda x: int(x["blockNumber"])), reverse=True)

    return total_action_trans



def compute_gas_used(bot_address,from_block,to_block,interval = 4):
    result = get_huge_transactions("txlist",bot_address,from_block,to_block)
    result_ordered = sorted(result, key=(lambda x: int(x["blockNumber"])), reverse=False)
    data = [tx['input'] for tx in result]
    tx_hash = [tx['hash'] for tx in result]
    
    results_erc = get_huge_transactions("tokentx",bot_address,from_block,to_block)
    tx_hash_erc = list(set([tx['hash'] for tx in results_erc]))
    
    executed_transactions = [trans['hash'] for trans in result_ordered if trans['hash'] in tx_hash_erc]
    
    executed_gas_used   = 0
    cumulative_gas_used = 0
    egu,cgu,pmev,blocks = [],[],[],[]
    blockNumber = result_ordered[0]['blockNumber']
    pmev_dict2 = dict() 
    pmev_dict = defaultdict(lambda : defaultdict(int))
    block_list = [from_block+i for i in range(0,to_block-from_block+1,interval)]
    block_list2 = []
    for block in block_list:
        pmev_dict[block] = {"gas_used":0,
                            "executed_gas_used":0,
                            "executed_acumulated_gas_used":0,
                            "total_acumated_gas_used":0,
                           }
    for trans in result_ordered:
        good_gas_used = 0
        if trans['hash'] in tx_hash_erc:
            executed_gas_used += int(trans['gasUsed'])
            good_gas_used = int(trans['gasUsed'])
            #print(int(trans['blockNumber']),good_gas_used)
        cumulative_gas_used += int(trans['gasUsed'])
        gas_used = int(trans['gasUsed'])
        try:
            blockNumber = min([block for block in block_list if block>=int(trans['blockNumber'])])
            pmev_dict[blockNumber] = {"gas_used":gas_used+pmev_dict[blockNumber]["gas_used"],
                                      "executed_gas_used":good_gas_used+pmev_dict[blockNumber]["executed_gas_used"],
                                      "executed_acumulated_gas_used":executed_gas_used,
                                      "total_acumated_gas_used":cumulative_gas_used,
                                      }
            pmev_dict2[blockNumber] = pmev_dict[blockNumber]
            block_list2.append(blockNumber)
        except:
            print(trans["blockNumber"])

    for block in pmev_dict:
        try:
            block2 = min([_block for _block in block_list2 if _block>=block])
            pmev_dict[block] = pmev_dict[block2]
        except:
            pass
    return pmev_dict2


def compute_price_mev(bots_list,from_block,to_block,interval=4):
    executed_acumulated_gas_used, executed_acumulated_gas_used = 0,0
    for bot in bots_list:
        bot_dict[bot] = compute_gas_used(bot,from_block,to_block,interval)
    block_list = list(bot_dict[bot].keys())
    for block in block_list:
        executed_gas_used=0
        gas_used=0
        for bot in bots_list:
            executed_gas_used += bot_dict[bot]["executed_gas_used"]
            gas_used += bot_dict[bot]["gas_used"]
            executed_acumulated_gas_used += bot_dict[bot]["executed_acumulated_gas_used"]
            total_acumated_gas_used += bot_dict[bot]["total_acumated_gas_used"]
        if executed_gas_used==0:
            executed_gas_used = 10**5
        pmev[block] = gas_used / executed_gas_used
        acumulated_executed[block] = executed_acumulated_gas_used
        acumulated_total[block] = total_acumated_gas_used
    return pmev, acumulated_executed, acumulated_total