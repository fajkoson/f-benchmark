from pseudoconsole import PseudoConsole
import time


def gotcha() -> None:
    """
    Minimal test function to validate that the PseudoConsole Python binding works.
    Spawns a CMD shell, writes a simple echo command, and prints the output.
    """
    try:
        pc = PseudoConsole()
        pc.spawn("cmd.exe")
        pc.write("echo yo from py\n")
        pc.write("exit\n")
        time.sleep(0.1)
        print(">>>", pc.read())
    finally:
        pc.close()
