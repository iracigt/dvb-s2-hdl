module top (
    input clk,
    input rst,
    input [7:0] data,
    output next_data,
    output valid,
    output [15:0] I,
    output [15:0] Q
);


wire [2:0] header_sym;
wire [2:0] shifter_sym;
wire [2:0] mod_sym;
wire [1:0] R;
wire shifter_irq;
wire shift_hold;
wire gc_reset;
wire shifter_rst;
wire [7:0] I_sym;
wire [7:0] Q_sym;
wire [7:0] I_fin;
wire [7:0] Q_fin;
reg dvalid;
wire fvalid;

assign I_fin = clk_sym ? I_sym : 8'b0;
assign Q_fin = clk_sym ? Q_sym : 8'b0;

/* verilator lint_off UNUSED */
wire fready;
/* verilator lint_on UNUSED */

reg [15:0] index = 0; 

PLHeaderGen hdr (
    .idx(index),
    .sym(header_sym)
);

SymbolShifter shifter (
    .irq(shifter_irq),
    .sym(shifter_sym),
    .clk(clk_sym),
    .data(data),
    .hold(shift_hold),
    .reset(shifter_rst)
);

GoldCode_HDL code (
    .R(R),
    .clk(clk_sym),
    .reset(gc_reset)
);

PL_Scrambler mod (
    .sym(mod_sym),
    .R(R),
    .I(I_sym),
    .Q(Q_sym)
);

IQ_FIRFilter filt (
    .i_clk_x16(clk_filt),
    .i_rst(rst),
    .i_en(1'b1),
    .i_I(I_fin),
    .i_Q(Q_fin),
    .o_ready(fready),
    .o_valid(fvalid),
    .o_I(I),
    .o_Q(Q)
);

reg [4:0] div = 0;
wire clk_sym;
// wire clk_samp;
wire clk_filt;

assign clk_sym = div[4];
// assign clk_samp = div[3];
assign clk_filt = clk;

always @(posedge clk) begin
    div <= div + 1;
end

always @(posedge clk_sym) begin
    if (rst) begin
        index <= 0;
        dvalid <= 0;
    end else begin
        if (index == 21689) begin
            index <= 0;
        end else begin
            index <= index + 1;
        end
        dvalid <= 1;
    end
end

assign valid = dvalid && fvalid;

assign mod_sym = (index < 90) ? header_sym : shifter_sym;
assign gc_reset = index < 90 || 1;
assign shift_hold = index < 88; // two cycles early to allow it to fill
assign next_data = (index < 21687) && (index > 88) && shifter_irq; // supress the last irq
assign shifter_rst = index == 0; // Reset shifter with each new packet

endmodule
