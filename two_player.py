from __future__ import print_function

from builtins import range
import MalmoPython
import json
import logging
import math
import os
import random
import sys
import time
import malmoutils
from safeCommands import safeStartMission
from safeCommands import safeWaitForStart

malmoutils.fix_print()

# -- set up two agent hosts --
agent_host1 = MalmoPython.AgentHost()
agent_host2 = MalmoPython.AgentHost()

# Use agent_host1 for parsing the command-line options.
# (This is why agent_host1 is passed in to all the subsequent malmoutils calls, even for
# agent 2's setup.)
malmoutils.parse_command_line(agent_host1)

# -- set up the mission --
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
        <RewardForCollectingItem>
            <Item reward="1" type="dirt"/>
        </RewardForCollectingItem>
        <RewardForDiscardingItem>
            <Item reward="10" type="dirt"/>
        </RewardForDiscardingItem>''' + malmoutils.get_video_xml(agent_host1) + '''
    </AgentHandlers>
  </AgentSection>

  <AgentSection mode="Survival">
    <Name>Player2</Name>
    <AgentStart>
      <Placement x="1.5" y="227.0" z="6.5" pitch="30" yaw="180"/>
    </AgentStart>
    <AgentHandlers>
        <ContinuousMovementCommands turnSpeedDegs="180"/>
        <RewardForCollectingItem>
            <Item reward="10" type="dirt"/>
        </RewardForCollectingItem>
        <RewardForDiscardingItem>
            <Item reward="100" type="dirt"/>
      </RewardForDiscardingItem>''' + malmoutils.get_video_xml(agent_host1) + '''
    </AgentHandlers>
  </AgentSection>
  
</Mission>'''
my_mission = MalmoPython.MissionSpec(xml,True)

client_pool = MalmoPython.ClientPool()
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )

MalmoPython.setLogging("", MalmoPython.LoggingSeverityLevel.LOG_OFF)

safeStartMission(agent_host1, my_mission, client_pool, malmoutils.get_default_recording_object(agent_host1, "agent_1_viewpoint_discrete"), 0, '' )
safeStartMission(agent_host2, my_mission, client_pool, malmoutils.get_default_recording_object(agent_host1, "agent_2_viewpoint_discrete"), 1, '' )
safeWaitForStart([agent_host1, agent_host2])

def player1_commands():
    agent_host1.sendCommand("move 1")
    time.sleep(3)

def player2_commands():
    agent_host2.sendCommand("move 1")

# wait for the missions to end    
while agent_host1.peekWorldState().is_mission_running or agent_host2.peekWorldState().is_mission_running:
    time.sleep(1)
    player1_commands()
    player2_commands()
