module sm83_reg #(
    parameter int DATA_WIDTH = 8
) (
    input logic i_clk,
    input logic i_rst,

    // 8 bit signals
    input logic [2:0] i_read_sel_a,
    input logic [2:0] i_read_sel_b,
    output logic [DATA_WIDTH-1:0] o_read_data_a,
    output logic [DATA_WIDTH-1:0] o_read_data_b,

    input logic i_write_en,
    input logic [2:0] i_write_sel,
    input logic [DATA_WIDTH-1:0] i_write_data,

    // 16 bit signals
    // 00 = BC
    // 01 = DE
    // 10 = HL
    // 11 = AF
    input  logic [ 1:0] i_pair_read_sel,
    output logic [15:0] o_pair_read_data,

    input logic        i_pair_write_en,
    input logic [ 1:0] i_pair_write_sel,
    input logic [15:0] i_pair_write_data
);

  // 8 bit registers
  logic [DATA_WIDTH-1:0] a;
  logic [DATA_WIDTH-1:0] b;
  logic [DATA_WIDTH-1:0] c;
  logic [DATA_WIDTH-1:0] d;
  logic [DATA_WIDTH-1:0] e;
  logic [DATA_WIDTH-1:0] f;
  logic [DATA_WIDTH-1:0] h;
  logic [DATA_WIDTH-1:0] l;

  // logic [ADDR_WIDTH-1:0] sp;
  // logic [ADDR_WIDTH-1:0] pc;

  always_ff @(posedge i_clk or posedge i_rst) begin
    if (i_rst) begin
      a <= '0;
      b <= '0;
      c <= '0;
      d <= '0;
      e <= '0;
      f <= '0;
      h <= '0;
      l <= '0;
    end else begin
      // i_pair_write_en takes precedence over i_write_en
      if (i_write_en) begin
        case (i_write_sel)
          3'b000: b <= i_write_data;
          3'b001: c <= i_write_data;
          3'b010: d <= i_write_data;
          3'b011: e <= i_write_data;
          3'b100: h <= i_write_data;
          3'b101: l <= i_write_data;
          // 110 = (HL), not a register
          3'b111: a <= i_write_data;

          default: begin
          end
        endcase
      end

      if (i_pair_write_en) begin
        case (i_pair_write_sel)
          2'b00: begin
            b <= i_pair_write_data[15:8];
            c <= i_pair_write_data[7:0];
          end
          2'b01: begin
            d <= i_pair_write_data[15:8];
            e <= i_pair_write_data[7:0];
          end
          2'b10: begin
            h <= i_pair_write_data[15:8];
            l <= i_pair_write_data[7:0];
          end
          2'b11: begin
            a <= i_pair_write_data[15:8];
            f <= {i_pair_write_data[7:4], 4'b0000};
          end

          default: ;
        endcase
      end
    end
  end

  always_comb begin
    case (i_read_sel_a)
      3'b000: o_read_data_a = b;
      3'b001: o_read_data_a = c;
      3'b010: o_read_data_a = d;
      3'b011: o_read_data_a = e;
      3'b100: o_read_data_a = h;
      3'b101: o_read_data_a = l;
      // 110 means (HL) in many SM83 instruction encodings.
      // Memory access should be handled by the CPU control logic.
      3'b110: o_read_data_a = 8'h00;
      3'b111: o_read_data_a = a;

      default: o_read_data_a = 8'h00;
    endcase

    case (i_read_sel_b)
      3'b000: o_read_data_b = b;
      3'b001: o_read_data_b = c;
      3'b010: o_read_data_b = d;
      3'b011: o_read_data_b = e;
      3'b100: o_read_data_b = h;
      3'b101: o_read_data_b = l;
      3'b110: o_read_data_b = 8'h00;
      3'b111: o_read_data_b = a;

      default: o_read_data_b = 8'h00;
    endcase
  end

  always_comb begin
    case (i_pair_read_sel)
      2'b00: o_pair_read_data = {b, c};
      2'b01: o_pair_read_data = {d, e};
      2'b10: o_pair_read_data = {h, l};
      2'b11: o_pair_read_data = {a, f};

      default: o_pair_read_data = 16'h0000;
    endcase
  end

endmodule
