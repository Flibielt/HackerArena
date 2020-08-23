from builtins import range
from past.utils import old_div
import MalmoPython
import malmoutils

def commandAgent(agent, observations):
    # Use the line-of-sight observation to determine when to hit and when not to hit:
    if u'LineOfSight' in observations:
      los = observations[u'LineOfSight']
      type=los["type"]
      if type == "Zombie":
        agent.sendCommand("attack 1")
        agent.sendCommand("attack 0")