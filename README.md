# Price-of-MEV
Compute the estimated price of MEV in a time frame.

The price of MEV is formally defined in [Price of MEV](https://arxiv.org/abs/2208.13464), as the ratio between the gas cost induced by competing players extracting an MEV opportunity (in equilibrium) and the optimal extraction. In reality, is unknown if players converged to some notion of equilibrium howeover, we can estimated the Price of MEV by assuming so. In this repository, we compute the price of MEV of a subset of players in a given time frame.

