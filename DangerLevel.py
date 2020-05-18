import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# changes from last version: DL 'none' removed, time 'low' narrowed from 5 to 3,
# other "time" categories adjusted, speed 'none' removed,
# new rule bases for the new inputs, removed excessive rule bases and functions

# time "outright absurd" kept for future reasons, as system might need it later

# changed time range from 0-25 to 0-10

# antecedent = input, consequent = output
# not really, but just to simplify
speed = ctrl.Antecedent(np.arange(0, 11, 1), 'speed')
time = ctrl.Antecedent(np.arange(0, 11, 1), 'time')
dangerLevel = ctrl.Consequent(np.arange(0, 9, 1), 'danger')

time['Low'] = fuzz.trapmf(time.universe, [0, 0, 1, 2])
time['Medium'] = fuzz.trimf(time.universe, [1, 2, 3])
time['High'] = fuzz.trapmf(time.universe, [2, 3, 4, 5])
time['Very High'] = fuzz.trapmf(time.universe, [4, 5, 7, 8])
time['Outright Absurd'] = fuzz.trapmf(time.universe, [7, 8, 10, 10])

speed['Low'] = fuzz.trimf(speed.universe, [0, 2, 4])
speed['Medium'] = fuzz.trimf(speed.universe, [2, 4, 6])
speed['High'] = fuzz.trimf(speed.universe, [4, 6, 8])
speed['Too Damn Fast'] = fuzz.trapmf(speed.universe, [6, 8, 10, 10])

dangerLevel['Low'] = fuzz.trimf(dangerLevel.universe, [0, 2, 3.5])
dangerLevel['Medium'] = fuzz.trimf(dangerLevel.universe, [2.5, 4, 5.5])
dangerLevel['High'] = fuzz.trimf(dangerLevel.universe, [4.5, 6, 7.5])
dangerLevel['Dear Fucking God'] = fuzz.trimf(dangerLevel.universe, [6.5, 8, 8])

# use to see membership functions
# faceSituation.view()
# time.view()
# speed.view()
# dangerLevel.view()

# base rules, no danger if vehicle not moving,and no danger if driver in normal situation
# these did not make it into the final version, due to "rule" rules
# rule1 = ctrl.Rule(speed['None'], dangerLevel['None'])
# rule3 = ctrl.Rule(time['Outright Absurd'], dangerLevel['Dear Fucking God'])


# rules for the situation "distracted", there will be one of these for each possible state
distractedRule1 = ctrl.Rule(time['Low'] & speed['Low'], dangerLevel['Low'])
distractedRule2 = ctrl.Rule(time['Low'] & speed['Medium'], dangerLevel['Low'])
distractedRule3 = ctrl.Rule(time['Low'] & speed['High'], dangerLevel['Low'])
distractedRule4 = ctrl.Rule(time['Low'] & speed['Too Damn Fast'], dangerLevel['Low'])
distractedRule5 = ctrl.Rule(time['Medium'] & speed['Low'], dangerLevel['Low'])
distractedRule6 = ctrl.Rule(time['Medium'] & speed['Medium'], dangerLevel['Medium'])
distractedRule7 = ctrl.Rule(time['Medium'] & speed['High'], dangerLevel['Medium'])
distractedRule8 = ctrl.Rule(time['Medium'] & speed['Too Damn Fast'], dangerLevel['Medium'])
distractedRule9 = ctrl.Rule(time['High'] & speed['Low'], dangerLevel['Medium'])
distractedRule10 = ctrl.Rule(time['High'] & speed['Medium'], dangerLevel['High'])
distractedRule11 = ctrl.Rule(time['High'] & speed['High'], dangerLevel['High'])
distractedRule12 = ctrl.Rule(time['High'] & speed['Too Damn Fast'], dangerLevel['High'])
distractedRule13 = ctrl.Rule(time['Very High'] & speed['Low'], dangerLevel['High'])
distractedRule14 = ctrl.Rule(time['Very High'] & speed['Medium'], dangerLevel['High'])
distractedRule15 = ctrl.Rule(time['Very High'] & speed['High'], dangerLevel['Dear Fucking God'])
distractedRule16 = ctrl.Rule(time['Very High'] & speed['Too Damn Fast'], dangerLevel['Dear Fucking God'])
distractedRule17 = ctrl.Rule(time['Outright Absurd'] & speed['Low'], dangerLevel['Dear Fucking God'])
distractedRule18 = ctrl.Rule(time['Outright Absurd'] & speed['Medium'], dangerLevel['Dear Fucking God'])
distractedRule19 = ctrl.Rule(time['Outright Absurd'] & speed['High'], dangerLevel['Dear Fucking God'])
distractedRule20 = ctrl.Rule(time['Outright Absurd'] & speed['Too Damn Fast'], dangerLevel['Dear Fucking God'])

# rules for the situation "tired", there will be one of these for each possible state
tiredRule1 = ctrl.Rule(time['Low'] & speed['Low'], dangerLevel['Low'])
tiredRule2 = ctrl.Rule(time['Low'] & speed['Medium'], dangerLevel['Low'])
tiredRule3 = ctrl.Rule(time['Low'] & speed['High'], dangerLevel['Low'])
tiredRule4 = ctrl.Rule(time['Low'] & speed['Too Damn Fast'], dangerLevel['Low'])
tiredRule5 = ctrl.Rule(time['Medium'] & speed['Low'], dangerLevel['Low'])
tiredRule6 = ctrl.Rule(time['Medium'] & speed['Medium'], dangerLevel['Low'])
tiredRule7 = ctrl.Rule(time['Medium'] & speed['High'], dangerLevel['Low'])
tiredRule8 = ctrl.Rule(time['Medium'] & speed['Too Damn Fast'], dangerLevel['Low'])
tiredRule9 = ctrl.Rule(time['High'] & speed['Low'], dangerLevel['Low'])
tiredRule10 = ctrl.Rule(time['High'] & speed['Medium'], dangerLevel['Low'])
tiredRule11 = ctrl.Rule(time['High'] & speed['High'], dangerLevel['Medium'])
tiredRule12 = ctrl.Rule(time['High'] & speed['Too Damn Fast'], dangerLevel['Medium'])
tiredRule13 = ctrl.Rule(time['Very High'] & speed['Low'], dangerLevel['Medium'])
tiredRule14 = ctrl.Rule(time['Very High'] & speed['Medium'], dangerLevel['High'])
tiredRule15 = ctrl.Rule(time['Very High'] & speed['High'], dangerLevel['High'])
tiredRule16 = ctrl.Rule(time['Very High'] & speed['Too Damn Fast'], dangerLevel['Dear Fucking God'])
tiredRule17 = ctrl.Rule(time['Outright Absurd'] & speed['Low'], dangerLevel['High'])
tiredRule18 = ctrl.Rule(time['Outright Absurd'] & speed['Medium'], dangerLevel['Dear Fucking God'])
tiredRule19 = ctrl.Rule(time['Outright Absurd'] & speed['High'], dangerLevel['Dear Fucking God'])
tiredRule20 = ctrl.Rule(time['Outright Absurd'] & speed['Too Damn Fast'], dangerLevel['Dear Fucking God'])

# use this to view any rule
# r.view()

# superRuleBase = ctrl.ControlSystem([ distractedRule1, distractedRule2, distractedRule3, distractedRule4,
# distractedRule5, distractedRule6, distractedRule7, distractedRule8, distractedRule9, distractedRule10,
# distractedRule11, distractedRule12, distractedRule13, distractedRule14, distractedRule15, distractedRule16,
# distractedRule17, distractedRule18, distractedRule19, distractedRule20, tiredRule1, tiredRule2, tiredRule3,
# tiredRule4, tiredRule5, tiredRule6, tiredRule7, tiredRule8, tiredRule9, tiredRule10, tiredRule11, tiredRule12,
# tiredRule13, tiredRule14, tiredRule15, tiredRule16, tiredRule17, tiredRule18, tiredRule19, tiredRule20, sleepRule1,
# sleepRule2, sleepRule3, sleepRule4, sleepRule5, sleepRule6, sleepRule7, sleepRule8, sleepRule9, sleepRule10,
# sleepRule11, sleepRule12, sleepRule13, sleepRule14, sleepRule15, sleepRule16, sleepRule17, sleepRule18,
# sleepRule19, sleepRule20, tiredRule1, tiredRule2, tiredRule3, tiredRule4, tiredRule5, tiredRule6, tiredRule7,
# tiredRule8, tiredRule9, tiredRule10, tiredRule11, tiredRule12, tiredRule13, tiredRule14, tiredRule15, tiredRule16,
# tiredRule17, tiredRule18, tiredRule19, tiredRule20, yawningRule1, yawningRule2, yawningRule3, yawningRule4,
# yawningRule5, yawningRule6, yawningRule7, yawningRule8, yawningRule9, yawningRule10, yawningRule11, yawningRule12,
# yawningRule13, yawningRule14, yawningRule15, yawningRule16, yawningRule17, yawningRule18, yawningRule19,
# yawningRule20])

distractedRuleBase = ctrl.ControlSystem(
    [distractedRule1, distractedRule2, distractedRule3, distractedRule4, distractedRule5, distractedRule6,
     distractedRule7, distractedRule8, distractedRule9, distractedRule10, distractedRule11, distractedRule12,
     distractedRule13, distractedRule14, distractedRule15, distractedRule16, distractedRule17, distractedRule18,
     distractedRule19, distractedRule20])
tiredRuleBase = ctrl.ControlSystem(
    [tiredRule1, tiredRule2, tiredRule3, tiredRule4, tiredRule5, tiredRule6, tiredRule7, tiredRule8, tiredRule9,
     tiredRule10, tiredRule11, tiredRule12, tiredRule13, tiredRule14, tiredRule15, tiredRule16, tiredRule17,
     tiredRule18, tiredRule19, tiredRule20])

# ok, so there is an issue with such a massive rule base
# now with as many rules as there is in the SUPER RULE BASE
# there quickly becomes a problem, as the end result always
# ends with a result around 5.25, which is in the crossower
# area between "Medium" and "High" in dangerLevel.
# So the Rule Base had to be split up, and be placed in different
# Rule Bases, which have to run on different systems.
# C'est la vie, I guess. I'll leave the SRB and the simulator
# using it behind as comments...

distracted = ctrl.ControlSystemSimulation(distractedRuleBase)
tired = ctrl.ControlSystemSimulation(tiredRuleBase)


def Get_Danger_Level_distracted(time, speed):
    distracted.input['time'] = time
    distracted.input['speed'] = speed

    distracted.compute()

    #     print (danger.output['danger'])
    #     dangerLevel.view(sim=danger)
    return distracted.output['danger']


def Get_Danger_Level_tired(time, speed):
    tired.input['time'] = time
    tired.input['speed'] = speed

    tired.compute()

    #     print (danger.output['danger'])
    #     dangerLevel.view(sim=danger)
    return tired.output['danger']


# this is the one function this was made for
def Chief_Danger_Acquisition_Officer(situation, time, speed):
    #     
    if speed == 0 or situation == 0:
        return 0

    #     
    elif situation == 1:
        return Get_Danger_Level_distracted(time, speed)

    #
    elif situation == 2:
        return Get_Danger_Level_tired(time, speed)

    else:
        print("Invalid situation")
        return 422
