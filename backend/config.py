'''global values'''
NANOSECONDS = 1
MICROSECONDS = 1000 * NANOSECONDS
MILLISECONDS = 1000 * MICROSECONDS
SECONDS = 1000 * MILLISECONDS

MINE_RATE = 4 * SECONDS  # just a rate that set arbitrary
'''like 4 BILLLISECOND'''

STARTING_BALANCE = 1000

MINING_REWARD = 50
MINING_REWARD_INPUT = { 'address': '*-- official-mining-reward --*' } # --*: just to make the address unique