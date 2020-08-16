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
      <DrawingDecorator>
        <DrawEntity x="-1.5" y="227.0" z="5" type="Zombie"/>
      </DrawingDecorator>
      <ServerQuitFromTimeUp description="" timeLimitMs="20000"/>
      <ServerQuitWhenAnyAgentFinishes description=""/>
    </ServerHandlers>
  </ServerSection>

  <AgentSection mode="Survival">
    <Name>Hunter</Name>
    <AgentStart>
      <Placement x="-1.5" y="227.0" z="0.5" pitch="30" yaw="0"/>
      <Inventory>
        <InventoryItem slot="0" type="iron_sword"/>
        <InventoryItem slot="1" type="iron_axe"/>
        <InventoryItem slot="2" type="bow"/>
        
        <InventoryItem slot="7" type="arrow" quantity="64"/>
        <InventoryItem slot="8" type="arrow" quantity="64"/>
        
        <InventoryItem slot="36" type="iron_boots"/>
        <InventoryItem slot="37" type="iron_leggings"/>
        <InventoryItem slot="38" type="iron_chestplate"/>
        <InventoryItem slot="39" type="iron_helmet"/>
      </Inventory>
    </AgentStart>
    <AgentHandlers>
      <ObservationFromFullStats/>
      <ObservationFromGrid>
        <Grid name="foot3x3">
          <min x="-1" y="0" z="-1"/>
          <max x="1" y="2" z="1"/>
        </Grid>
      </ObservationFromGrid>
      <ObservationFromNearbyEntities>
        <Range name="close_entities" xrange="5" yrange="5" zrange="2" />
      </ObservationFromNearbyEntities>
      <ObservationFromFullInventory flat="false"/>
      <InventoryCommands/>
      <ContinuousMovementCommands turnSpeedDegs="180"/>
    </AgentHandlers>
  </AgentSection>

</Mission>'''
my_mission = MalmoPython.MissionSpec(xml,True)
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
    print(closeEntities)
    print()
