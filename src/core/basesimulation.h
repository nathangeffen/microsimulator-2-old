/*
 * BaseSimulation.h
 *
 *  Created on: 12 Oct 2011
 *      Author: Nathan Geffen
 */

#ifndef MICROSIMULATOR_H_
#define MICROSIMULATOR_H_

#include <vector>
#include <map>
#include <tuple>
#include <QByteArray>
#include <QString>
#include <QFile>
#include <QMap>

#include "simutils.h"
#include "individual.h"
#include "state.h"
#include "stateage.h"
#include "state_parameter.h"

namespace microsimulator {

const ParameterMap emptyParameterMap;
const StateVector emptyStateVector;
const FilterFunctionList emptyFilterFunctionVector;

class BaseSimulation
{
public:
  BaseSimulation (int nIndividuals=defaultNumberIndividuals,
                  int nIterations=defaultNumberIterations,
                  double timePeriod=YEAR,
                  const StateVector& states=emptyStateVector) :
    nIndividuals_(nIndividuals),
    nIterations_(nIterations),
    timePeriod_(timePeriod),
    states_(states),
    stateCounter_(0) {};
  virtual ~BaseSimulation();

  virtual void prepare();
  void simulate();
  AnalysisOutput analyze();

  void loadStates(const QByteArray& inputTable,
                  const SimulationFormat& tableFormat);
  void loadStates(QFile& inputFile, const SimulationFormat& tableFormat);

  // Getters and setters
  int getIndividuals() const;
  int getIterations() const;
  double getTimePeriod() const;
  ParameterMap getParameters() const;
  double getParameterValue(QString name) const;
  double getParameterNormalizedValue(QString name) const;
  double getParameterTimePeriod(string name) const;

  void setIndividuals(int nIndividuals_);
  void setIterations(int nIterations_);
  void setTimePeriod(double timePeriod_);
  int addState(QString name, State* const state, bool markForDeletion=false);
  void addAnalysisDescriptor(QString AnalysisName,
                             int stateIndex,
                             AnalysisFunction function,
                             FilterFunctionList filters=
                                                     emptyFilterFunctionVector);

protected:
  void loadStatesFromJsonTable(const QByteArray& inputTable);
  void loadJsonState(const QMap< QString, QVariant >& fields);
  void loadJsonInitialValue(const QMap< QString, QVariant >& fields);
  void loadJsonTransitionRecord(const QMap< QString, QVariant>& fields);
  void loadJsonEntry(const QMap< QString, QVariant>& fields);

  int nIndividuals_;
  int nIterations_;
  double timePeriod_;
  IndividualVector individuals_;
  StateVector states_;
  vector<int> statesToDelete_;
  AnalysisDescriptorVector analysisDescriptors_;
private:
  int stateCounter_;
  map < int, int > pkToState_;
  map < int, int > transitionPktoState_;
};

}

#endif /* SIMULATION_H_ */
