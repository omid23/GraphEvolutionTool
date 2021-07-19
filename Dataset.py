from math import sqrt


class Dataset:
    max: float  # Max value in Dataset
    min: float  # Minimum value in Dataset
    count: int  # Number of values added to the Dataset
    mu: float  # Average of sum
    sd: float  # Standard deviation
    CI95: float  # 95% Confidence Interval
    empty: bool  # Whether set is empty or not
    computed: bool  # Keeps track if statistical analysis has occurred yet
    sum: float  # Sum of all values in Dataset
    sums: float  # Sum of all values squared in Dataset

    def __init__(self):
        # TODO: MICHAEL's comment ! Seriously.....just turn add into a constructor...
        self.sum = 0.0
        self.sums = 0.0
        self.max = 0.0
        self.min = 0.0
        self.count = 0
        self.mu = 0.0
        self.sd = 0.0
        self.CI95 = 0.0
        self.empty = True
        self.computed = False

    # Adds the values within vals to the Dataset
    def add(self, vals):
        if self.empty:  # Clear
            self.sum = 0.0
            self.sums = 0.0
            self.max = vals[0]
            self.min = vals[0]
            self.count = 0
            self.mu = 0.0
            self.sd = 0.0
            self.CI95 = 0.0
            self.empty = False
            self.computed = False

        for val in vals:
            self.sum += val
            self.sums += val * val
            if val > self.max:
                self.max = val

            if val < self.min:
                self.min = val

        self.count += len(vals)

    # Calculates the 95% Confidence Interval, Mu and Standard Deviation
    def compute(self):
        # double n

        if not self.empty:
            n = float(self.count)
            self.mu = self.sum / n
            if self.count > 1:
                self.sd = self.sums / n - self.mu * self.mu
                if self.sd > 0:
                    self.sd = sqrt(self.sd)
                else:
                    self.sd = 0.0

                self.CI95 = 1.96 * self.sd / sqrt(n - 1.0)
            else:
                self.sd = 0.0
                self.CI95 = 0.0

        self.computed = True

    def getMu(self):
        if not self.computed:
            self.compute()
            # TODO: Exceptions for these bools
        return self.mu

    def getSD(self):
        if not self.computed:
            self.compute()

        return self.sd

    def getCI(self):
        if not self.computed:
            self.compute()

        return self.CI95

    def getMin(self):
        if not self.computed:
            self.compute()
        return self.min

    def getMax(self):
        if not self.computed:
            self.compute()

        return self.max

    def getReport(self) -> str:
        if not self.computed:
            self.compute()

        return str(self.mu) + " " + str(self.CI95) + " " + str(self.sd) + " " + str(self.min) + "\n"
