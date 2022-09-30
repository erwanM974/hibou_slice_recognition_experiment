
# A small experiment to recognize slices of multi-traces using parameterized simulation with HIBOU

Multi-traces are sets of local traces, each corresponding to a sequence of communication actions (emissions or receptions of messages) 
that are observed locally on a specific sub-system or set of co-localized sub-systems. 
A multi-trace is hence a collection of local observations of the same global behavior (which is what was executed in the distributed system).

Under conditions of partial observation, observation might have started too late or ended too early one any one of the local observers that are tasked with logging the different component (local traces) of the multi-traces.
Hence what might be obtained instead of a fully-observed multi-trace is a slice (in the sense of slices of a word) of this unobserved multi-trace.

As a side note, this notion of partial observation can be linked to the absence of synchronisation mechanisms in between distant observers, which may not be able
to ensure having similar periods of observation.

As a specification language for assessing the conformance of multi-traces logged during the execution of a distributed system, 
we use a language of "interactions".
Interactions are formal models,
akin to Message Sequence Charts or UML Sequence Diagrams for their graphical representation,
but more related to process algebra for their structure and the manner in which we exploit them, via an operational-style semantics.

We then propose an algorithm for verifying multi-traces against interactions. 
This algorithm must be tolerant to the absence of synchronisation between distant observers.
Hence it must be able to recognize slices of accepted multi-traces
(accepted multi-traces corresponding to fully observed behaviors that are exactly specified by the interaction specification).

This experiment constitutes a small-scale experimental validation of such an algorithm which is implemented in the HIBOU tool
(see "[hibou_label](https://github.com/erwanM974/hibou_label)").


## Principle of the experiment



## Input data


## Results


