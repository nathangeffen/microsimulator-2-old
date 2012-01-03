//============================================================================
// Name        : microsimulator.cpp
// Author      : Nathan Geffen
// Version     :
// Copyright   : Copyright Nathan Geffen, 2011
// Description : Microsimulator of epidemics
//============================================================================

#include <vector>
#include <iostream>
#include <algorithm>
#include <QByteArray>
#include <QString>
#include <QVariant>
#include <QDebug>
#include <QFile>
#include <qjson/parser.h>

#include "simutils.h"
#include "basesimulation.h"
#include "state.h"
#include "statetransitiontable.h"

using namespace microsimulator;

const double DEFAULT_TRANSITION_PROBABILITY = 0.009;
const double DEFAULT_TRANSITION_BACK_PROBABILITY = 0.7;

BaseSimulation::BaseSimulation(QString name,
                               int nIndividuals,
                               int nIterations,
                               double timePeriod)
{
  this->stateCounter_ = 0;
  this->setName( name );
  this->setPopulation( nIndividuals );
  this->setTimePeriod( timePeriod );
}


BaseSimulation::~BaseSimulation()
{
  for (auto index : statesToDelete_) {
    delete states_[index];
  }
}




void BaseSimulation::loadStates(const QByteArray& inputTable,
                                const SimulationFormat& tableFormat)
{
  switch( tableFormat ) {
    case JSONTEXT:
      this->loadStatesFromJsonTable(inputTable);
      break;
    case SQLITE:
      throw SimulationException("SQLITE state transition table"
                                "not implemented yet", __LINE__, __FILE__);
      break;
    default:
      throw SimulationException("Unknown state transition table format",
                                __LINE__, __FILE__);
      break;
  }
}

void BaseSimulation::loadStates(QFile& inputFile,
                                const SimulationFormat& tableFormat)
{

  if ( !inputFile.open(QIODevice::ReadOnly | QIODevice::Text) ) {
    throw SimulationException( "Could not open file " + inputFile.fileName() );
  }
  QByteArray inputTable = inputFile.readAll();
  this->loadStates(inputTable, tableFormat);
}

void BaseSimulation::loadStatesFromJsonTable(const QByteArray& inputTable)
{
  // Parse example data

  QJson::Parser parser;
  bool ok;

  QVariantList modelArray = parser.parse (inputTable, &ok).toList();

  // Did it go wrong?
  if ( !ok )
  {
    throw SimulationException("JSON transition table did not parse",
                              __LINE__, __FILE__);
  }

  for ( auto model : modelArray ) {
    QMap < QString, QVariant > fields = model.toMap();

    QString model = fields [ "model" ].toString();
    if ( model == "specification.state" ) {
      this->loadJsonState(fields);
    } else if ( model == "specification.specifiedinitialvalue" ) {
      this->loadJsonInitialValue(fields);
    } else if ( model == "specification.transitionrecord" ) {
      this->loadJsonTransitionRecord(fields);
    } else if ( model == "specification.entry" ) {
      this->loadJsonEntry(fields);
    } else if ( model == "specification.simulation" ) {
      // Do nothing
    } else if ( model == "" ){
      throw SimulationException("Missing model name in Json file",
                                      __LINE__, __FILE__);
    } else {
      throw SimulationException("Unknown model name " + model +
                                " in Json file", __LINE__, __FILE__);
    }
  }
}

void BaseSimulation::loadJsonState(const QMap< QString, QVariant >& fields)
{
  int pk = fields[ "pk" ].toInt();
  int stateIndex = addState(fields [ "fields" ].toMap()[ "name" ].toString(),
                            new StateTransitionTable(),
                            true);
  pkToState_[pk] = stateIndex;
}

void BaseSimulation::loadJsonInitialValue(const QMap< QString, QVariant >& fields)
{
  QMap<QString, QVariant> subfields = fields[ "fields" ].toMap();
  int statePk = subfields[ "state" ].toInt();
  StateTransitionTable* state = static_cast< StateTransitionTable* >
                                  ( states_[ pkToState_[ statePk ] ] );
  state->addInitialValue(subfields);
}

void BaseSimulation::loadJsonTransitionRecord(
                                  const QMap< QString, QVariant>& fields)
{
  int pk = fields[ "pk" ].toInt();
  QMap<QString, QVariant> subfields = fields[ "fields" ].toMap();
  int statePk = subfields[ "state" ].toInt();
  StateTransitionTable* state = static_cast< StateTransitionTable* >
                                  ( states_[ pkToState_[ statePk ] ] );
  state->addTransitionRecord(pk, subfields);
  transitionPktoState_[pk] = pkToState_[ statePk ];
}

void BaseSimulation::loadJsonEntry(const QMap< QString, QVariant>& fields)
{

  QMap<QString, QVariant> subfields = fields[ "fields" ].toMap();

  int transitionPk = subfields[ "transition_record" ].toInt();
  int stateIndex = transitionPktoState_[transitionPk];

  StateTransitionTable* state = static_cast< StateTransitionTable* >
                                  ( states_[ stateIndex ] );

  int statePk = subfields[ "state" ].toInt();
  int entryStateIndex = pkToState_[ statePk ];

  state->addEntryToTransitionRecord(transitionPk, entryStateIndex, subfields);
}


void BaseSimulation::prepare()
{

  // Prepare states
  for ( auto itState : states_ ) {
    itState->prepare(timePeriod_);
  }


  // Initialize individuals
  for ( int i=0; i<nIndividuals_; ++i ) {
    Individual individual;
    for ( auto state : states_ ) {
      individual.initializeStateValue(state->initialize());
    }
    individuals_.push_back(individual);
  }
};

void BaseSimulation::simulate() {
  for (int i=0; i<nIterations_; ++i) {
    for (auto& individual : individuals_) {
      for (int j=0; j < stateCounter_; ++j) {
        if (passesFilters(*individual.getStateValues(),
                          *states_[j]->getFilterFunctions())) {
          double stateValue = individual.getStateValue(j);
          stateValue = states_[j]->transition(stateValue,
                                              states_,
                                              individuals_,
                                              individual);
          individual.setStateValue(j, stateValue);
        }
      }
    }
  }
};

AnalysisOutput BaseSimulation::analyze()
{
  AnalysisOutput output;
  OutputDescriptor o;

  for (auto descriptor : analysisDescriptors_) {

    // Get state name and filter out unneeded individuals
    QString outputDescription = get<0>(descriptor);
    int stateIndex = get<1>(descriptor);
    vector<On> filters = get<3>(descriptor);

    IndividualVector filteredIndividuals(individuals_.size());
    auto itend = remove_copy_if(
                   individuals_.begin(), individuals_.end(),
                   filteredIndividuals.begin(),
                   [filters](Individual& i){
      return !passesFilters(*i.getStateValues(), filters);
    });
    filteredIndividuals.erase(itend, filteredIndividuals.end());

    o.description = outputDescription;
    o.value = get<2>(descriptor)(stateIndex, filteredIndividuals);
    output.push_back(o);
  }

  o.description = "population";
  o.value = (double) individuals_.size();
  output.push_back(o);

  return output;
};


// Getters and setters


QString BaseSimulation::getName() const
{
  return name_;
}

int BaseSimulation::getPopulation() const
{
  return nIndividuals_;
}

int BaseSimulation::getIterations() const
{
  return nIterations_;
}

double BaseSimulation::getTimePeriod() const
{
  return timePeriod_;
}

void BaseSimulation::setName(QString name)
{
  this->name_ = name;
}

void BaseSimulation::setPopulation(int nIndividuals_)
{
  this->nIndividuals_ = nIndividuals_;
}

void BaseSimulation::setIterations(int nIterations_)
{
  this->nIterations_ = nIterations_;
}

void BaseSimulation::setTimePeriod(double timePeriod_)
{
  this->timePeriod_ = timePeriod_;
}

int BaseSimulation::addState(QString name,
                             State* state,
                             bool markForDeletion)
{
  int stateCounter = stateCounter_;
  state->setName(name);
  state->setId(stateCounter);
  states_.push_back(state);
  if (markForDeletion) {
    statesToDelete_.push_back(stateCounter);
  }
  ++stateCounter_;
  return stateCounter;
}

void BaseSimulation::addAnalysisDescriptor(
            QString analysisName,
            int stateIndex,
            AnalysisFunction analysisFunction,
            vector<On> filters)
{
  analysisDescriptors_.push_back(AnalysisDescriptor(analysisName,
      stateIndex, analysisFunction, filters));
}

void BaseSimulation::print() const
{

  cout << "-----------------------" << endl;
  cout << "Simulation: " << this->getName().toStdString() << endl;
  cout << "Population size: " << this->getPopulation() << endl;
  cout << "Time period: " << this->getTimePeriod() << endl;
  cout << "Iterations:" << this->getIterations() << endl;
  cout << "States" << endl;
  cout << "Number entries: " << states_.size() << endl;
  for (auto state : states_) {
    state->print(states_);
  }
  cout << "-----------------------" << endl;
}
