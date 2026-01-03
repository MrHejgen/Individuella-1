class Package:
    """Klass för paket som ska levereras i lastbilarna."""

    def __init__(
        self,
        package_id: int,
        weight: float,
        profit: float,
        deadline: int,
        volume: float,
    ) -> None:
        self.package_id = package_id
        self.weight = weight
        self.profit = profit
        self.deadline = deadline
        self.volume = volume

    def calculate_profit(self) -> float:
        if self.deadline < 0:
            days_late = abs(self.deadline)
            penalty = days_late**2
            return self.profit - penalty
        return self.profit


class Truck:
    """Klass för lastbilar som levererar paketen."""

    def __init__(self, truck_id: str) -> None:
        self.truck_id = truck_id
        self.weight_capacity: float = 800
        self.volume_capacity: float = 1000
        self.packages: list[Package] = []
        self.current_weight: float = 0
        self.current_volume: float = 0

    def add_package(self, package: Package) -> bool:
        if self.current_weight + package.weight <= self.weight_capacity:
            if self.current_volume + package.volume <= self.volume_capacity:
                self.current_volume += package.volume
                self.current_weight += package.weight
                self.packages.append(package)
                return True
        return False
