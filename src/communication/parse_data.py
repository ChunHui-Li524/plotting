from enum import Enum

MAX_SAMPLE_DATA_NUMBER = 512
DATA_LENGTH = MAX_SAMPLE_DATA_NUMBER * 2 + 8        # 1024个点+帧头帧尾等信息8个字节


class DomainEnum(Enum):
    FREQUENCY = 0
    TIME = 1


def parse_frequency_domain_data(valid_data):
    samples_data = valid_data[6:-2]  # 获取采样点数据
    print(samples_data)
    real_voltage = []
    for i in range(0, len(samples_data), 2):
        value = bytes_list_to_normalized(samples_data[i:i+2])
        # if value != 0:
        #     print(value)
        real_voltage.append(value)       # 频域归一化，32767为最大值

    return real_voltage


def check_frame(data):
    header_index, tail_index = find_frame_boundaries(data)
    valid_data = data[header_index:tail_index + 2]
    frame_header = int.from_bytes(valid_data[:2], byteorder='big')  # 注意解析时高低位的定义
    if frame_header != 0xDFFD:
        raise ValueError(f"帧头错误:{frame_header}")
    frame_tail = int.from_bytes(valid_data[-2:], byteorder='big')  # 注意解析时高低位的定义
    if frame_tail != 0xDEAF:
        raise ValueError(f"帧尾错误:{frame_tail}")
    info_id = valid_data[2]
    if info_id != 0x02:
        raise ValueError(f"信息标识错误:{info_id}")
    channel_id = valid_data[3]
    pulse_data_encoding = int.from_bytes(valid_data[4:6], byteorder='big')
    if not (0x01 <= channel_id <= 0x03):
        raise ValueError(f"通道标识错误:{channel_id}")
    if not (0x0 <= pulse_data_encoding <= 0x7D0):
        raise ValueError(f"脉冲数据编码标识错误:{pulse_data_encoding}")
    return channel_id, pulse_data_encoding, valid_data


def bytes_list_to_normalized(byte_list):
    """
    将字节列表转换并归一化。
    参数:
    byte_list (list of bytes): 字节列表，每个元素为单个字节的bytes对象。

    返回:
    float: 归一化后的结果。
    """
    # 确保我们至少有两个字节
    if len(byte_list) >= 2:
        # 将字节列表转换为整数，高位在前
        data = (byte_list[0] << 8) + byte_list[1]

        # 进行归一化处理，仅考虑正数情况
        if 0x0000 <= data <= 0xFFFF:
            return data / 65535.0
        else:
            raise ValueError(f"数据{data}超出预期的正数范围（0x0000至0xFFFF）。")
    else:
        raise ValueError("输入字节列表长度至少需要为2，以表示一个完整的两字节数据。")


def parse_time_domain_data(valid_data):
    samples_data = valid_data[6:-2]  # 获取采样点数据
    real_voltage = []
    for i in range(0, len(samples_data), 2):
        sample_point = int.from_bytes(samples_data[i:i+2], byteorder='big', signed=True)
        real_voltage.append(sample_point * 0.65 / 2048)

        # 如果解码时选择是无符号数，则要根据最高位确定正负，然后进行转换
        # if sample_point > 0:
        #     real_voltage.append(sample_point * 0.65 / 2048)
        # else:
        #     real_voltage.append(-(65535 - sample_point) * 0.65 / 2048)

    return real_voltage


def find_frame_boundaries(data):
    """查找并返回数据中的有效帧头和帧尾位置"""
    frame_header = b'\xDF\xFD'
    header_index = data.find(frame_header)
    if header_index == -1:
        raise ValueError("数据中缺少帧头")

    frame_tail = b'\xDE\xAF'
    tail_index = data.rfind(frame_tail)
    if tail_index == -1:
        raise ValueError("数据中缺少帧尾")

    if header_index + 2 >= tail_index:
        raise ValueError("帧头与帧尾距离过近，无法构成有效帧")

    return header_index, tail_index
