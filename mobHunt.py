from __future__ import print_function
from __future__ import division

from builtins import range
from past.utils import old_div
import MalmoPython
import os
import random
import sys
import time
import json
import random
import errno
import math
import malmoutils

from agentCommands import commandAgent

malmoutils.fix_print()

agent_host = MalmoPython.AgentHost()
malmoutils.parse_command_line(agent_host)

# -- set up the mission -- #
mission_file = './mobHunt.xml'
with open(mission_file, 'r') as f:
    print("Loading mission from %s" % mission_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
  try:
    agent_host.startMission( my_mission, my_mission_record )
    break
  except RuntimeError as e:
    if retry == max_retries - 1:
      print("Error starting mission:",e)
      exit(1)
    else:
      time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission running ", end=' ')

while world_state.is_mission_running:
  world_state = agent_host.getWorldState()
  if world_state.number_of_observations_since_last_state > 0:
    msg = world_state.observations[-1].text
    observations = json.loads(msg)
    grid = observations.get(u'foot3x3', 0)
    closeEntities = observations.get(u'close_entities')
    print(observations)
    print()

    # The agent commands are in a separate file, so it can be reused in different missions
    commandAgent(agent_host, observations)