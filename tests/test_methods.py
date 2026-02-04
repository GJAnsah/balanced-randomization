import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import statistics
from balanced_randomization import BalancedRand, SoftBalancedRand

def pure_random(num_trials, num_choices=2):
    counts = {i: 0 for i in range(1, num_choices + 1)}
    options=[]
    
    for trial in range(num_trials):
        option = random.randint(1,num_choices)
        counts[option]+=1
        options.append(option)
    
    return counts,options


def block_random(num_trials,num_choices=2,block_size=4):
    
    if num_choices>block_size:
        raise ValueError("block_size must be >= num_choices")
    if block_size%num_choices != 0:
        raise ValueError("block_size must be divisible by num_choices")
    
    multiplier = block_size//num_choices
    
    block = list(range(1,num_choices+1))*multiplier
    
    counts = {i: 0 for i in range(1, num_choices + 1)}
    options=[]
    
    for trial in range(num_trials):
        
        idx = trial%block_size
        
        if idx == 0:
            random.shuffle(block)
            
        option = block[idx]
        counts[option]+=1
        options.append(option)
    
    return counts,options


def get_imbalance(counts):
    return statistics.stdev(counts.values())


# --- SMART GUESSERS
def smart_guesser_pure_random(num_trials, num_choices=2):
    correct = 0
    for _ in range(num_trials):
        guess = random.randint(1, num_choices)
        actual = random.randint(1, num_choices)
        
        correct += (guess == actual)
    return correct / num_trials

def smart_guesser_block(num_trials,num_choices=2,block_size=4):
    
    correct = 0
    
    multiplier = block_size//num_choices
    
    block = list(range(1,num_choices+1))*multiplier
    
    for trial in range(num_trials):
        
        idx = trial%block_size
        
        if idx == 0:
            random.shuffle(block)
            
        actual = block[idx]
        guess = random.choice(block[idx:])
        
        correct += (guess == actual)
        
    return correct / num_trials

def smart_guesser_balanced_rand(num_trials, num_choices=2,max_imbalance=3):
    
    correct = 0
    
    br = BalancedRand(max_imbalance=max_imbalance, num_choices=num_choices)
    
    for trial in range(num_trials):
        
        counts = br.get_counts()
        min_count = min(counts.values())
        max_count = max(counts.values())
        
        
        if (max_count-min_count)>=max_imbalance:
            min_options = [c for c in counts if counts[c] == min_count]
            guess = random.choice(min_options)
        
        else:
            guess = random.randint(1,num_choices)
        
        actual = br.draw()
        correct += (guess == actual)
    
    return correct / num_trials


def smart_guesser_soft_balanced_rand(num_trials, num_choices=2,max_imbalance=3):
    
    correct = 0
    
    br = SoftBalancedRand(max_imbalance=max_imbalance, num_choices=num_choices)
    
    for trial in range(num_trials):
        
        counts = br.get_counts()
        min_count = min(counts.values())
        max_count = max(counts.values())
        
        min_options = [c for c in counts if counts[c] == min_count]
        

        
        diff = max_count - min_count

        if diff >= max_imbalance:
            # Threshold 1 to max_imbalance, all will trigger
            guess = random.choice(min_options)
        elif diff > 0:
            # Probability that threshold <= diff
            prob_forced = diff / max_imbalance
            if random.random() < prob_forced:
                guess = random.choice(min_options)
            else:
                guess = random.randint(1, num_choices)
        else:
            guess = random.randint(1, num_choices)
            
        actual = br.draw()
        correct += (guess == actual)
    
    return correct / num_trials

def run_tests(num_trials, num_choices=2, num_experiments=500,block_size=4, max_imbalance=3):
    
    results = dict()
    
    rand_imbalances = []
    block_imbalances = []
    balanced_imbalances = []
    soft_imbalances = []
    
    for experiment in range(num_experiments):
        rand_c, rand_o = pure_random(num_trials, num_choices)
        rand_imbalances.append(get_imbalance(rand_c))
        
        block_c, block_o = block_random(num_trials, num_choices, block_size=block_size)
        block_imbalances.append(get_imbalance(block_c))
        
        balanced = BalancedRand(num_choices,max_imbalance=max_imbalance)
        for _ in range(num_trials):
            balanced.draw()
        balanced_imbalances.append(get_imbalance(balanced.get_counts()))
        
        softbalanced = SoftBalancedRand(num_choices,max_imbalance=max_imbalance)
        for _ in range(num_trials):
            softbalanced.draw()
        soft_imbalances.append(get_imbalance(softbalanced.get_counts()))
        
    
    
    results['Pure Random']={'mean_imbalance': statistics.mean(rand_imbalances),
                            'max_imbalance': max(rand_imbalances)}
    
    results['Block Random']={'mean_imbalance': statistics.mean(block_imbalances),
                            'max_imbalance': max(block_imbalances)}
    
    results['Balanced Random']={'mean_imbalance': statistics.mean(balanced_imbalances),
                            'max_imbalance': max(balanced_imbalances)}
    
    results['Soft Balanced Random']={'mean_imbalance': statistics.mean(soft_imbalances),
                            'max_imbalance': max(soft_imbalances)}
    
    
    # Predictability 
    results['Pure Random']['predictability'] = smart_guesser_pure_random(num_trials, num_choices)
    results['Block Random']['predictability'] = smart_guesser_block(num_trials, num_choices,block_size)
    results['Balanced Random']['predictability'] = smart_guesser_balanced_rand(num_trials, num_choices)
    results['Soft Balanced Random']['predictability'] = smart_guesser_soft_balanced_rand(num_trials, num_choices)
    
    # Print table
    print(f"{'Method':<22} {'Mean Imb':<12} {'Max Imb':<12} {'Predictability':<12}")
    print("-" * 70)
    for method, stats in results.items():
        print(f"{method:<22} {stats['mean_imbalance']:<12.2f} {stats['max_imbalance']:<12.2f} {stats['predictability']*100:<5.1f}%")
    
    return results

if __name__ == "__main__":
    run_tests(num_trials=50, num_choices=2, num_experiments=500,block_size=4, max_imbalance=3)
    