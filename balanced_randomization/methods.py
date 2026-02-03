import random

class BalancedRand:
    
    """
    Generates random integer between a set of options with a hard balance constraint.
    
    When any option has been overdrawn (i.e. count creates imbalance in count distribution)
    the algorithm forces selection of underrepresented choices.
    
    Parameters
    ----------
    num_choices : int
        Number of possible choices (default: 2)
    max_imbalance : int
        Maximum allowed deviation from expected count (default: 3)
    
    Example
    -------
    >>> br = BalancedRand(num_choices=2, max_imbalance=3)
    >>> choices = [br.draw() for _ in range(50)]
    >>> print(br.get_counts())
    """
    
    
    def __init__(self,num_choices = 2, max_imbalance = 3):
        if num_choices < 2:
            raise ValueError("num_choices must be at least 2")
        if max_imbalance < 1:
            raise ValueError("max_imbalance must be at least 1")
            
        self.max_imbalance = max_imbalance
        self.num_choices = num_choices
        self._counts = {i: 0 for i in range(1, self.num_choices + 1)}
        
    
    def draw(self):
        
        """
        Draw a random choice with balance constraint.
        
        Returns
        -------
        int
            A choice from 1 to num_choices
        """
        
        min_count = min(self._counts.values())
        max_count = max(self._counts.values())
        
        
        if (max_count-min_count)>=self.max_imbalance:
            min_options = [c for c in self._counts if self._counts[c] == min_count]
            option_to_return = random.choice(min_options)
        
        else:
            option_to_return = random.randint(1,self.num_choices)
        
        self._counts[option_to_return]+=1
        
        return option_to_return
    
    def get_counts(self):
        
        """
        Return the current counts of each option
        
        """
        
        return self._counts.copy()
    
    def reset(self):
        """
        Reset all counts
        """
        self._counts = {i: 0 for i in range(1, self.num_choices + 1)}
        
    

class SoftBalancedRand(BalancedRand):
    """
    Generates random integer between a set of options with a soft balance constraint.
    
    When any option has been overdrawn (i.e. count creates imbalance in count distribution)
    the algorithm forces selection of underrepresented choices.
    This is different from balanced round in that imbalance threshold is made to be variable
    
    Parameters
    ----------
    num_choices : int
        Number of possible choices (default: 2)
    max_imbalance : int
        Maximum allowed deviation from expected count (default: 3)
    
    Example
    -------
    >>> br = SoftBalancedRand(num_choices=2, max_imbalance=3)
    >>> choices = [br.draw() for _ in range(50)]
    >>> print(br.get_counts())
    """
    
    def draw(self):
        
        """
        Draw a random choice with soft balance constraint.
        Returns
        -------
        int
            A choice from 1 to num_choices
        """
        
        imbalance = random.randint(1,self.max_imbalance)
        
        min_count = min(self._counts.values())
        max_count = max(self._counts.values())
        
        
        if (max_count-min_count)>=imbalance:
            min_options = [c for c in self._counts if self._counts[c] == min_count]
            option_to_return = random.choice(min_options)
        
        else:
            option_to_return = random.randint(1,self.num_choices)
        
        self._counts[option_to_return]+=1
        
        return option_to_return
    