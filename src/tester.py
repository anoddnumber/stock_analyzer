from scripts.utilities.utils import Utils
from scripts.report_generator import ReportGenerator

print(Utils.calculate_yoy_return(375, 1800))
print(Utils.calculate_yoy_return(1800, 375))
print(Utils.calculate_yoy_return(375, -1800))
print(Utils.calculate_yoy_return(-375, -1800))
print(Utils.calculate_yoy_return(-375, 1800))

ReportGenerator.generate_report('AMZN')