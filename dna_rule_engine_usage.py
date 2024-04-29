#!/usr/bin/env python3

import random

from specs import SolutionSpec, TextRetrievalSpec, CryptoSpec
from rules.fsm import FSM
from rules.engine import RuleEngine
from crypto.vigenere import vigenere
from crypto.atbash import ATBASH, RUNE_LOOKUP
from lp import get_pages, get_segments

if __name__ == "__main__":
    fsm = FSM()

    state_transitions = {
        "crypto": {
            # We can define all rule transitions for crypto based on scheme
            "scheme": {
                "vigenere": {
                    "includes": ["$keyed", "*"]
                },
                "running_shift": {
                    "includes": ["$keyed", "*"],
                    "excludes": ["$keyed.key"],
                    "key": lambda: [random.sample(range(-29, 29), random.randint(0, 10))]
                },
                "atbash": {
                    "includes": ["*"]
                },
                "rot": {
                    "includes": ["*"]
                },
                # Attrs prepended with $ should be referenced by their appropriate types
                "$keyed": {
                    # TODO: Will pick from wordlist in future
                    "key": "MUTATED",
                    "excludes": {'a': lambda: random.randint(0, 10), 'b': lambda: random.randint(0, 10)},
                    "skips": {},
                    "key_index": lambda: random.randint(0, len("MUTATED") - 1)
                },
                # * denotes common attributes referenced in all
                "*": {
                    "lookup": lambda: random.choice([ATBASH, RUNE_LOOKUP]), # Should probably create random lookups too
                    "shift": lambda: random.randint(-29, 29)
                }
            }
        },
        "retrieval": {
            "mode": lambda: random.choice([get_pages, get_segments]),
            # TODO: nums - using tooling in argument validations to pull valid ranges
        }
    }

    # Using lambdas in the rules - we can call and still get different values rather than inserting
    # logic in the target function
    print(state_transitions["crypto"]["scheme"]["*"]["lookup"]())
    print(state_transitions["crypto"]["scheme"]["*"]["lookup"]())

    # FIXME: Didn't finish implementing - just wanted to give you a snapshot of my vision for this
    state = "crypto.scheme"
    fsm.set_state(state)
    rule_engine = RuleEngine(fsm)
    mutated_parameters = rule_engine.mutate_parameters()
    print("Mutated parameters:", mutated_parameters)
