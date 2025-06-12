from beta9 import function


@function()
def square(x):
    print("This code is running on a remote worker!")
    return x**2


def main():
    print("The square is", square.remote(42))


if __name__ == "__main__":
    main()
