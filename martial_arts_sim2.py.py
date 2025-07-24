import random
from time import sleep

# --- Fighter Class ---
class Fighter:
    def __init__(self, name, archetype="Boxer"):
        self.name = name
        self.archetype = archetype
        self.level = 1
        self.stats = {
            # Punches
            "jab_accuracy": 50, "jab_speed": 50, "cross_power": 50, "cross_accuracy": 50,
            "hook_power": 50, "hook_speed": 50, "uppercut_power": 50, "uppercut_accuracy": 50,
            # Kicks
            "front_kick_speed": 50, "front_kick_power": 50, "roundhouse_accuracy": 50, 
            "roundhouse_power": 50, "low_kick_power": 50, "low_kick_defense": 50,
            # Clinch
            "elbow_power": 50, "knee_power": 50, "clinch_striking": 50,
            # Defense
            "footwork": 50, "head_movement": 50, "chin": 50, "stamina": 100,
            # Meta
            "aggression": 50, "counter_timing": 50
        }
        self.strike_loadout = []
        self.stance = "orthodox"
        self.energy = 100
        self.set_archetype(archetype)

    def set_archetype(self, archetype):
        """Apply archetype stat modifiers"""
        if archetype == "Pressure Brawler":
            self.stats.update({"hook_power": 70, "chin": 70, "aggression": 80})
        elif archetype == "Counter Sniper":
            self.stats.update({"counter_timing": 70, "head_movement": 70, "footwork": 70})

# --- UI Functions ---
def clear_screen():
    print("\n" * 50)

def show_header(title):
    print(f"=== {title.upper()} ===")
    print("-" * 30)

def show_fighter_stats(fighter):
    print(f"\n{fighter.name} ({fighter.archetype})")
    print(f"Level: {fighter.level} | Energy: {fighter.energy}/100")
    print("Top Attributes:")
    top_stats = sorted(fighter.stats.items(), key=lambda x: x[1], reverse=True)[:3]
    for stat, val in top_stats:
        print(f"  {stat.replace('_', ' ').title()}: {val}")

# --- Combat System ---
class Combat:
    @staticmethod
    def calculate_damage(attacker, defender, strike):
        """Balanced damage formula using all relevant stats"""
        strike_stats = {
            "jab": ["jab_accuracy", "jab_speed"],
            "cross": ["cross_power", "cross_accuracy"],
            "hook": ["hook_power", "hook_speed"],
            "uppercut": ["uppercut_power", "uppercut_accuracy"],
            "front_kick": ["front_kick_power", "front_kick_speed"],
            "roundhouse": ["roundhouse_power", "roundhouse_accuracy"]
        }
        
        attack_score = sum(attacker.stats[stat] for stat in strike_stats[strike]) / 2
        defense_score = (defender.stats["head_movement"] + defender.stats["footwork"]) / 2
        
        # Add randomness (10-20% variance)
        damage = max(1, attack_score * (0.9 + 0.2 * random.random()) - defense_score * 0.5)
        return int(damage)

    def fight_round(self, fighter1, fighter2):
        """Execute one round of combat"""
        clear_screen()
        show_header(f"Round {self.round}")
        
        # Fighter 1 attacks
        if fighter1.strike_loadout:
            strike = random.choice(fighter1.strike_loadout)
            damage = self.calculate_damage(fighter1, fighter2, strike)
            fighter2.stats["stamina"] -= damage
            print(f"{fighter1.name} lands a {strike.replace('_', ' ')} for {damage} damage!")
            sleep(1)
        
        # Fighter 2 attacks
        if fighter2.stats["stamina"] > 0 and fighter2.strike_loadout:
            strike = random.choice(fighter2.strike_loadout)
            damage = self.calculate_damage(fighter2, fighter1, strike)
            fighter1.stats["stamina"] -= damage
            print(f"{fighter2.name} counters with a {strike.replace('_', ' ')} for {damage} damage!")
            sleep(1)
        
        self.round += 1
        return fighter1 if fighter2.stats["stamina"] <= 0 else (fighter2 if fighter1.stats["stamina"] <= 0 else None)

# --- Main Game Loop ---
def main():
    # Create fighters
    player = Fighter("Player", "Pressure Brawler")
    opponent = Fighter("CPU", "Counter Sniper")
    
    # Pre-fight setup
    player.strike_loadout = ["jab", "cross", "hook"]
    opponent.strike_loadout = ["front_kick", "roundhouse"]
    
    # Combat loop
    combat = Combat()
    combat.round = 1
    
    while True:
        winner = combat.fight_round(player, opponent)
        if winner:
            clear_screen()
            show_header("Fight Result")
            print(f"{winner.name} wins by knockout!")
            break
        
        # Between rounds
        print("\n1. Keep current strategy")
        print("2. Change strikes (coming soon)")
        print("3. Rest (recover 20 stamina)")
        choice = input("Choose: ")
        
        if choice == "3":
            player.stats["stamina"] = min(100, player.stats["stamina"] + 20)
            print(f"{player.name} rests and recovers 20 stamina!")
            sleep(1)

if __name__ == "__main__":
    main()