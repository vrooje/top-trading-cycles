from serialdictatorship import serialDictatorship
from toptradingcycles import getAgents, anyCycle, topTradingCycles
from graph import Graph, Vertex

import sys,os
import csv

# assume a default test file name if one is not entered at the prompt
# format of file is one agent (student) per row, with their name/ID in the
# second column and their ranked preferences in additional comma-separated columns
# e.g.
# blah,Zach,Amy,Brenda,Carol
# where Zach wants to work most with Amy and least with Carol
#
# (this is consistent with the exports from a Google form, where the first column
#  is a timestamp, which we will ignore)
#
# Also, the second input is just a list of objects (potential supervisors),
# one per line as a text file
try:
    agent_pref_csv = sys.argv[1]
    objects_csv    = sys.argv[2]
except:
    agent_pref_csv = 'test_data.csv'
    objects_csv    = 'test_supervisors.txt'
    print("Using %s as input preferences from students and %s as a list of potential supervisors." % (agent_pref_csv, objects_csv))
    print("Note: you can specify different files at the prompt.")

agents = []
prefs = []
agentPreferences = {}
with open(agent_pref_csv, 'r') as f:
    reader = csv.reader(f)
    for i_row, row in enumerate(reader):
        if i_row == 0:
            # for now we're ignoring this, just note it
            header = row
        else:
            # split out the name of the agent from their preferences
            the_agent = row[1]
            the_pref  = row[2:]
            agents.append(the_agent)
            prefs.append(the_pref)
            agentPreferences[the_agent] = the_pref

    # end looping through the csv lines
# end reading the input file

# now read the list of potential supervisors
with open(objects_csv) as f:
    objects = f.read().splitlines()

# try an initial allocation using the simple method
allocation = serialDictatorship(prefs, objects)

# the allocation is a dictionary where the agent is the index and their assignment
# is the entry. for the TTC code, you need a dictionary where those are reversed.
# obviously

# let's talk about how appropriate the house ownership language is here for
# the relationship between supervisors and PhD students
initialOwnership = {}

# also print out which agents (students) got assigned to which objects (supervisors)
print("Serial Dictatorship Allocations:\n_____________________________________")
for i, the_agent in enumerate(agents):
    print("%s: %s" % (agents[i], allocation[i]))
    initialOwnership[allocation[i]] = agents[i]


new_allocations = topTradingCycles(agents, objects, agentPreferences, initialOwnership)
print("\n\n\nHouse Ownership Allocations:\n_____________________________________")
for the_agent in new_allocations:
    print("%s: %s" % (the_agent, new_allocations[the_agent]))

#
