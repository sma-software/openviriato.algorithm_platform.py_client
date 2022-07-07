![#openviriato logo](openviriato_400px.png)

# openviriato.algorithm-platform.py-client

## The Pythonic API Wrapper for Viriato's Algorithm Platform

We provide a Python client implementing the [AlgorithmInterface](py_client/algorithm_interface/algorithm_interface.py) in Python. If you want to implement your algorithms with Python you can use this client instead of working with the REST interface directly. It offers type-hints and takes over all low-level functionality needed like object serialization of Python objects to JSON objects and deserialization in the other direction such that you can immediately start working. In this case, the relevant API for you is directly our Python API. Under the hood, the communication with the Algorithm Platform is still carried out via REST calls and your algorithms run in a separate process. The only thing you have to do is to install the wheel file shipped with the Algorithm Platform SDK in your Python environment, see below.

## Getting Started

We refer the reader to the [Walkthrough using the py_client](walkthroughs/py_client_usage/dist/py_client_usage.md) to see how the py_client can be used by an algorithm.

## Rerouting a train

We propose a [Walkthrough for rerouting a train](walkthroughs/rerouting_a_train/dist/rerouting_a_train.md).

## Creating roster links

In the [Rostering walkthrough](walkthroughs/rostering/dist/rostering.md) we explain how to link pieces of rolling stock together and create empty runs if needed. 

## Wiki

Check out our [Wiki](https://github.com/sma-software/openviriato.algorithm-platform.py-client/wiki) for more information!

