module PL_Scrambler (
	output [7:0] I,
	output [7:0] Q,
	input  [1:0] R,
	input  [2:0] sym
);

reg [7:0] I_reg;
reg [7:0] Q_reg;
reg [7:0] I_mod;
reg [7:0] Q_mod;

/* verilator lint_off UNUSED */
wire [8:0] nI_mod_;
wire [8:0] nQ_mod_;

wire [7:0] nI_mod;
wire [7:0] nQ_mod;

assign nI_mod_ = 9'h100 - {1'b0, I_mod}; // FIXME?
assign nQ_mod_ = 9'h100 - {1'b0, Q_mod}; // FIXME?
assign nI_mod = nI_mod_[7:0];
assign nQ_mod = nQ_mod_[7:0];

always @(sym) begin
    case (sym)
    3'b001: begin I_mod = 8'ha0; Q_mod = 8'h80; end // (1, 0)
    3'b000: begin I_mod = 8'h97; Q_mod = 8'h97; end // (sqrt(2), sqrt(2))
    3'b100: begin I_mod = 8'h80; Q_mod = 8'ha0; end // (0, 1)
    3'b110: begin I_mod = 8'h69; Q_mod = 8'h97; end // (-sqrt(2), sqrt(2))
    3'b010: begin I_mod = 8'h60; Q_mod = 8'h80; end // (-1, 0)
    3'b011: begin I_mod = 8'h69; Q_mod = 8'h69; end // (-sqrt(2), -sqrt(2))
    3'b111: begin I_mod = 8'h80; Q_mod = 8'h60; end // (0, -1)
    3'b101: begin I_mod = 8'h97; Q_mod = 8'h69; end // (sqrt(2), -sqrt(2))
    endcase
end

// always @(sym) begin
//     case (sym)
//     3'b001: begin I_mod = 8'h60; Q_mod = 8'h40; end // (1, 0)
//     3'b000: begin I_mod = 8'h37; Q_mod = 8'h37; end // (sqrt(2), sqrt(2))
//     3'b100: begin I_mod = 8'h40; Q_mod = 8'h60;  end // (0, 1)
//     3'b110: begin I_mod = 8'h29; Q_mod = 8'h37; end // (-sqrt(2), sqrt(2))
//     3'b010: begin I_mod = 8'h20; Q_mod = 8'h40; end // (-1, 0)
//     3'b011: begin I_mod = 8'h29; Q_mod = 8'h29; end // (-sqrt(2), -sqrt(2))
//     3'b111: begin I_mod = 8'h40; Q_mod = 8'h20; end // (0, -1)
//     3'b101: begin I_mod = 8'h37; Q_mod = 8'h29; end // (sqrt(2), -sqrt(2))
//     endcase
// end

always @(R) begin
    case (R)
    2'b00: begin I_reg =  I_mod; Q_reg =  Q_mod; end // *  1
    2'b01: begin I_reg = nQ_mod; Q_reg =  I_mod; end // *  i
    2'b10: begin I_reg = nI_mod; Q_reg = nQ_mod; end // * -1
    2'b11: begin I_reg =  Q_mod; Q_reg = nI_mod; end // * -i
    endcase
end

assign I = I_reg;
assign Q = Q_reg;

endmodule
