Simulation TB
Description: Simulates the TB epidemic in South Africa

State Alive
Description: Indicates if person is alive or dead
Initial-values: 1

State Age
Description: Age of a person
Initial-values: 0 probability 0.1, 1 probability 0.1, 0.2

Transition
Probability: 1
Increment: 1 per 365.25 linear
Condition: Alive == 1

State Alive


tb = Simulation("tb")
tb.description = "Simulates the TB epidemic in South Africa"
tb.iterations = 70
tb.population = 1000
tb.timePeriod = 365.25
alive = State(simulation=tb, name="alive")
alive.description = "Indicates if person is alive or dead"
alive.addInitialValue(value = 1)
age = State(simulation=tb, name="age")
age.addInitialValue(value = 0, probability = 0.01)
age.addInitialValue(value = 1, probability = 0.01)
age.addInitialValue(value = 2, probability = 0.01)
t = age.addTransition(value=1, assignment=INCREMENT, period=365.25, normalize=LINEAR, 
                      probability=1, probability_normalize=NONE)
t.addCondition(alive, EQ, 1.0)

