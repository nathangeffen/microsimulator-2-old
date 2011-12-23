/*
 * statetransitiontable.cpp
 *
 *  Created on: 16 Nov 2011
 *      Author: nathan
 */

#include <QString>
#include <QVariant>
#include <QDebug>
#include <QFile>
#include <qjson/parser.h>
#include <iostream>

#include "simutils.h"
#include "statetransitiontable.h"

using namespace microsimulator;


void StateTransitionTable::addInitialValue(
                                  const QMap< QString, QVariant>& fields)
{
  InitialValue initialValue;
  initialValue.value = fields[ "value" ].toReal();
  initialValue.probability = fields [ "probability" ].toReal();
  initialValues_.push_back(initialValue);
}

void StateTransitionTable::addTransitionRecord(
                               int pk, const QMap< QString, QVariant>& fields)
{
  TransitionRecord transitionRecord;

  // Set transition values

  QString assignFunction = fields[ "assign_function" ].toString();

  if ( assignFunction == "AS" ) {
    transitionRecord.assignFunction = ASSIGN;
  } else if ( assignFunction == "IN" ) {
    transitionRecord.assignFunction = INCREMENT;
  } else {
    throw SimulationException("Invalid assign function " + assignFunction,
                              __LINE__, __FILE__);
  }

  transitionRecord.newValue = fields[ "new_value" ].toReal();
  transitionRecord.valueTimePeriod = fields[ "value_time_period" ].toReal();

  QString valueNormalizeFunction = fields[ "value_normalize_function" ].toString();

  if ( valueNormalizeFunction == "0" ) {
    transitionRecord.valueNormalizeFunction = normalize_identity;
  } else if ( valueNormalizeFunction == "1" ) {
    transitionRecord.valueNormalizeFunction = normalize_linear_proportion;
  } else if ( valueNormalizeFunction == "2" ) {
    transitionRecord.valueNormalizeFunction = normalize_compounded_proportion;
  } else {
    throw SimulationException("Invalid probability normalize function " +
                               valueNormalizeFunction,
                              __LINE__, __FILE__);
  }

  // Set probability of transition values

  transitionRecord.probability = fields[ "probability" ].toReal();
  transitionRecord.probabilityTimePeriod = fields[ "probability_time_period" ].toReal();

  QString probabilityNormalizeFunction = fields[ "probability_normalize_function" ].toString();

  if ( probabilityNormalizeFunction == "0" ) {
    transitionRecord.probabilityNormalizeFunction = normalize_identity;
  } else if ( probabilityNormalizeFunction == "1" ) {
    transitionRecord.probabilityNormalizeFunction = normalize_linear_proportion;
  } else if ( probabilityNormalizeFunction == "2" ) {
    transitionRecord.probabilityNormalizeFunction = normalize_compounded_proportion;
  } else {
    throw SimulationException("Invalid probability normalize function " +
                               probabilityNormalizeFunction,
                              __LINE__, __FILE__);
  }

  transitionTable_.push_back(transitionRecord);
  pkToTransitionRecord_[pk] = transitionTable_.size() - 1;
}

void StateTransitionTable::addEntryToTransitionRecord(
                                  int transitionPk,
                                  int entryStateIndex,
                                  const QMap< QString, QVariant>& fields)
{
  TransitionEntry transitionEntry;

  transitionEntry.stateIndex = entryStateIndex;
  transitionEntry.lower = fields[ "lower" ].toReal();
  transitionEntry.upper = fields[ "lower" ].toReal();

  QString matchFunction = fields[ "match_function" ].toString();

  if ( matchFunction == "EQ" ) {
    transitionEntry.matchFunction = EQ;
  } else if ( matchFunction == "GTE_LTE" ) {
    transitionEntry.matchFunction = GTE_LTE;
  } else if ( matchFunction == "GTE_LT" ) {
    transitionEntry.matchFunction = GTE_LT;
  } else if ( matchFunction == "GT_LTE" ) {
    transitionEntry.matchFunction = GT_LTE;
  } else if ( matchFunction == "GT_LT" ) {
    transitionEntry.matchFunction = GT_LT;
  }

  int transitionIndex = pkToTransitionRecord_[transitionPk];
  transitionTable_[transitionIndex].entries.push_back(transitionEntry);
}

double StateTransitionTable::initialize()
{
  for ( int i=0; i<initialValues_.size() - 1; i++ ) {
    if ( frand() <= initialValues_[i].probability ) {
      return initialValues_[i].value;
    }
  }
  int lastEntry = initialValues_.size() - 1;
  if ( lastEntry >= 0 ) {
    return initialValues_[lastEntry].value;
   } else {
    return 0.0;
  }
}

double StateTransitionTable::transition(
                                      double value,
                                      StateVector& states,
                                      IndividualVector& individuals,
                                      Individual& individual)
{
  for ( auto record : transitionTable_ ) {
    bool match = false;
    for ( auto entry : record.entries ) {
      switch ( entry.matchFunction ) {
        case ( EQ ):
          if ( value == entry.lower )
            match = true;
          break;
        case ( GTE_LTE ):
          if ( value >= entry.lower && value <= entry.upper )
            match = true;
        case ( GTE_LT ):
          if ( value >= entry.lower && value < entry.upper )
            match = true;
          break;
        case ( GT_LTE ):
          if ( value > entry.lower && value <= entry.upper )
            match = true;
          break;
        case ( GT_LT ):
          if ( value > entry.lower && value < entry.upper )
            match = true;
          break;
      }
      if ( !match ) break;
    }
    if ( match ) {
      if ( frand() < record.normalizedProbability ) {
        if ( record.assignFunction == ASSIGN ) {
          return record.normalizedValue;
        } else {
          return value + record.normalizedValue;
        }
      } else {
        // Event did not occur, then just return the state value unchanged
        return value;
      }
    }
  }
  // No match, then just return the state value unchanged.
  return value;
}

void StateTransitionTable::prepare(double toTimePeriod)
{

  //Check that if there are any initial values, the probabilities add to 1.0
  double sumProbability = 0.0;
  if ( initialValues_.size() > 0 ) {
    for ( auto initialValue : initialValues_ ) {
      sumProbability += initialValue.probability;
    }
    if ( sumProbability != 1.0 ) {
      QString s;
      s.setNum(sumProbability, 'g', 2);
      s = "Cumulative probability of all initial values equals " + s + " not 1";
      throw SimulationException(s.toStdString().c_str(),
                                __LINE__, __FILE__);
    }
  }

  //Normalize values and probabilities
  for ( auto record : transitionTable_ ) {

    if ( record.valueTimePeriod != toTimePeriod ) {
      record.normalizedValue = record.valueNormalizeFunction(
                                                         record.newValue,
                                                         record.valueTimePeriod,
                                                         toTimePeriod );
    } else {
      record.normalizedValue = record.newValue;
    }

    if ( record.probabilityTimePeriod != toTimePeriod ) {
      record.normalizedProbability = record.probabilityNormalizeFunction(
                                                   record.probability,
                                                   record.probabilityTimePeriod,
                                                   toTimePeriod );
    } else {
      record.normalizedProbability = record.probability;
    }

  }
}
