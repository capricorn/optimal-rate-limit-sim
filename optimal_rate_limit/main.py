import time
from math import floor, ceil

class Requester():
    WINDOW_SIZE = 5

    def __init__(self, max_requests_per_sec=1):
        self.max_requests_per_sec = max_requests_per_sec
        self.request_ts_window = []
    
    def reset(self):
        self.request_ts_window = []

    def request(self) -> bool:
        self.request_ts_window.append(time.time())
        if len(self.request_ts_window) < Requester.WINDOW_SIZE:
            return True
        
        req_per_sec = Requester.WINDOW_SIZE/(self.request_ts_window[-1] - self.request_ts_window[0])
        #self.request_ts_window = self.request_ts_window[1:]
        self.request_ts_window.pop(0)
        print(req_per_sec)

        if req_per_sec > self.max_requests_per_sec:
            return False
        
        return True

if __name__ == '__main__':
    req = Requester(max_requests_per_sec=1/3)   # a request every 3 seconds at most

    def k_req(sleep) -> bool:
        k = 5
        for _ in range(k):
            if not req.request():
                req.reset()
                return False
            time.sleep(sleep)
        
        req.reset()
        return True

    l = 0
    u = 10
    r = 0   # Debate: this vs (l+u)/2 (Somewhat makes sense to try the fastest rate)
    prev_r = r

    # TODO: Implement a random components to the rate limit
    # Ex: it may be dynamic depending on traffic at that time of day; show that this is adaptive to that 

    # TODO: Expected number of steps..?
    # TODO: Is tightening the bounds via midpoint the best approach..?
    # I think the problem is r beginning at 0?

    # TODO: Can the bounds be updated to improve the search?
    while True:
        if k_req(r):    # r too slow (or just right)
            u = r
            r = round((r+l)/2, 2)
            #u = round((r+u)/2, 4)
            print(f'Speeding up; new r: {r} [{l},{u}]')
        else:   # r too fast
            l = r
            r = round((r+u)/2, 2)
            #l = round((r+l)/2, 4)
            print(f'Slowing (and cooling) down; new r: {r} [{l},{u}]')
            # imitates a cooldown
            req.reset()
        
        if prev_r == r:
            break
        else:
            prev_r = r
    
    # TODO: Is it possible to _always_ satisfy the limiter?
    # (Clearly the last r _should_ satisfy the limiter.)
    # TODO: The precision shouldn't really matter wrt termination.
    optimal_req_per_sec = Requester.WINDOW_SIZE/r
    print(f'Optimal r: {r}s')

    '''
    while req.request():
        print('Successful request')
        time.sleep(4)

    print('Request failed.')
    '''
