import requests, time


server = 'http://localhost:8000'
#r = requests.get('http://localhost:8000')
print("Establishing connection with http://localhost:8000")
#r = requests.post(server, 'howdy')
print("Connection Established -")

want2play = 1

player = input("Please enter what player number you are\n (p1 or p2)")

while(want2play):

    value = input("Please enter one of the following - r (rock), p (paper), s (scissors), g (game score), n (new game), quit\n")
   
    f = open("data.txt", "r")

    if(value == 'p' or
        value =='r' or
        value =='s' or
        value =='n' or
        value =='g'):

        data = (player + " " + value)
        #print(data)

    
        r = requests.post(server, data)

        print('Waiting for other player to respond...')
        responded = 1
        while(responded < 10):
            time.sleep(2)
            res = requests.get(server)
            if(res.text != 'bad'):
                print(res, res.text)
                responded = 100
            responded = responded + 1
        if(responded == 10):
            print('You have been stood up')
            

    elif value =='quit':
        print('You have been TERMINAtED')
        want2play = 0
    else:
        print('Wrong answer - you have been TERMINATED')
        want2play = 0







print(r.text)
