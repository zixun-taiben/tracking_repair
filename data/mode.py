# -*- encoding: utf-8 -*-
"""
@File    :   mode.py
@Time    :   2021/07/02 14:18:56
@Author  :   Xing Yun
"""

import os
import random as pyrandom
import numpy as np


def consistent(clip_length:int, severity:int):
    severity_sequence = np.full(clip_length, severity).astype(np.int32)
    return severity_sequence 

def random(clip_length:int, max_pos_count:int, max_frame_count:int):
    """Randomly select frame position, count and severity for perturbation."""
    severity_sequence = np.zeros(clip_length).astype(np.int32)

    pos_count = pyrandom.randint(1,max_pos_count) # 1 perturbation at least
    for _ in range(0, pos_count):
        pos = pyrandom.randint(0, clip_length-1)
        frame_count = pyrandom.randint(1,max_frame_count) # select 1 frames at least to perturb
        if pos+frame_count > clip_length-1:
            severity_sequence[-frame_count:] = pyrandom.randint(1,5)
        else:
            severity_sequence[pos+1:pos+frame_count+1] = pyrandom.randint(1,5)

    return severity_sequence

def smooth(clip_length:int, order: str, max_level:int):
    severity_sequence = np.zeros(clip_length).astype(np.int32)
    if max_level > clip_length:
        raise Exception(f'Unsupport severity level: {max_level}')
    part_length = clip_length // max_level #  all severity levels are considered

    for i in range(max_level): # use i as both index and severity
        if i == max_level-1: 
            severity_sequence[i*part_length:] = max_level
        else:
            severity_sequence[i*part_length:(i+1)*part_length] = i

    if order=='ascending':
        return severity_sequence
    elif order=='descending':
        return np.flip(severity_sequence)
    else:
        raise ValueError(f'Invalid order argument: {order}')

def burst(clip_length:int, order:str, severity:int, burst_pos: int = None):
    severity_sequence = np.zeros(clip_length).astype(np.int32)
    if burst_pos == None:
        burst_pos = pyrandom.randint(0,clip_length-1)
    elif burst_pos >= clip_length or burst_pos < 0:
        burst_pos = pyrandom.randint(0,clip_length-1)
        print(f"Invalid burst frame postion, randomly initialized: {burst_pos}")

    if 0 < severity < 5:
        severity_sequence[burst_pos:] = severity
    else:
        severity_sequence[burst_pos:] = pyrandom.randint(1,5) # randomly set severity
        print(f"Invalid burst severity, randomly initialized: {burst_pos}")

    if order=='ascending':
        return severity_sequence
    elif order=='descending':
        return np.flip(severity_sequence)
    else:
        raise ValueError(f'Invalid order argument: {order}')


def get_severity_sequence(clip_length: int, mode: str, perturb_args: dict) -> list:
    """Get perturbation severity for each frame in the clip based on given perturbation mode.
    
    Args:
        clip_length:
        mode: 
        perturb_args: 

    Return:
        severity_sequence: list of perturbation severity
    """
    if mode.lower() == 'consistent':
        severity_sequence = consistent(clip_length, perturb_args['severity'])
    elif mode.lower() == 'random':
        severity_sequence = random(clip_length, perturb_args['max_pos_count'], perturb_args['max_frame_count'])
    elif mode.lower() == 'smooth':
        severity_sequence = smooth(clip_length, perturb_args['order'], perturb_args['max_level'])
    elif mode.lower() == 'burst':
        severity_sequence = burst(clip_length, perturb_args['order'], perturb_args['severity'], perturb_args['burst_pos'])
    else:
        raise ValueError('Unsupported mode: {}'.format(perturb_args['mode']))

    return severity_sequence