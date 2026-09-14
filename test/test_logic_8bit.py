import os
from enum import IntEnum
from pathlib import Path

import cocotb
from cocotb.triggers import Timer
from cocotb_tools.runner import get_runner

proj_path = Path(__file__).resolve().parent
rtl_path = proj_path.parent / "rtl"
build_dir = proj_path.parent / "build" / "logic_8bit"


def test_logic_8bit_runner():
    sim = os.getenv("SIM", "verilator")
    runner = get_runner(sim)
    runner.build(
        sources=[rtl_path / "logic_8bit.sv"],
        hdl_toplevel="logic_8bit",
        build_dir=build_dir,
        build_args=[
            "--trace-fst",
            "--trace-structs",
        ],
        always=True,
    )
    runner.test(
        hdl_toplevel="logic_8bit",
        test_module="test_logic_8bit",
    )


class LogicOp(IntEnum):
    OP_AND = 0
    OP_OR = 1
    OP_XOR = 2
    OP_CPL = 3


@cocotb.test()
async def test_initial_logic(dut):

    async def check(
        a, b, logic_op, expected_result, expected_z, expected_n, expected_h, expected_c
    ):
        dut.i_a.value = a
        dut.i_b.value = b
        dut.i_sel.value = logic_op

        await Timer(1, unit="ns")

        assert int(dut.result.value) == expected_result
        assert int(dut.f_z.value) == expected_z
        assert int(dut.f_n.value) == expected_n
        assert int(dut.f_h.value) == expected_h
        assert int(dut.f_c.value) == expected_c

    # AND
    await check(0x01, 0x01, LogicOp.OP_AND, 0x01, 0, 0, 1, 0)
