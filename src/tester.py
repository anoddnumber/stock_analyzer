from scripts.utilities.utils import Utils
print(Utils.calculate_yoy_return(375, 1800))
print(Utils.calculate_yoy_return(1800, 375))
print(Utils.calculate_yoy_return(375, -1800))
print(Utils.calculate_yoy_return(-375, -1800))
print(Utils.calculate_yoy_return(-375, 1800))