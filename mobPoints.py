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

malmoutils.fix_print()

agent_host = MalmoPython.AgentHost()
malmoutils.parse_command_line(agent_host)

xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <About>
    <Summary/>
  </About>
  <ServerSection>
    <ServerInitialConditions>
      <Time>
        <StartTime>0</StartTime>
      </Time>
    </ServerInitialConditions>
    <ServerHandlers>
      <FlatWorldGenerator forceReset="true" generatorString="3;7,220*1,5*3,2;3;,biome_1" seed=""/>
      <ServerQuitFromTimeUp description="" timeLimitMs="20000"/>
      <ServerQuitWhenAnyAgentFinishes description=""/>
    </ServerHandlers>
  </ServerSection>

  <AgentSection mode="Survival">
    <Name>Player1</Name>
    <AgentStart>
      <Placement x="-1.5" y="227.0" z="0.5" pitch="30" yaw="0"/>
    </AgentStart>
    <AgentHandlers>
        <ContinuousMovementCommands turnSpeedDegs="180"/>
    </AgentHandlers>
  </AgentSection>

</Mission>'''
my_mission = MalmoPython.MissionSpec(xml,True)

world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    time.sleep(0.1)
    world_state = agent_host.getWorldState()

while world_state.is_mission_running:
    world_state = agent_host.getWorldState()
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        ob = json.loads(msg)