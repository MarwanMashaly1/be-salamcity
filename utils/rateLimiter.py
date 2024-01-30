import asyncio

class RateLimiter:
    def __init__(self, rate, burst):
        self.rate = rate  # Requests per second
        self.burst = burst  # Maximum burst size
        self.tokens = burst
        self.last_time = None

    async def wait(self):
        if self.last_time is None:
            self.last_time = asyncio.get_event_loop().time()

        now = asyncio.get_event_loop().time()
        time_passed = now - self.last_time

        self.tokens += time_passed * self.rate
        self.tokens = min(self.tokens, self.burst)
        self.last_time = now

        if self.tokens < 1:
            delay = 1 / self.rate
            await asyncio.sleep(delay)
            self.tokens += 1
