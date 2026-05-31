#include "RunAction.hh"
#include "G4AnalysisManager.hh"
#include "G4SystemOfUnits.hh"

RunAction::RunAction() : G4UserRunAction() {
    auto analysisManager = G4AnalysisManager::Instance();
    analysisManager->SetDefaultFileType("csv");
    analysisManager->SetVerboseLevel(1);
    
    // Criando o arquivo e a tabela (Ntuple)
    analysisManager->CreateNtuple("MuonsUTFPR", "Dados Filtrados apenas de Muons");
    analysisManager->CreateNtupleDColumn("Altura_Z_metros"); // Coluna 0
    analysisManager->CreateNtupleDColumn("Energia_MeV");    // Coluna 1
    analysisManager->FinishNtuple();
}

RunAction::~RunAction() {}

void RunAction::BeginOfRunAction(const G4Run*) {
    G4AnalysisManager::Instance()->OpenFile("dados_muons.csv");
}

void RunAction::EndOfRunAction(const G4Run*) {
    auto analysisManager = G4AnalysisManager::Instance();
    analysisManager->Write();
    analysisManager->CloseFile();
}