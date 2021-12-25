f = open("day16_input.txt")
lines = f.read().splitlines()

debug_print = False
hex_to_bin = {"0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100",
              "5": "0101", "6": "0110", "7": "0111", "8": "1000", "9": "1001",
              "A": "1010", "B": "1011", "C": "1100", "D": "1101", "E": "1110", "F": "1111"}


def bin_to_dec(value):
    rslt = 0
    mlt = 1
    for i in range(len(value) - 1, -1, -1):
        if value[i] == "1":
            rslt += mlt
        mlt *= 2
    return rslt


def process_packet(value, depth):
    def print_indent(my_depth):
        for i in range(my_depth):
            print(" ", end="")
    version_sum = 0
    subpacket_values = []
    process_rslt = []
    packet_version = bin_to_dec(value[0:3])
    packet_type = bin_to_dec(value[3:6])
    if debug_print:
        print_indent(depth)
        print("Processing packet", value, "...")
        print_indent(depth)
        print("Packet version:", value[0:3], "->", packet_version, "| packet type", value[3:6], "->", packet_type)
    if packet_type == 4:
        # this one keeps a numerical value. Read in groups of 5 bits, finish after reading a group that starts with 0
        curr_index = 6
        sub_packet_total = ""
        while True:
            sub_packet = value[curr_index:curr_index + 5]
            sub_packet_total += sub_packet[1:]
            curr_index += 5
            if sub_packet[0] == "0":
                break
        bin_total = bin_to_dec(sub_packet_total)
        if debug_print:
            print_indent(depth)
            print("Raw value", sub_packet_total, "->", bin_total)
        process_rslt = [curr_index, packet_version, bin_total]
        return process_rslt  # total_length of a processed packet + packet version sum + num value
    else:
        if value[6] == "0":
            # read 15 bits: a total length of subpackets, then process subpackets
            subpacket_total_length = bin_to_dec(value[7:22])
            if debug_print:
                print_indent(depth)
                print("Subtype: 0 | subpacket total length:", subpacket_total_length)
            # calculations part
            sub0_index = 22
            while True:
                sub0_rslt = process_packet(value[sub0_index:], depth + 1)
                sub0_index += sub0_rslt[0]
                version_sum += sub0_rslt[1]
                subpacket_values.append(sub0_rslt[2])
                if sub0_index - 22 >= subpacket_total_length:
                    break
            process_rslt = [sub0_index, version_sum + packet_version]
        elif value[6] == "1":
            # read 11 bits: a total number of subpackets in this packet, then process subpackets
            subpacket_total_number = bin_to_dec(value[7:18])
            if debug_print:
                print_indent(depth)
                print("Subtype: 1 | subpacket total number:", subpacket_total_number)
            # calculations part
            sub1_index = 18
            sub1_counter = 0
            while True:
                sub1_rslt = process_packet(value[sub1_index:], depth + 1)
                sub1_index += sub1_rslt[0]
                version_sum += sub1_rslt[1]
                subpacket_values.append(sub1_rslt[2])
                sub1_counter += 1
                if sub1_counter >= subpacket_total_number:
                    break
            process_rslt = [sub1_index, version_sum + packet_version]
    # some post-processing for part 2
    if packet_type == 0:  # sum all subvalues
        process_rslt.append(sum(subpacket_values))
    elif packet_type == 1:  # multiply all packets
        sub_final_rslt = 1
        for subpacket_value in subpacket_values:
            sub_final_rslt *= subpacket_value
        process_rslt.append(sub_final_rslt)
    elif packet_type == 2:  # get minimum
        process_rslt.append(min(subpacket_values))
    elif packet_type == 3:  # get maximum
        process_rslt.append(max(subpacket_values))
    elif packet_type == 5:  # [0] > [1]: return 1 else 0
        if subpacket_values[0] > subpacket_values[1]:
            process_rslt.append(1)
        else:
            process_rslt.append(0)
    elif packet_type == 6:  # [0] < [1]: return 1 else 0
        if subpacket_values[0] < subpacket_values[1]:
            process_rslt.append(1)
        else:
            process_rslt.append(0)
    elif packet_type == 7:  # [0] == [1]: return 1 else 0
        if subpacket_values[0] == subpacket_values[1]:
            process_rslt.append(1)
        else:
            process_rslt.append(0)
    return process_rslt


for line in lines:
    bin_repr = ""
    for ch in line:
        bin_repr += hex_to_bin[ch]
    if debug_print:
        print("HEX", line, "->", "BIN", bin_repr)
    p_rslt = process_packet(bin_repr, 0)
    print("Packet length is:", p_rslt[0], "| packet version sum is:", p_rslt[1], "| packet value is:", p_rslt[2])
    print("----------")
