"""Tiny in-memory cooldown budget to avoid repeated media sends.

No database, timers, background polls or user-content logs. Each instance
is fixed-capacity. This is per-process protection, not a distributed limiter.
"""
from time import monotonic

class CooldownBudget:
    def __init__(self, seconds=3.0, capacity=1000, clock=None):
        if not isinstance(seconds,(int,float)) or isinstance(seconds,bool) or seconds<=0:
            raise ValueError("Positive cooldown required")
        if type(capacity) is not int or capacity<1:
            raise ValueError("Positive capacity required")
        self.seconds=float(seconds)
        self.capacity=capacity
        self.clock=clock or monotonic
        self._latest={}

    def allow(self, chat_id, user_id):
        if type(chat_id) is not int or type(user_id) is not int or chat_id<=0 or user_id<=0:
            return False
        now=self.clock()
        key=(chat_id,user_id)
        last=self._latest.get(key)
        if last is not None and now-last<self.seconds:
            return False
        if key not in self._latest and len(self._latest)>=self.capacity:
            oldest=min(self._latest,key=self._latest.get)
            self._latest.pop(oldest,None)
        self._latest[key]=now
        return True
