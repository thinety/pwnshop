import pwnshop
import pwnlib.asm, pwnlib.shellcraft
import os

class ShellBase(pwnshop.Challenge, register=False): # don't register this as an actual challenge
    TEMPLATE_PATH = "example_shell.c"
    EXEC_STACK = True
    CANARY = True
    LINK_LIBRARIES = ["capstone"]

    stack_shellcode = False
    shellcode_size = 0x1000
    allocation_size = 0x1000
    remap_rx_size = 0x0
    shellcode_filter = None
    close_stdin = False
    close_stdout = False
    close_stderr = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shellcode_address = self.random.randrange(0x13370000, 0x31337000, 0x1000)

class ShellExample(ShellBase):
    """
    An example shellcode loader.
    """

    stack_shellcode = True
    shellcode_size = 0x1000
    allocation_size = 0x1000

    def verify(self, **kwargs):
        """
        Read 0x1000 bytes onto the stack (address varies every time that it is run)
        """
        with self.run_challenge(**kwargs) as process:
            shellcode = pwnlib.asm.asm(
                pwnlib.shellcraft.open("/flag") + pwnlib.shellcraft.sendfile(1, 3, 0, 1024) + pwnlib.shellcraft.exit(0)
            )
            process.clean()
            process.write(shellcode)
            assert self.flag in process.readall()

class ShellOptimized(ShellExample):
    """
    The same example, but optimized with -O3.
    """
    OPTIMIZATION_FLAG = "-O3"
    DEBUG_SYMBOLS = True

class ShellBadVerifier(ShellExample):
    """
    The same example, with a verifier that fails.
    """

    def verify(self, binary=None, **kwargs):
        assert False

class Shell1604(ShellExample):
    """
    The same example, built using Ubuntu 16.04.
    """

    BUILD_IMAGE = "ubuntu:16.04"
    APT_DEPENDENCIES = [ "libcapstone-dev" ]
    PIN_LIBRARIES = True

    def build_compiler_cmd(self):
        cmd = super().build_compiler_cmd()

        # ubuntu 16.04's gcc doesn't support the file-prefix-map option we use to hide file paths
        return [ a for a in cmd if not a.startswith("-ffile-prefix-map") ]

class Shell1604InVitu(Shell1604):
    """
    The same example, built using Ubuntu 16.04 and verified in the same container, without the need for library pinning.
    """

    BUILD_IMAGE = "ubuntu:16.04"
    VERIFY_IMAGE = "ubuntu:16.04"
    PIN_LIBRARIES = False
