#import time
#from math import floor, ceil

_t = 0

def time():
    return _t

def sleep(sec):
    global _t
    _t += sec

class Requester():
    WINDOW_SIZE = 5

    def __init__(self, max_requests_per_sec=1):
        self.max_requests_per_sec = max_requests_per_sec
        self.request_ts_window = []
    
    def reset(self):
        self.request_ts_window = []

    def request(self) -> bool:
        self.request_ts_window.append(time())
        if len(self.request_ts_window) < Requester.WINDOW_SIZE:
            return True
        
        req_per_sec = (Requester.WINDOW_SIZE-1)/(self.request_ts_window[-1] - self.request_ts_window[0])
        self.request_ts_window.pop(0)

        if req_per_sec > self.max_requests_per_sec:
            return False
        
        return True

if __name__ == '__main__':
    req = Requester(max_requests_per_sec=1/2)   # a request every 3 seconds at most

    def k_req(time_betw_req) -> bool:
        k = 6
        result = True

        for _ in range(k):
            result = req.request()
            if time_betw_req > 0:
                sleep(time_betw_req)
            else:
                sleep(1/1e6)    # An epsilon of sorts
        
        return result

    # Time (s) between requests (ie sleep)
    l = 20
    u = 0
    r = 0
    prev_r = r

    while True:
        if k_req(r):    # r too slow (or just right)
            l = r
            r = round((r+u)/2, 3)
            print(f'Too slow, increasing rate, r={r} [l={l},u={u}]')
        else:   # r too fast
            u = r
            r = round((r+l)/2, 3)
            print(f'Too fast, decreasing rate, r={r} [l={l},u={u}]')
        
        if prev_r == r:
            break
        else:
            prev_r = r
    
    #optimal_req_per_sec = Requester.WINDOW_SIZE/r
    print(f'Optimal r: {r}s')