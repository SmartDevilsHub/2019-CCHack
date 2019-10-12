class Battery:
    def __init__(self, capacity):
        self.capacity = capacity
        self.amount_stored = 0

    def discharge_by(self, amount):
        if self.amount_stored >= amount:
            self.amount_stored -= amount
        else:
            alt_diff = self.amount_stored - amount
            self.amount_stored = 0
            return alt_diff

    def charge_by(self, amount):
        available_space = self.capacity - self.amount_stored
        if available_space >= amount:
            self.amount_stored += amount
        else:
            alt_diff = amount - available_space
            self.amount_stored = self.capacity
            return alt_diff
