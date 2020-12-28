# error-correction
Algorithms for real-time correction of 2d laser sensor slips and bursts.

Both algorithms are based on literature from the area of quickest detection, which is concerned with detecting changes in the distribution of data received in real time

The first algorithm is a CUSUM algorithm that detects consecutive changes in mean.
The second algorithm is a CUSUM-like algorithm that detects spikes or bursts in theb data.
It uses Hidden Markov Models to model the data, and detects a change from one HMM to another.
