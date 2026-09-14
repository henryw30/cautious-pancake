module sp #(
    parameter integer DATA_WIDTH = 16
) (
    input logic i_clk,
    input logic i_rst_n,
    input logic [1:0] i_sp_op,
    input logic [DATA_WIDTH-1:0] i_sp_load_data,

    output logic [DATA_WIDTH-1:0] o_output
);
  typedef enum logic [1:0] {
    SP_HOLD = 2'b00,
    SP_INC  = 2'b01,
    SP_DEC  = 2'b10,
    SP_LOAD = 2'b11
  } sp_op_t;

  logic [DATA_WIDTH-1:0] counter;

  always_ff @(posedge i_clk or negedge i_rst_n) begin
    if (!i_rst_n) begin
      counter <= '0;
    end else begin
      case (i_sp_op)
        SP_HOLD: ;
        SP_INC:  counter <= counter + 16'h0001;
        SP_DEC:  counter <= counter - 16'h0001;
        SP_LOAD: counter <= i_sp_load_data;

        default: ;
      endcase
    end
  end

  assign o_output = counter;

endmodule
