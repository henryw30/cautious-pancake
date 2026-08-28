import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_addr_8bit_directed(dut):
    async def check(a, b, cin, expected_sum, expected_h, expected_c):
        dut.i_a.value = a
        dut.i_b.value = b
        dut.i_c.value = cin

        await Timer(1, unit="ns")

        assert int(dut.sum.value) == expected_sum
        assert int(dut.f_h.value) == expected_h
        assert int(dut.f_c.value) == expected_c
        assert int(dut.f_z.value) == int(expected_sum == 0)
        assert int(dut.f_n.value) == 0

    # 1 + 1 = 2
    await check(0x01, 0x01, 0, 0x02, 0, 0)

    # Half carry: 0x0F + 1 = 0x10
    await check(0x0F, 0x01, 0, 0x10, 1, 0)

    # Carry: 0xFF + 1 = 0x00
    await check(0xFF, 0x01, 0, 0x00, 1, 1)

    # Carry-in causes half carry: 0x0F + 0 + 1 = 0x10
    await check(0x0F, 0x00, 1, 0x10, 1, 0)

    # Carry-in causes full carry: 0xFF + 0 + 1 = 0x00
    await check(0xFF, 0x00, 1, 0x00, 1, 1)

    # No carry
    await check(0x12, 0x23, 0, 0x35, 0, 0)
