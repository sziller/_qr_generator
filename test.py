def div_string(string: str, size: int) -> list:
    """=== Method name: div_string =====================================================================================
    Returns a list on strings, each made up of <size> number of characters
    :param string: str - the string you want to divide
    :param size: integer - the size of the segments
    ============================================================================================== by Sziller ==="""
    return [string[start:start+size] for start in range(0, len(string), size)]


if __name__ == "__main__":
    szoveg = "123456789\n123456789\n123456789\n123456789\n123456789"
    for _ in div_string(szoveg, 11):
        print(_)
