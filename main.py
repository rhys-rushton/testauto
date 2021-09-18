#import the user class object
from classes import userClass

#main function that will do everything
def main():
    em = input("enter email please ")
    pw = input("enter pword")
    user = userClass.User(em, pw)
    print(user.email)

main()

