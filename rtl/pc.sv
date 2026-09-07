module pc #(
    parameter int DATA_WIDTH = 16
) (
    input logic i_clk,
    input logic i_rst_n,
    input logic [1:0] i_pc_op,
    input logic [DATA_WIDTH-1:0] i_pc_next,

    output logic [DATA_WIDTH-1:0] o_output
);
  typedef enum logic [1:0] {
    PC_HOLD = 2'b00,
    PC_INC  = 2'b01,
    PC_LOAD = 2'b10
  } pc_op_t;

  logic [DATA_WIDTH-1:0] counter;

  always_ff @(posedge i_clk or negedge i_rst_n) begin
    if (!i_rst_n) begin
      counter <= '0;
    end else begin
      case (i_pc_op)
        PC_HOLD: ;
        PC_INC:  counter <= counter + 16'h0001;
        PC_LOAD: counter <= i_pc_next;

        default: ;
      endcase
    end
  end

  assign o_output = counter;

endmodule
