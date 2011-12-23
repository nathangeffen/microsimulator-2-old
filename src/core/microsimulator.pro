QT += core
QT -= gui

TARGET = microsim

CONFIG += qt 
CONFIG += console
CONFIG += debug
CONFIG -= app_bundle

TEMPLATE = app

QMAKE_CXXFLAGS += -std=c++0x

LIBS += -lqjson

HEADERS += basesimulation.h
HEADERS += stateage.h
HEADERS += statetransitiontable.h
HEADERS += individual.h
HEADERS += state.h
HEADERS += tbsimulation.h
HEADERS += simutils.h
HEADERS += state_parameter.h
HEADERS += tb_states.h

SOURCES += main.cpp
SOURCES += basesimulation.cpp  
SOURCES += simutils.cpp  
SOURCES += state_parameter.cpp
SOURCES += tb_states.cpp
SOURCES += individual.cpp
SOURCES += stateage.cpp
SOURCES += statetransitiontable.cpp
SOURCES += state.cpp
SOURCES += tbsimulation.cpp



