import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_addr_8bit_exhaustive(dut):
    for a in range(256):
        for b in range(256):
            for carry_in in range(2):
                dut.i_a.value = a
                dut.i_b.value = b
                dut.i_carry_in.value = carry_in

                # Allow combinational logic to settle
                await Timer(1, unit="ns")

                # Reference calculation
                full_sum = a + b + carry_in
                expected_sum = full_sum & 0xFF
                expected_c = (full_sum >> 8) & 1

                # Carry from bit 3 to bit 4
                low_sum = (a & 0x0F) + (b & 0x0F) + carry_in
                expected_h = (low_sum >> 4) & 1

                expected_z = int(expected_sum == 0)
                expected_n = 0

                # Check sum
                actual_sum = int(dut.sum.value)

                assert actual_sum == expected_sum, (
                    f"SUM failure: "
                    f"A={a:02X}, B={b:02X}, C={carry_in} "
                    f"expected={expected_sum:02X}, "
                    f"got={actual_sum:02X}"
                )

                # Check Z
                actual_z = int(dut.f_z.value)

                assert actual_z == expected_z, (
                    f"Z failure: "
                    f"A={a:02X}, B={b:02X}, C={carry_in} "
                    f"expected={expected_z}, got={actual_z}"
                )

                # Check N
                actual_n = int(dut.f_n.value)

                assert actual_n == expected_n, (
                    f"N failure: "
                    f"A={a:02X}, B={b:02X}, C={carry_in} "
                    f"expected={expected_n}, got={actual_n}"
                )

                # Check H
                actual_h = int(dut.f_h.value)

                assert actual_h == expected_h, (
                    f"H failure: "
                    f"A={a:02X}, B={b:02X}, C={carry_in} "
                    f"expected={expected_h}, got={actual_h}"
                )

                # Check C
                actual_c = int(dut.f_c.value)

                assert actual_c == expected_c, (
                    f"C failure: "
                    f"A={a:02X}, B={b:02X}, C={carry_in} "
                    f"expected={expected_c}, got={actual_c}"
                )

    dut._log.info("All 131072 test cases passed!")


@cocotb.test()
async def test_addr_8bit_directed(dut):
    async def check(a, b, cin, expected_sum, expected_h, expected_c):
        dut.i_a.value = a
        dut.i_b.value = b
        dut.i_carry_in.value = cin

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
