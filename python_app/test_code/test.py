#!/usr/bin/python3
import random

const = ['1', '2', '3', '4', '5']
extend = ".jpeg"

def img_select(const):
    return random.choice(const) + extend

print("test result is: ", img_select(const))
