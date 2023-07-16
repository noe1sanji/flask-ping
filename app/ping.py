import subprocess as sp


def send_ping(host):
    command = f"ping {host} -c2 -W 1000"

    try:
        status, output = sp.getstatusoutput(command)
        if status != 0:
            error = None

            net_error = "Destination Net Unreachable"

            if net_error in output:
                error = net_error
                raise Exception("Timeout")

            packet_loss = "100% packet loss"

            if packet_loss in output:
                error = packet_loss
                raise Exception("Packet loss")

            if error is None:
                raise Exception(f"Error: {output}")

        stats = output.split("\n")[-1:][0].split(" ")
        rtt_min, rtt_avg, rtt_max, rtt_mdev = stats[-2:][0].split("/")

        return int(float(rtt_avg))
    except Exception as e:
        print(e)
        return 0
