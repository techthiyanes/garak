#!/usr/bin/env python3

import importlib
import os

import backoff
import replicate.exceptions
import tqdm

import garak._config
from garak.generators.base import Generator


class ReplicateGenerator(Generator):
    generator_family_name = "Replicate"
    temperature = 1
    top_p = 1.0
    repetition_penalty = 1

    def __init__(self, name, generations=10):
        self.name = name
        self.fullname = f"Replicate {self.name}"
        self.seed = garak._config.seed

        super().__init__(name, generations=generations)

        if os.getenv("REPLICATE_API_TOKEN", default=None) == None:
            raise Exception(
                'Put the Replicate API token in the REPLICATE_API_TOKEN environment variable (this was empty)\n \
                e.g.: export REPLICATE_API_TOKEN="r8-123XXXXXXXXXXXX"'
            )
        self.replicate = importlib.import_module("replicate")

    @backoff.on_exception(
        backoff.fibo, replicate.exceptions.ReplicateError, max_value=70
    )
    def _call_api(self, prompt):
        response_iterator = self.replicate.run(
            self.name,
            input={
                "prompt": prompt,
                "max_length": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "repetition_penalty": self.repetition_penalty,
                "seed": self.seed,
            },
        )
        return "".join(response_iterator)

    def generate(self, prompt):
        outputs = []
        generation_iterator = tqdm.tqdm(list(range(self.generations)), leave=False)
        generation_iterator.set_description(
            self.fullname[:55]
        )  # replicate names are long incl. hash
        for i in generation_iterator:
            outputs.append(self._call_api(prompt))
        return outputs


default_class = "ReplicateGenerator"
