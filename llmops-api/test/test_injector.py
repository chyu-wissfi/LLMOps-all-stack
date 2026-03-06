"""
@Time: 2026/3/4
@Author: chyu.wissfi@gmail.com
@Description: Test the injector
"""

from injector import Injector, inject
from dataclasses import dataclass
import injector 


class A:
    name:str = "LLMOps"

@inject
class B:
    def __init__(self, a: A) -> None:
        self.a = a

    def print(self):
        print(f"The name of class A is {self.a.name}")

@inject
@dataclass
class C:
    a : A

    def print(self):
        print(f"The name of class A is {self.a.name}")

injector = Injector()
b = injector.get(B)
b.print()
c = injector.get(C)
c.print()