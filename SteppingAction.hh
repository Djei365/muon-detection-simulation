#ifndef SteppingAction_h
#define SteppingAction_h 1

#include "G4UserSteppingAction.hh"

class EventAction; // Adicione esta linha antes da classe

class SteppingAction : public G4UserSteppingAction {
  public:
    SteppingAction(EventAction* eventAction); // Modifique aqui
    virtual ~SteppingAction();
    virtual void UserSteppingAction(const G4Step*);
  private:
    EventAction* fEventAction; // Nova variável
};

#endif