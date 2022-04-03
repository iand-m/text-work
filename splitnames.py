# splits audio file of speech aligned by Gentle into individual words
# adapted from https://unix.stackexchange.com/a/421294

import ffmpeg
from sys import argv

""" split_wav `audio file` `time listing`

    `audio file` is any file known by local FFmpeg
    `time listing` is a file containing multiple lines of format:
        `start time` `end time` output name 

    times can be either MM:SS or S*
"""

_in_file = argv[1]


def make_time(elem):
    # allow user to enter times on CLI
    t = elem.split(':')

    return float(t[0])


talker = argv[3]

if talker == 'aaron':
    spkr = 'a'
elif talker == 'ian':
    spkr = 'i'
else:
    spkr = talker

list_num = argv[4]


def collect_from_file():
    """file from gentle. [expected word],[found word],[start time],[end time]"""

    time_pairs = []
    with open(argv[2]) as in_times:
        for l, line in enumerate(in_times):
            tp = line.split(",")
            # used expected word + speaker + list runthrough number .wav as filename
            tp[0] = f'{tp[0]}-{spkr}-{list_num}.wav'
            # set start and end times
            tp[2] = make_time(tp[2])
            tp[3] = make_time(tp[3]) - tp[2]
            time_pairs.append(tp)
    return time_pairs


def main():
    for i, tp in enumerate(collect_from_file()):
        # open a file, from `ss`, for duration `t`
        stream = ffmpeg.input(_in_file, ss=tp[2], t=tp[3])
        # output to named file
        stream = ffmpeg.output(stream, tp[0])
        # this was to make trial and error easier
        stream = ffmpeg.overwrite_output(stream)

        # and actually run
        ffmpeg.run(stream)


if __name__ == '__main__':
    main()
