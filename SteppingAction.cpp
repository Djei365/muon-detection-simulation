#include "SteppingAction.hh"
#include "EventAction.hh"
#include "G4Step.hh"
#include "G4RunManager.hh"
#include "G4AnalysisManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4Track.hh"
#include "G4ParticleDefinition.hh"
#include "G4VPhysicalVolume.hh" // <-- ADICIONADO: Necessário para ler os nomes dos volumes

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

    // Segurança: Verifica se o volume físico existe para evitar crashes
    G4VPhysicalVolume* volumeAtual = step->GetPreStepPoint()->GetTouchableHandle()->GetVolume();
    if (!volumeAtual) return; 

    // Pega o nome do volume atual
    G4String nomeVolume = volumeAtual->GetName();

    // Filtro 2: Registra todos os passos (a cada 10cm) APENAS no ar e nas lajes.
    // REMOVEMOS a trava IsFirstStepInVolume() para permitir o rastreio contínuo!
    if (nomeVolume == "World" || nomeVolume == "Slab_1" || nomeVolume == "Slab_2" || nomeVolume == "Slab_3") {
        
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