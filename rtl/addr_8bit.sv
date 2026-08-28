module addr_8bit #(
    parameter int DATA_WIDTH = 8
) (
    input logic [DATA_WIDTH-1:0] i_a,
    input logic [DATA_WIDTH-1:0] i_b,
    input logic i_c,

    output logic [DATA_WIDTH-1:0] sum,
    output logic f_z,
    output logic f_n,
    output logic f_h,
    output logic f_c
);

  assign f_n = 1'b0;
  logic [4:0] half_sum;

  always_comb begin
    {f_c, sum} = i_a + i_b + i_c;

    half_sum = {1'b0, i_a[3:0]} + {1'b0, i_b[3:0]} + i_c;

    f_z = (sum == '0);
    f_h = half_sum[4];
  end

endmodule
