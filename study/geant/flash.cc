// flash.cc -- prompt neutron/photon flash at an SNS BSM fixed-target near detector.
//
// Geometry: 1.3 GeV proton pencil beam on a bare compact tungsten dump
// (r = 15 cm, L = 30 cm ~ 3 nuclear interaction lengths) in an air-filled
// hall. Every particle crossing one of three transverse scoring planes
// downstream of the dump is recorded (PDG id, kinetic energy, global time,
// radius at crossing):
//   plane 0: z = 0.6 m,  r < 0.5 m  (decay-chamber entrance, "near" config)
//   plane 1: z = 3.6 m,  r < 0.5 m  (calorimeter face, end of 3 m chamber)
//   plane 2: z = 15 m,   r < 1.0 m  (far-hall detector location)
// Primaries start at t = 0 (delta pulse); the beam pulse shape is convolved
// in the analysis. Physics list: Shielding (HP neutron transport).
// Tracks are killed below 100 keV (neutrons) or beyond 10 us global time.

#include "G4RunManagerFactory.hh"
#include "G4PhysListFactory.hh"
#include "G4VUserDetectorConstruction.hh"
#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4VUserActionInitialization.hh"
#include "G4UserSteppingAction.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4NistManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4UImanager.hh"
#include "G4Threading.hh"
#include "G4Step.hh"
#include "G4Track.hh"
#include "G4Neutron.hh"

#include <fstream>
#include <sstream>
#include <string>

namespace {
constexpr double kPlaneZ[3] = {60. * cm, 360. * cm, 1500. * cm};
constexpr double kPlaneR[3] = {50. * cm, 50. * cm, 100. * cm};
constexpr double kTimeCut = 10. * microsecond;
constexpr double kNeutronEkinCut = 100. * keV;
}  // namespace

class DetectorConstruction : public G4VUserDetectorConstruction {
 public:
  G4VPhysicalVolume* Construct() override {
    auto* nist = G4NistManager::Instance();
    auto* air = nist->FindOrBuildMaterial("G4_AIR");
    auto* tungsten = nist->FindOrBuildMaterial("G4_W");

    auto* worldS = new G4Box("World", 4. * m, 4. * m, 20. * m);
    auto* worldL = new G4LogicalVolume(worldS, air, "World");
    auto* worldP = new G4PVPlacement(nullptr, {}, worldL, "World", nullptr,
                                     false, 0, true);

    auto* dumpS = new G4Tubs("Dump", 0., 15. * cm, 15. * cm, 0., 360. * deg);
    auto* dumpL = new G4LogicalVolume(dumpS, tungsten, "Dump");
    new G4PVPlacement(nullptr, {0., 0., 15. * cm}, dumpL, "Dump", worldL,
                      false, 0, true);
    return worldP;
  }
};

class PrimaryGenerator : public G4VUserPrimaryGeneratorAction {
 public:
  PrimaryGenerator() : fGun(1) {
    fGun.SetParticleDefinition(
        G4ParticleTable::GetParticleTable()->FindParticle("proton"));
    fGun.SetParticleEnergy(1.3 * GeV);
    fGun.SetParticlePosition({0., 0., -10. * cm});
    fGun.SetParticleMomentumDirection({0., 0., 1.});
  }
  void GeneratePrimaries(G4Event* evt) override { fGun.GeneratePrimaryVertex(evt); }

 private:
  G4ParticleGun fGun;
};

class FlashSteppingAction : public G4UserSteppingAction {
 public:
  FlashSteppingAction() {
    std::ostringstream name;
    name << "flash_hits_t" << G4Threading::G4GetThreadId() << ".csv";
    fOut.open(name.str());
    fOut << "plane,pdg,ekin_MeV,t_ns,r_cm\n";
  }
  ~FlashSteppingAction() override { fOut.close(); }

  void UserSteppingAction(const G4Step* step) override {
    auto* track = step->GetTrack();
    if (track->GetGlobalTime() > kTimeCut) {
      track->SetTrackStatus(fStopAndKill);
      return;
    }
    if (track->GetDefinition() == G4Neutron::Definition() &&
        track->GetKineticEnergy() < kNeutronEkinCut) {
      track->SetTrackStatus(fStopAndKill);
      return;
    }

    const auto& p1 = step->GetPreStepPoint()->GetPosition();
    const auto& p2 = step->GetPostStepPoint()->GetPosition();
    for (int i = 0; i < 3; ++i) {
      if (p1.z() < kPlaneZ[i] && p2.z() >= kPlaneZ[i]) {
        const double f = (kPlaneZ[i] - p1.z()) / (p2.z() - p1.z());
        const double x = p1.x() + f * (p2.x() - p1.x());
        const double y = p1.y() + f * (p2.y() - p1.y());
        const double r = std::hypot(x, y);
        if (r < kPlaneR[i]) {
          const double t = step->GetPreStepPoint()->GetGlobalTime() +
                           f * step->GetDeltaTime();
          const double ekin = step->GetPostStepPoint()->GetKineticEnergy();
          if (ekin > 0.1 * MeV) {
            fOut << i << ',' << track->GetDefinition()->GetPDGEncoding()
                 << ',' << ekin / MeV << ',' << t / ns << ',' << r / cm
                 << '\n';
          }
        }
      }
    }
  }

 private:
  std::ofstream fOut;
};

class ActionInitialization : public G4VUserActionInitialization {
 public:
  void Build() const override {
    SetUserAction(new PrimaryGenerator);
    SetUserAction(new FlashSteppingAction);
  }
};

int main(int argc, char** argv) {
  const int nEvents = (argc > 1) ? std::atoi(argv[1]) : 1000;
  auto* runManager =
      G4RunManagerFactory::CreateRunManager(G4RunManagerType::Default);
  runManager->SetNumberOfThreads(4);
  runManager->SetUserInitialization(new DetectorConstruction);

  G4PhysListFactory factory;
  runManager->SetUserInitialization(factory.GetReferencePhysList("Shielding"));
  runManager->SetUserInitialization(new ActionInitialization);

  auto* ui = G4UImanager::GetUIpointer();
  ui->ApplyCommand("/run/initialize");
  ui->ApplyCommand("/run/beamOn " + std::to_string(nEvents));

  delete runManager;
  return 0;
}
