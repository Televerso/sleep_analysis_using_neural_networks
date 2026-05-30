import os


if __name__ == "__main__":
    os.system("pybabel update -i ../sleep_analysis.pot -d .. -l ru_RU -D sleep_analysis")
    os.system("pybabel update -i ../sleep_analysis.pot -d .. -l en_US -D sleep_analysis")
    os.system("pybabel update -i ../sleep_analysis.pot -d .. -l en_GB -D sleep_analysis")