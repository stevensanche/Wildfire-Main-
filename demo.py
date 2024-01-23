'''demo code
'''


def find_string(str1, sub_str):
    if any(sub_str in s for s in str1):
        return True
    return False


def main():
    print(find_string(["red", "black", "white", "green", "orange"], "ack"))


main()

