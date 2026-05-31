#include "SteppingAction.hh"
#include "EventAction.hh"
#include "G4Step.hh"
#include "G4RunManager.hh"
#include "G4AnalysisManager.hh"
#include "G4SystemOfUnits.hh"

#include "G4Track.hh"
#include "G4SystemOfUnits.hh"
#include "G4ParticleDefinition.hh"


SteppingAction::SteppingAction(EventAction*) : G4UserSteppingAction() {}
SteppingAction::~SteppingAction() {}

void SteppingAction::UserSteppingAction(const G4Step* step)
{
    G4Track* track = step->GetTrack();

    // Filtro 1: Queremos apenas registrar múons (mu- e mu+)
    G4String particleName = track->GetDefinition()->GetParticleName();
    if (particleName != "mu-" && particleName != "mu+") {
        return;
    }

    // Filtro 2: Registra apenas o primeiro passo dentro de um volume 
    // (evita contar o mesmo múon várias vezes no mesmo milímetro)
    if (step->IsFirstStepInVolume()) {
        
        // 1. Altitude (Z) convertida para metros
        G4double z_m = track->GetPosition().z() / m;

        // 2. Momento Total (p) convertido para GeV/c
        G4double p_GeV = track->GetMomentum().mag() / GeV;

        // 3. Ângulo Zenital (Theta) em radianos
        G4double theta_rad = track->GetMomentumDirection().theta();

        // Imprime os 3 valores separados por vírgula para o CSV
        G4cout << z_m << "," << p_GeV << "," << theta_rad << G4endl;
    }
}