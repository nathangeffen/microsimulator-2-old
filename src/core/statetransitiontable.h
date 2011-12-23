/*
 * statetransitiontable.h
 *
 *  Created on: 16 Nov 2011
 *      Author: Nathan Geffen
 *
 *
 */

#ifndef STATETRANSITIONTABLE_H_
#define STATETRANSITIONTABLE_H_

#include <QString>
#include <QVariant>
#include <QFile>
#include <qjson/parser.h>


#include "simutils.h"
#include "state.h"
#include "state_parameter.h"

using namespace std;

namespace microsimulator {

enum MatchFunction {
  EQ,
  GTE_LTE,
  GTE_LT,
  GT_LTE,
  GT_LT
};

enum AssignFunction {
  ASSIGN,
  INCREMENT
};

struct InitialValue {
  double value;
  double probability;
};

struct TransitionEntry
{
  int stateIndex;
  MatchFunction matchFunction;
  double lower;
  double upper;
};

struct TransitionRecord
{
  vector < TransitionEntry > entries;
  AssignFunction assignFunction;

  double probability;
  double probabilityTimePeriod;
  double normalizedProbability;
  NormalizeFunction probabilityNormalizeFunction;

  double newValue;
  double valueTimePeriod;
  double normalizedValue;
  NormalizeFunction valueNormalizeFunction;
};

class StateTransitionTable : public State
{
public:
  void addInitialValue(const QMap< QString, QVariant>& fields);
  void addTransitionRecord(int pk, const QMap< QString, QVariant>& fields);
  void addEntryToTransitionRecord(int transitionPk,
                                  int entryStateIndex,
                                  const QMap< QString, QVariant>& fields);
  virtual void prepare(double timePeriod);
  virtual double transition(double value,
                            StateVector& states,
                            IndividualVector& individuals,
                            Individual& individual);
  virtual double initialize();

protected:
  vector < InitialValue > initialValues_;
  vector < TransitionRecord > transitionTable_;

private:
  map < int, int > pkToTransitionRecord_;

};

}

#endif /* STATETRANSITIONTABLE_H_ */
