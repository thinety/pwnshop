ALL_CHALLENGES = { }
ALL_MODULES = { }
MODULE_LEVELS = { }

from .challenge import Challenge, KernelChallenge, WindowsChallenge, ChallengeGroup
from .register import register_challenge, register_challenges
from .util import did_segfault, did_timeout, retry
