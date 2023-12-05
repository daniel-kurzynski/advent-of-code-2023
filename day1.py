from aocd import get_data, submit

# data = "1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet"
# data = "two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen"
data = get_data(day=1, year=2023)

digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
def search_for_digit_at_position(row, i,writtenDigits):
    if row[i].isdigit():
        return row[i]
    elif writtenDigits:
        for index in range(len(digits)):
            if row[i:].startswith(digits[index]):
                return str(index + 1)
    return None


def find_calibration(row, writtenDigits = False):
    calibration = ""
    for i in range(len(row)):
        digit = search_for_digit_at_position(row, i, writtenDigits)
        if digit is not None:
            calibration = digit
            break;

    for i in reversed(range(len(row))):
        digit = search_for_digit_at_position(row, i, writtenDigits)
        if digit is not None:
            calibration = calibration + digit
            break;

    return int(calibration)


calibrations_1 = [find_calibration(row) for row in data.split("\n")]
print(f"Part 1: Sum of calibrations is: {sum(calibrations_1)}")

calibrations_2 = [find_calibration(row, True) for row in data.split("\n")]
print(f"Part 2: Sum of calibrations is: {sum(calibrations_2)}")
