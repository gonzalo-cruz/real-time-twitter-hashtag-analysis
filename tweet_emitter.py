import socket
import time
from colorama import Fore


class TweetStream:
    

    def listen(self, host, port):
        
        # Type of socket, in this case IPV4 addresses are expected to be used
        self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reusing this socket for multiple connections
        self.socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        # Bind to our set IP/port
        self.socketServer.bind((host, port))
        # Queue up as many as 5 connect requests before refusing additional connections
        self.socketServer.listen(5) 
        print(Fore.YELLOW + "[+] listening on port "+str(port), Fore.WHITE)
        self._tweetEmitter()
    
    def _tweetEmitter(self):
        # Only consider 1 process (only one connection allowed, enough for Spark)
        while True:
            # Accept new connection
            conn, addr = self.socketServer.accept()
            print(Fore.GREEN, f'\n[*] Accepted new connection from: {addr[0]}:{addr[1]}', Fore.WHITE)
            with open("tweets_raw_1769MB.json") as f:
                index=1
                for tweet in f:
                    print(Fore.MAGENTA, f'[>] Sending tweet {index}', Fore.WHITE)
                    try:
                        conn.send(tweet.encode())
                        time.sleep(0.1)
                        index+=1
                    except:
                        print(Fore.RED, f'The client is disconnected', Fore.WHITE)
                        exit(1)
                    
if __name__ == "__main__":
    
    host = "0.0.0.0" # No IP restrictions for the IP to be used for a connection
    port = 5000      # The selected port we will use for listening for a connection
    tweetStream = TweetStream()
    tweetStream.listen(host, port)
    