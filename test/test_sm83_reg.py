import os
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ReadOnly, RisingEdge, Timer
from cocotb_tools.runner import get_runner

proj_path = Path(__file__).resolve().parent
rtl_path = proj_path.parent / "rtl"
build_dir = proj_path.parent / "build" / "sm83_reg"


def test_sm83_reg_runner():
    sim = os.getenv("SIM", "verilator")
    runner = get_runner(sim)
    runner.build(
        sources=[rtl_path / "sm83_reg.sv"],
        hdl_toplevel="sm83_reg",
        build_dir=build_dir,
        build_args=[
            "--trace-fst",
            "--trace-structs",
        ],
        always=True,
    )
    runner.test(
        hdl_toplevel="sm83_reg",
        test_module="test_sm83_reg",
    )


@cocotb.test()
async def test_write_read_b(dut):
    """Write 0xFF to register B, then read it back on port A."""

    # Start a 10ns-period clock
    cocotb.start_soon(Clock(dut.i_clk, 10, unit="ns").start())

    # Reset the DUT
    dut.i_rst.value = 1
    dut.i_write_en.value = 0
    dut.i_write_sel.value = 0
    dut.i_write_data.value = 0
    dut.i_read_sel_a.value = 0
    dut.i_read_sel_b.value = 0
    dut.i_pair_write_en.value = 0
    dut.i_pair_write_sel.value = 0
    dut.i_pair_write_data.value = 0
    dut.i_pair_read_sel.value = 0

    await RisingEdge(dut.i_clk)
    await RisingEdge(dut.i_clk)
    dut.i_rst.value = 0
    await RisingEdge(dut.i_clk)

    # Write 0xFF to register B (i_write_sel = 3'b000)
    dut.i_write_en.value = 1
    dut.i_write_sel.value = 0b000
    dut.i_write_data.value = 0xFF

    await RisingEdge(dut.i_clk)

    # Deassert write enable
    dut.i_write_en.value = 0

    # Give combinational read logic a moment to settle
    await Timer(1, unit="ns")

    # Select register B on read port A and check the value
    dut.i_read_sel_a.value = 0b000
    await ReadOnly()

    assert dut.o_read_data_a.value == 0xFF, (
        f"Expected o_read_data_a to be 0xFF, got {dut.o_read_data_a.value}"
    )
