#include "G4RunManagerFactory.hh"
#include "G4UImanager.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"
#include "DetectorConstruction.hh" 
#include "ActionInitialization.hh"
#include "FTFP_BERT.hh" 

int main(int argc, char** argv) {
    // ---------------------------------------------------------
    // O TRUQUE: Só cria a interface se não houver argumentos (.mac)
    // Se argc == 1, significa que você digitou apenas ./muonSim
    // ---------------------------------------------------------
    G4UIExecutive* ui = nullptr;
    if (argc == 1) {
        ui = new G4UIExecutive(argc, argv);
    }

    auto* runManager = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Default);

    // 1. Geometria
    runManager->SetUserInitialization(new DetectorConstruction());
    
    // 2. Física 
    runManager->SetUserInitialization(new FTFP_BERT());
    
    // 3. Ação 
    runManager->SetUserInitialization(new ActionInitialization());

    // Inicializa tudo
    runManager->Initialize();

    G4VisManager* visManager = new G4VisExecutive;
    visManager->Initialize();
    
    G4UImanager* UImanager = G4UImanager::GetUIpointer();
    
    // ---------------------------------------------------------
    // AS DUAS PERSONALIDADES DO SIMULADOR
    // ---------------------------------------------------------
    if (!ui) {
        // PERSONALIDADE 1: BATCH MODE (Silencioso)
        // Como o 'ui' é nulo, ele executa o arquivo (producao.mac) que você passou no terminal
        G4String command = "/control/execute ";
        G4String fileName = argv[1];
        UImanager->ApplyCommand(command + fileName);
    } 
    else {
        // PERSONALIDADE 2: MODO INTERATIVO (Com tela)
        // Se você tiver um arquivo de visualização, descomente a linha abaixo:
        // UImanager->ApplyCommand("/control/execute vis.mac");
        
        ui->SessionStart();
        delete ui;
    }
    
    delete visManager; 
    delete runManager;
    return 0;
}