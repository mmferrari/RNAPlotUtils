#!/usr/bin/env python3
import argparse
import os
import re

"""
Script to convert a file created with Multistrand/DrTransformer/Kinwalker for RNAplot.


Copyright 2019 Margherita Maria Ferrari.


This file is part of RNAPlotUtils.

RNAPlotUtils is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RNAPlotUtils is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RNAPlotUtils.  If not, see <http://www.gnu.org/licenses/>.
"""


class RNAPlotUtils:
    NUM_DIGITS = 5
    SEQUENCE_PATTERN = re.compile(r'^[ACGTU]+$')
    SEC_STRUCT_PATTERN = re.compile(r'^[.()]+')

    @classmethod
    def get_args(cls):
        parser = argparse.ArgumentParser(description='RNAplot utils')
        parser.add_argument('-i1', '--input-multistrand', metavar='MULTISTRAND_IN_FILE', type=str, required=False,
                            help='Multistrand input file', default=None)
        parser.add_argument('-i2', '--input-drtransformer', metavar='DRTRANSFORMER_IN_FILE', type=str, required=False,
                            help='Drtransformer input file', default=None)
        parser.add_argument('-i3', '--input-kinwalker', metavar='KINWALKER_IN_FILE', type=str, required=False,
                            help='Kinwalker input file', default=None)
        return parser.parse_args()

    @classmethod
    def convert_multistrand_file(cls, input_file=None, output_file=None):
        if not input_file or not output_file:
            raise AssertionError('You must specify input and output files (multistrand)')

        sequence = ''
        sec_structs = list()
        output = ''

        with open(input_file, 'r') as fin:
            line = fin.readline()

            while not sequence:
                if not line:
                    raise AssertionError('Cannot find the sequence (multistrand)')

                line = line.replace('\n', '')
                found = cls.SEQUENCE_PATTERN.findall(line)
                line = fin.readline()

                if len(found) > 0:
                    sequence = found[0].replace('T', 'U')

            while line:
                line_parts = line.replace('\n', '').split()
                line = fin.readline()

                if len(line_parts) == 0:
                    continue

                found = cls.SEC_STRUCT_PATTERN.findall(line_parts[0])

                if len(found) > 0:
                    sec_structs.append(found[0])

        step_count = 0
        for sec_struct in sec_structs:
            step_count += 1
            output += '\n>multistrand_' + str(step_count).rjust(cls.NUM_DIGITS, '0') + '\n' + \
                      sequence[0:len(sec_struct)] + '\n' + \
                      sec_struct + '\n'

        if not output:
            raise AssertionError('** ERROR **  Nothing to write to output file (multistrand)')

        with open(output_file, 'w') as fout:
            fout.write(output)

    @classmethod
    def convert_drtransformer_file(cls, input_file=None, output_file=None):
        if not input_file or not output_file:
            raise AssertionError('You must specify input and output files (drtransformer)')

        sequence = ''
        sec_structs = list()
        output = ''

        with open(input_file, 'r') as fin:
            line = fin.readline()

            while not sequence:
                if not line:
                    raise AssertionError('Cannot find the sequence (drtransformer)')

                line = line.replace('\n', '').strip('#').strip()
                found = cls.SEQUENCE_PATTERN.findall(line)
                line = fin.readline()

                if len(found) > 0:
                    sequence = found[0]

            last_step = False
            step = '-1'
            step_idx = '-1'
            occupancy = '-1'

            while line:
                line_parts = line.replace('\n', '').split()
                line = fin.readline()

                if len(line_parts) < 5:
                    continue

                found = cls.SEC_STRUCT_PATTERN.findall(line_parts[2])

                if len(found) == 0:
                    continue

                if step == line_parts[0] or last_step:
                    if step_idx > line_parts[1]:
                        last_step = True
                    elif occupancy < line_parts[4]:
                        sec_structs.remove(sec_structs[len(sec_structs) - 1])
                    else:
                        continue

                step = line_parts[0]
                step_idx = line_parts[1]
                occupancy = line_parts[4]
                sec_structs.append(found[0])

        step_count = 0
        for sec_struct in sec_structs:
            step_count += 1
            output += '\n>drtransformer_' + str(step_count).rjust(cls.NUM_DIGITS, '0') + '\n' + \
                      sequence[0:len(sec_struct)] + '\n' + \
                      sec_struct + '\n'

        if not output:
            raise AssertionError('** ERROR **  Nothing to write to output file (drtransformer)')

        with open(output_file, 'w') as fout:
            fout.write(output)

    @classmethod
    def convert_kinwalker_file(cls, input_file=None, output_file=None):
        if not input_file or not output_file:
            raise AssertionError('You must specify input and output files (kinwalker)')

        sequence = ''
        sec_structs = list()
        output = ''

        with open(input_file, 'r') as fin:
            line = fin.readline()

            while not sequence:
                if not line:
                    raise AssertionError('Cannot find the sequence (kinwalker)')

                line = line.replace('\n', '').split()[0]
                found = cls.SEQUENCE_PATTERN.findall(line)
                line = fin.readline()

                if len(found) > 0:
                    sequence = found[0]

            while line:
                line_parts = line.replace('\n', '').split()
                line = fin.readline()

                if len(line_parts) == 0:
                    continue

                found = cls.SEC_STRUCT_PATTERN.findall(line_parts[0])

                if len(found) == 0:
                    continue

                sec_structs.append(found[0])

        step_count = 0
        for sec_struct in sec_structs:
            step_count += 1
            output += '\n>kinwalker_' + str(step_count).rjust(cls.NUM_DIGITS, '0') + '\n' + \
                      sequence[0:len(sec_struct)] + '\n' + \
                      sec_struct + '\n'

        if not output:
            raise AssertionError('** ERROR **  Nothing to write to output file (kinwalker)')

        with open(output_file, 'w') as fout:
            fout.write(output)


if __name__ == '__main__':
    args = vars(RNAPlotUtils.get_args())

    if args.get('input_multistrand', None):
        in_file = args.get('input_multistrand', None)
        basename, ext = os.path.splitext(in_file)
        out_file = basename + '.vienna'
        RNAPlotUtils.convert_multistrand_file(in_file, out_file)

    if args.get('input_drtransformer', None):
        in_file = args.get('input_drtransformer', None)
        basename, ext = os.path.splitext(in_file)
        out_file = basename + '.vienna'
        RNAPlotUtils.convert_drtransformer_file(in_file, out_file)

    if args.get('input_kinwalker', None):
        in_file = args.get('input_kinwalker', None)
        basename, ext = os.path.splitext(in_file)
        out_file = basename + '.vienna'
        RNAPlotUtils.convert_kinwalker_file(in_file, out_file)
