# Price-of-MEV
Compute the estimated price of MEV in a time frame.

The price of MEV is formally defined in [Price of MEV](https://arxiv.org/abs/2208.13464), as the ratio between the gas cost induced by competing players extracting an MEV opportunity (in equilibrium) and the optimal extraction. In reality, is unknown if players converged to some notion of equilibrium howeover, we can estimated the Price of MEV by assuming so. In this repository, we compute the price of MEV of a subset of players in a given time frame.

In the report, we formally defined the front-running PGA, Back-running PGA (Random ordering game), Flashbots game, meta-data game and a Latency game. Obtaning lower bounds of the the price of MEV for each game.

## Pre pull request

## Post pull request / Pre Flashbots auction

## Post Flashbots auction


## Improve the computation of Price of MEV using mev-inspect-py

In the future we will implement the computation the price of MEV in the MEV-inspect-py. The changes need it are the following.
Take the set of all searchers known (using mev-inspect-py or other tools). Take an inteval of blocks and execute all the MEV opportunities. For each MEV opportunity, fork and execute the transaction that leave an MEV opportunity, then test all transactions send by other players and compute the difference of balance. In this way we would check that both transactions were conflicting, therefore extracting the same MEV opportunity. Add the gas costs of all this transactions and divided by the transaction that extacted to estimate the Price of MEV (or divided by the most efficient one using the simulations). 

![](https://i.imgur.com/le72Cfy.png)
