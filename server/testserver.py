from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO

def score_update(filename, p1score, p2score):
    f = open(filename, 'w')

    p1score = str(p1score)
    p2score = str(p2score)
    newstr = p1score + '\n' + p2score
    f.write(newstr)
    result = "*** " + p1score + " - " + p2score + " ***"
    return result




class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    #Get is a query for the results of the game
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        result = self.process_results()
        result_as_bytes = bytearray(result, "utf8")
        self.wfile.write(result_as_bytes)
        


    #Post is sending user input to the server to play game
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        f = open("data.txt", "a")
        response = BytesIO()
        response.write(b'Thank you for your submission')
        response.write(b'\nReceived: ')
        response.write(body)
        f.write("\n"+ body.decode("utf-8"))
        self.wfile.write(response.getvalue())
        f.close()

    def process_results(self):
        cfile = open('./database/requests.txt', 'r')
        contents = cfile.readlines()[0]
        numrequests = int(contents)
        cfile.close()
        cfile = open('./database/requests.txt', 'w')
        line = str(numrequests+1)
        cfile.write(line)
        cfile.close()
        
        
        f = open("data.txt", "r")
        playerDict = {
                "p1" : "null",
                "p2" : "null"
                }

        for line in f:
            if line[0:2] == "p1":
                playerDict["p1"] = line[3]
            elif line[0:2] == "p2":
                playerDict["p2"] = line[3]

        f.close()
        
        last_line = '0'

        with open("data.txt", "r") as file:
            for last_line in file:
                pass
        f.close()

        if((last_line != '1') and (last_line != '2')): 
            f = open("data.txt", "a")
            f.write("\n1")
            f.close()
            return "bad"

        elif(last_line == '1'):
            f = open("data.txt", "a")
            f.write("\n2")
            f.close()
            return "bad"

        elif(last_line == '2'):
            f = open("data.txt", "a")
            f.write("\n2")
            f.close()
            scorefile = './database/score.txt'
            f = open('./database/score.txt', 'r')
            
            contents = f.readlines()
            #print(contents)
            p1score = int(contents[0])
            p2score = int(contents[1])
            if (playerDict["p1"] == "r") and (playerDict["p2"] == "p"):

                if(numrequests % 2 == 0):
                    p2score = p2score + 1
                score = score_update(scorefile, p1score, p2score)
                return "Player 2 wins" + score
        
            elif (playerDict["p1"] == "r") and (playerDict["p2"] == "s"):

                if(numrequests % 2 == 0):
                    p1score = p1score + 1
                score = score_update(scorefile, p1score, p2score)
                return "Player 1 wins." + score

            elif (playerDict["p1"] == "r") and (playerDict["p2"] == "r"):
                score = score_update(scorefile, p1score, p2score)
                return "Duplicate thow, try again." + score

            elif (playerDict["p1"] == "p") and (playerDict["p2"] == "r"):

                if(numrequests % 2 == 0):
                    p1score = p1score + 1
                score = score_update(scorefile, p1score, p2score)
                return "Player 1 wins." + score

            elif (playerDict["p1"] == "p") and (playerDict["p2"] == "s"):

                if(numrequests % 2 == 0):
                    p2score = p2score + 1
                score = score_update(scorefile, p1score, p2score)
                return "Player 2 wins" + score

            elif (playerDict["p1"] == "p") and (playerDict["p2"] == "p"):
                score = score_update(scorefile, p1score, p2score)
                return "Duplicate thow, try again." + score

            elif (playerDict["p1"] == "s") and (playerDict["p2"] == "r"):

                if(numrequests % 2 == 0):
                    p2score = p2score + 1
                score = score_update(scorefile, p1score, p2score)
                return "Player 2 wins" + score

            elif (playerDict["p1"] == "s") and (playerDict["p2"] == "p"):

                if(numrequests % 2 == 0):
                    p1score = p1score + 1
                score = score_update(scorefile, p1score, p2score)
                return "Player 1 wins." + score

            elif (playerDict["p1"] == "s") and (playerDict["p2"] == "s"):
                score = score_update(scorefile, p1score, p2score)
                return "Duplicate thow, try again." + score

            elif (playerDict["p1"] == "n") and (playerDict["p2"] == "n"):
                
                    f= open("./database/score.txt", "w")
                    f.write('0\n0')
                    f.close()
                    return "New Game *** 0-0 ***" 

            else:
                return "bad"



httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
