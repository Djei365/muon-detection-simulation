#ifndef PrimaryGeneratorAction_h
#define PrimaryGeneratorAction_h 1

#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4ParticleGun.hh"
#include "CRYGenerator.h"
#include "CRYSetup.h"

class PrimaryGeneratorAction : public G4VUserPrimaryGeneratorAction {
  public:
    PrimaryGeneratorAction();    
    virtual ~PrimaryGeneratorAction();
    virtual void GeneratePrimaries(G4Event*);

  private:
    G4ParticleGun* fParticleGun; 
    CRYGenerator* fCRYGenerator;
    CRYSetup* fCRYSetup;
};

#endif