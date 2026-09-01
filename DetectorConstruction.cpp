#include "DetectorConstruction.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"
#include "G4Color.hh"
#include "G4UserLimits.hh" // <-- ADICIONADO: Biblioteca do limitador de passos

DetectorConstruction::DetectorConstruction() : G4VUserDetectorConstruction() {}
DetectorConstruction::~DetectorConstruction() {}

G4VPhysicalVolume* DetectorConstruction::Construct() {
    G4NistManager* nist = G4NistManager::Instance();
    G4Material* air = nist->FindOrBuildMaterial("G4_AIR");
    G4Material* concrete = nist->FindOrBuildMaterial("G4_CONCRETE");
    G4Material* plastic = nist->FindOrBuildMaterial("G4_POLYSTYRENE"); 

    // Mundo para 120m x 120m para que a nuvem do CRY (100m) caiba toda dentro
    G4Box* solidWorld = new G4Box("World", 60*m, 60*m, 300*m); 
    G4LogicalVolume* logicWorld = new G4LogicalVolume(solidWorld, air, "World");
    G4VPhysicalVolume* physWorld = new G4PVPlacement(0, G4ThreeVector(0,0,0), logicWorld, "World", 0, false, 0);
    logicWorld->SetVisAttributes(G4VisAttributes::GetInvisible());

    // =========================================================================
    // LIMITADOR DE PASSOS (STEP LIMITER) ADICIONADO AQUI
    // Isso força o Geant4 a registrar a posição da partícula a cada 10 cm no ar.
    // Assim, o Python terá dados suficientes para desenhar o gráfico contínuo!
    // =========================================================================
    G4double maxStep = 10.0 * cm;
    G4UserLimits* limitadorAr = new G4UserLimits(maxStep);
    logicWorld->SetUserLimits(limitadorAr);
    // =========================================================================

    // As 3 Lajes do Prédio (Posicionadas no Fundo, entre z=5m e z=11m)
    G4Box* solidSlab = new G4Box("Slab", 30*m, 3*m, 30*cm);
    G4LogicalVolume* logicSlab = new G4LogicalVolume(solidSlab, concrete, "Slab");
    logicSlab->SetVisAttributes(new G4VisAttributes(G4Color(0.5, 0.5, 0.5))); // Cinza

    new G4PVPlacement(0, G4ThreeVector(0, 0, 5.0*m), logicSlab, "Slab_1", logicWorld, false, 0);
    new G4PVPlacement(0, G4ThreeVector(0, 0, 8.0*m), logicSlab, "Slab_2", logicWorld, false, 0);
    new G4PVPlacement(0, G4ThreeVector(0, 0, 11.0*m), logicSlab, "Slab_3", logicWorld, false, 0);

    // O Sensor de Múons 
    G4Box* solidDetector = new G4Box("Detector", 30*m, 3*m, 5*cm);
    G4LogicalVolume* logicDetector = new G4LogicalVolume(solidDetector, plastic, "Detector");
    logicDetector->SetVisAttributes(new G4VisAttributes(G4Color(1.0, 0.0, 0.0))); // Vermelho
    new G4PVPlacement(0, G4ThreeVector(0, 0, 0), logicDetector, "Detector_Phys", logicWorld, false, 0);

    return physWorld;
}