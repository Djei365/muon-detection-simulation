#ifndef EventAction_h
#define EventAction_h 1
#include "G4UserEventAction.hh"
#include "globals.hh"

class EventAction : public G4UserEventAction {
  public:
    EventAction();
    virtual ~EventAction();
    virtual void BeginOfEventAction(const G4Event*);
    virtual void EndOfEventAction(const G4Event*);

    // Método para o espião ir pingando energia aqui
    void AddEnergy(G4double edep) { fTotalEnergy += edep; }

  private:
    G4double fTotalEnergy;
};
#endif