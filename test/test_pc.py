import os
from enum import IntEnum
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ReadOnly, RisingEdge
from cocotb_tools.runner import get_runner

proj_path = Path(__file__).resolve().parent
rtl_path = proj_path.parent / "rtl"
build_dir = proj_path.parent / "build" / "pc"


def test_pc_runner():
    sim = os.getenv("SIM", "verilator")
    runner = get_runner(sim)
    runner.build(
        sources=[rtl_path / "pc.sv"],
        hdl_toplevel="pc",
        build_dir=build_dir,
        build_args=[
            "--trace-fst",
            "--trace-structs",
        ],
        always=True,
        waves=True,
    )
    runner.test(hdl_toplevel="pc", test_module="test_pc", waves=True)


class PcOp(IntEnum):
    PC_HOLD = 0
    PC_INC = 1
    PC_LOAD = 2


@cocotb.test()
async def test_pc_operations(dut):
    cocotb.start_soon(Clock(dut.i_clk, 10, unit="ns").start())

    # Assert the active-low asynchronous reset and provide safe inputs.
    dut.i_rst_n.value = 0
    dut.i_pc_op.value = PcOp.PC_HOLD.value
    dut.i_pc_load.value = 0

    # Hold reset for two clock cycles.
    await RisingEdge(dut.i_clk)
    await RisingEdge(dut.i_clk)

    # Release reset between clock edges.
    dut.i_rst_n.value = 1

    # The DUT resets synchronously at this edge because PC_HOLD is selected.
    await RisingEdge(dut.i_clk)
    # Drive the operation for the next edge before entering ReadOnly.
    dut.i_pc_op.value = PcOp.PC_HOLD.value
    await ReadOnly()
    assert dut.o_output.value.to_unsigned() == 0

    # PC_HOLD leaves the current value unchanged.
    await RisingEdge(dut.i_clk)
    dut.i_pc_op.value = PcOp.PC_INC.value
    await ReadOnly()
    assert dut.o_output.value.to_unsigned() == 0

    # PC_INC increments once per rising edge.
    await RisingEdge(dut.i_clk)
    dut.i_pc_op.value = PcOp.PC_INC.value
    await ReadOnly()
    assert dut.o_output.value.to_unsigned() == 1

    await RisingEdge(dut.i_clk)
    dut.i_pc_load.value = 0x1234
    dut.i_pc_op.value = PcOp.PC_LOAD.value
    await ReadOnly()
    assert dut.o_output.value.to_unsigned() == 2

    # PC_LOAD replaces the counter with i_pc_load.
    await RisingEdge(dut.i_clk)
    dut.i_pc_op.value = PcOp.PC_HOLD.value
    await ReadOnly()
    assert dut.o_output.value.to_unsigned() == 0x1234

    # HOLD still works after a load.
    await RisingEdge(dut.i_clk)
    await ReadOnly()
    assert dut.o_output.value.to_unsigned() == 0x1234


@cocotb.test()
async def test_pc_increment(dut):
    cocotb.start_soon(Clock(dut.i_clk, 10, unit="ns").start())

    # reset
    dut.i_rst_n.value = 0
    dut.i_pc_op.value = PcOp.PC_HOLD.value
    dut.i_pc_load.value = 0
    await RisingEdge(dut.i_clk)

    # deassert and incremen 20 times
    dut.i_rst_n.value = 1
    await RisingEdge(dut.i_clk)
    dut.i_pc_op.value = PcOp.PC_INC.value
    ReadOnly()
    assert dut.counter.value == 0

    for i in range(20):
        await RisingEdge(dut.i_clk)
        ReadOnly()
        assert dut.counter.value == i
