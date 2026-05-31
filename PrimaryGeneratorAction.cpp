#include "PrimaryGeneratorAction.hh"
#include "G4Event.hh"
#include "G4ParticleTable.hh"
#include "G4SystemOfUnits.hh"
#include "CRYSetup.h"
#include "CRYGenerator.h"
#include "CRYParticle.h"
#include "CRYUtils.h"

PrimaryGeneratorAction::PrimaryGeneratorAction() {
    fParticleGun = new G4ParticleGun();
    
    // subboxLength 50 garante que a chuva caiba dentro do Mundo do Geant4
    G4String cryConfig = "returnNeutrons 1 returnProtons 1 returnGammas 1 returnPions 1 returnElectrons 1 returnMuons 1 date 3-24-2026 latitude -24.7 altitude 0 subboxLength 50";
    
    // O caminho que sabemos que você tem
    G4String dataPath = "/home/djei/cry_v1.7/data"; 
    
    fCRYSetup = new CRYSetup(cryConfig, dataPath);
    fCRYGenerator = new CRYGenerator(fCRYSetup);
}

PrimaryGeneratorAction::~PrimaryGeneratorAction() {
    delete fCRYGenerator; delete fCRYSetup; delete fParticleGun;
}

void PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent) {
    std::vector<CRYParticle*> *ev = new std::vector<CRYParticle*>;
    fCRYGenerator->genEvent(ev); 
    G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();

    for (unsigned j=0; j < ev->size(); j++) {
        G4int pdgCode = (*ev)[j]->PDGid();
        G4ParticleDefinition* particleDef = particleTable->FindParticle(pdgCode);
        
        if (particleDef) {
            fParticleGun->SetParticleDefinition(particleDef);
            fParticleGun->SetParticleEnergy((*ev)[j]->ke() * MeV);
            // Nascem no topo (z=245m)
            fParticleGun->SetParticlePosition(G4ThreeVector((*ev)[j]->x() * m, (*ev)[j]->y() * m, 245.0 * m));
            fParticleGun->SetParticleMomentumDirection(G4ThreeVector((*ev)[j]->u(), (*ev)[j]->v(), (*ev)[j]->w()));
            fParticleGun->GeneratePrimaryVertex(anEvent);
        }
        delete (*ev)[j];
    }
    delete ev;
}