
def escape4glog(instr: str) -> str:
    """[summary]

    Args:
        instr (str): [description]

    Returns:
        str: [description]
    """
    outstr = instr.replace('[', '\\[').replace(']', '\\]')
    return outstr.replace('\\[', '[[]').replace('\\]', '[]]')


if __name__ == "__main__":
    pass
