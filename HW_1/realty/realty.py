class Realty(object):
    def __init__(self, name: str, area: float):
        if not area:
            raise ValueError("area should be provided nd be pasitive float value")
        
        self.name = name
        self.area = area

    def greet(self):
        greeting = f"Hello, {self.name}"
        return greeting

    @staticmethod
    def calculate_monthly_payment(value: int, years: int, interest: float) -> float:
        monthly_interest = interest / 12.0
        overall_interest = (1.0 + monthly_interest) ** (years * 12)
        monthly_payment = value * monthly_interest * overall_interest / (overall_interest - 1.0)
        return monthly_payment

    @classmethod
    def load_from_file(cls, filepath: str):
        with open(filepath) as fin:
            name, area = fin.read().strip().split()
            area =float(area)
            return cls(name=name, area=area)

    def __repr__(self):
        repr_ = f"{self.__class__.__name__} (name='{self.name}', area={self.area})"
        return repr_

    def __eq__(self, rhs):
        outcome = (
            (self.name == rhs.name)
            and (self.area == rhs.area)
        )
        return outcome