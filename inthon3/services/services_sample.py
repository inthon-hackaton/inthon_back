from fastapi import Depends, HTTPException, Response
from repository.repository_sample import SampleRepository

class SampleService():
    def __init__(self, repository: SampleRepository = Depends()) -> None:
        self.repository = repository