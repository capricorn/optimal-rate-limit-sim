_t = 0
EPSILON = 1/1e6

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

req = Requester(max_requests_per_sec=3)

def k_req(time_betw_req) -> bool:
    k = Requester.WINDOW_SIZE
    result = True

    for _ in range(k):
        result = req.request()
        if time_betw_req > 0:
            sleep(time_betw_req)
        else:
            sleep(EPSILON)
    
    return result

# sec/req
l = 20
u = EPSILON # Avoid divide by zero difficulties -- close enough to 'instantaneous' 
r = EPSILON
prev_r = r

while True:
    if k_req(r):    # r too slow (or just right)
        l = r
        r = round((r+u)/2, 2)
        print(f'Too slow, increasing rate, r={r} [u={u}, l={l}]')
    else:   # r too fast
        u = r
        r = round((r+l)/2, 2)
        print(f'Too fast, decreasing rate, r={r} [u={u},l={l}]')
    
    if prev_r == r:
        break
    else:
        prev_r = r

print(f'Optimal r: {r:.2f}s {r**(-1):.2f} req/sec')