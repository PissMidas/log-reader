from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import time
import pygetwindow

#these are key value pairs of internal names to real names.

#awakenings
#dict_internal_to_external = {"TD_BlessingCooldownRate": "Spark of Focus", "TD_BlessingMaxStagger": "Spark of Resilience", "TD_BlessingPower": "Spark of Strength", "TD_BlessingSpeed": "Spark of Agility", "TD_BuffAndDebuffDuration": "Cast to Last", "TD_ComboATarget": "One-Two Punch", "TD_CreationSize": "Monumentalist", "TD_CreationSizeLifeTime": "Timeless Creator", "TD_DistancePower": "Deadeye", "TD_EmpoweredHitsBuff": "Specialized Training", "TD_EnergyCatalyst": "Catalyst", "TD_EnergyConversion": "Egoist", "TD_EnergyDischarge": "Fire Up!", "TD_EnhancedOrbsCooldown": "Orb Ponderer" , "TD_EnhancedOrbsSpeed": "Orb Dancer", "TD_FasterDashes": "Super Surge", "TD_FasterDashes2": "Chronoboost", "TD_FasterProjectiles": "Missile Propulsion", "TD_FasterProjectiles2": "Aerials", "TD_HitAnythingRestoreStagger": "Tempo Swing", "TD_HitEnemyBurnThem": "Stinger", "TD_HitRockCooldown": "Hotshot", "TD_HitsIncreaseSpeedAndPower": "Stacks on Stacks", "TD_HitsReduceCooldowns": "Perfect Form", "TD_IncreasedPowerWithMaxStagger": "Unstoppable", "TD_IncreasedSpeedWithStagger": "Stagger Swagger", "TD_KOKing": "Prize Fighter", "TD_MovementAbilityCharges": "Twin Drive", "TD_MultiHitsReduceCooldowns": "Heavy Impact", "TD_OrbShare": "Orb Replicator", "TD_PrimaryAbilityCooldownReduction": "Rapid Fire", "TD_PrimaryEcho": "Primetime", "TD_SizeIncrease": "Built Different", "TD_SizeIncrease2": "Big Fish", "TD_SpecialCooldownAfterRounds": "Extra Special", "TD_StaggerCooldownRateConversion": "Reverberation", "TD_StaggerPowerConversion": "Bulk Up", "TD_StaggerSpeedConversion": "PeakPerformance", "TD_StrikeCooldownReduction": "Quick Strikes", "TD_TakeDownReduceCooldowns": "Adrenaline Rush"}

#gears
#dict_internal_to_external.update({"TD_MovementAbilitiesTeleport": "Eject Button", "TD_IncreasedSpeedCrossingMidfield": "Magnetic Soles", "TD_GainRampingSpeed": "Momentum Boots", "TD_HitEnemyDrainThem": "Siphoning Wand", "TD_GoalArcPower": "PowerhousePauldrons", "TD_HitStaggerEnemyCooldownReduction": "Pummelers", "TD_StrikeRockSpeedUp": "Slick Kicks", "TD_RangedStrike": "Strike Shot", "TD_KnockAnythingRecoverStagger": "Vicious Vambraces" })

#characters
#dict_internal_to_external.update({"C_AngelicSupport_C": "Atlas", "C_ChaoticRocketeer_C": "Luna", "C_CleverSummoner_C": "Juno", "C_EDMOni_C": "Octavia", "C_EmpoweringEnchanter_C": "Era", "C_FlashySwordsman_C": "Zentaro", "C_FlexibleBrawler_C": "Juliette", "C_GravityMage_C": "Finii", "C_HulkingBeast_C": "X", "C_MagicalPlaymaker_C": "Ai.Mi", "C_ManipulatingMastermind_C": "Rune", "C_NimbleBlaster_C": "Drek'ar",  "C_RockOni_C": "Vyce", "C_Shieldz_C": "Asher", "C_SpeedySkirmisher_C": "Kai", "C_StalwartProtector_C": "Dubu",  "C_TempoSniper_C": "Estelle", "C_UmbrellaUser_C": "Kazan",  "C_WhipFighter_C": "Rasmus" })

#maps
#dict_internal_to_external.update({"GameMapDigitalWorld": "Aimi's App", "GameMapOniVillage": "Oni Village", "GameMapSummerSplash": "Inky's Splash Zone", "GameMapAtlasLab": "Atlas's Lab", "GameMapObscura": "Gates of Obscura", "GameMapNightMarket": "Night Market" })
#missing demon dais and ahten city

def is_omega_strikers_window_open():
    game_title = "OmegaStrikers"
    windows = pygetwindow.getAllWindows()
    for window in windows:
        if game_title in window.title:
            return True
    return False

def resourcePath(relativePath):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

class LogEventHandler(FileSystemEventHandler):
    def __init__(self, log_file_path):
        super().__init__()
        self.log_file_path = log_file_path
        self.file_size = 0

    def on_modified(self, event):
        if not event.is_directory and event.src_path == self.log_file_path:
            # Get the size of the modified file
            current_size = os.path.getsize(self.log_file_path)

            # Read only the newly added content since the last modification
            with open(self.log_file_path, "r") as file:
                file.seek(self.file_size)
                new_content = file.read()

            # Update the file size
            self.file_size = current_size

            # Process the new log messages
            log_lines = new_content.splitlines()
            for line in log_lines:
                #if 'Training Class' in line or 'Application Will Terminate' in line or 'PostGameCelebration' in line:
                    #this if statement acts as a whitelister. add more to let more messages from the .log file through.

                print(line) #USED FOR DEBUGGING, OR CALL SOME OTHER FUNCTION HERE, SUCH AS MESSAGING WITH A PIPE OR SOCKET.
                if 'Application Will Terminate' in line:
                    print("Omega Strikers is shutting down. also shutting down this observer program")
                    print("this code is being terminated with os._exit(0). please consider changing this in a production setting!")
                    os._exit(0)  # Terminates the program without cleanup. TODO please change this!

if __name__ == "__main__":

    if is_omega_strikers_window_open()== False:
        print("terminating this program because game is not open. try again once you have omega strikers open!")
        sys.exit()
    # Creates the file path to the logs. functionally equivalent to "%LOCALAPPDATA%/OmegaStrikers/Saved/Logs/OmegaStrikers.log"
    log_file_path = os.path.join(os.getenv('LOCALAPPDATA'), 'OmegaStrikers', 'Saved', 'Logs', 'OmegaStrikers.log')

    # Create an instance of LogEventHandler
    log_handler = LogEventHandler(log_file_path)
    time.sleep(1)
    # Create the watchdog observer and start monitoring
    observer = Observer()
    time.sleep(1)
    observer.schedule(log_handler, os.path.dirname(log_file_path), recursive=False)
    time.sleep(1)
    observer.start()

    print("press Control + C to terminate")
    try:
        while True:
            # Keep the script running indefinitely
            time.sleep(1)
    except:
        # Stop the observer when the user presses Ctrl+C
        observer.stop()


    observer.join()  # Wait for the observer thread to finish gracefully
