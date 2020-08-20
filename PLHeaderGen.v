module PLHeaderGen (
    input [15:0] idx,
    output [2:0] sym
);

reg [2:0] tbl [0:89];

assign sym = idx < 90 ? tbl[idx[6:0]] : 0;

// fmt = 'initial tbl[{}] = 3\'d{};'
// for i in range(len(hdr)):
//     print(fmt.format(i, hdr[i])

initial tbl[0]  = 3'd0;
initial tbl[1]  = 3'd5;
initial tbl[2]  = 3'd3;
initial tbl[3]  = 3'd6;
initial tbl[4]  = 3'd0;
initial tbl[5]  = 3'd6;
initial tbl[6]  = 3'd3;
initial tbl[7]  = 3'd5;
initial tbl[8]  = 3'd0;
initial tbl[9]  = 3'd5;
initial tbl[10]  = 3'd0;
initial tbl[11]  = 3'd6;
initial tbl[12]  = 3'd3;
initial tbl[13]  = 3'd6;
initial tbl[14]  = 3'd3;
initial tbl[15]  = 3'd5;
initial tbl[16]  = 3'd3;
initial tbl[17]  = 3'd6;
initial tbl[18]  = 3'd3;
initial tbl[19]  = 3'd6;
initial tbl[20]  = 3'd0;
initial tbl[21]  = 3'd6;
initial tbl[22]  = 3'd0;
initial tbl[23]  = 3'd6;
initial tbl[24]  = 3'd3;
initial tbl[25]  = 3'd6;
initial tbl[26]  = 3'd0;
initial tbl[27]  = 3'd5;
initial tbl[28]  = 3'd0;
initial tbl[29]  = 3'd6;
initial tbl[30]  = 3'd0;
initial tbl[31]  = 3'd6;
initial tbl[32]  = 3'd3;
initial tbl[33]  = 3'd6;
initial tbl[34]  = 3'd3;
initial tbl[35]  = 3'd6;
initial tbl[36]  = 3'd3;
initial tbl[37]  = 3'd6;
initial tbl[38]  = 3'd3;
initial tbl[39]  = 3'd5;
initial tbl[40]  = 3'd3;
initial tbl[41]  = 3'd6;
initial tbl[42]  = 3'd3;
initial tbl[43]  = 3'd6;
initial tbl[44]  = 3'd3;
initial tbl[45]  = 3'd5;
initial tbl[46]  = 3'd0;
initial tbl[47]  = 3'd6;
initial tbl[48]  = 3'd0;
initial tbl[49]  = 3'd6;
initial tbl[50]  = 3'd3;
initial tbl[51]  = 3'd5;
initial tbl[52]  = 3'd3;
initial tbl[53]  = 3'd5;
initial tbl[54]  = 3'd3;
initial tbl[55]  = 3'd6;
initial tbl[56]  = 3'd3;
initial tbl[57]  = 3'd6;
initial tbl[58]  = 3'd3;
initial tbl[59]  = 3'd6;
initial tbl[60]  = 3'd0;
initial tbl[61]  = 3'd5;
initial tbl[62]  = 3'd3;
initial tbl[63]  = 3'd5;
initial tbl[64]  = 3'd3;
initial tbl[65]  = 3'd5;
initial tbl[66]  = 3'd3;
initial tbl[67]  = 3'd6;
initial tbl[68]  = 3'd0;
initial tbl[69]  = 3'd6;
initial tbl[70]  = 3'd3;
initial tbl[71]  = 3'd5;
initial tbl[72]  = 3'd3;
initial tbl[73]  = 3'd6;
initial tbl[74]  = 3'd3;
initial tbl[75]  = 3'd5;
initial tbl[76]  = 3'd3;
initial tbl[77]  = 3'd6;
initial tbl[78]  = 3'd0;
initial tbl[79]  = 3'd6;
initial tbl[80]  = 3'd0;
initial tbl[81]  = 3'd5;
initial tbl[82]  = 3'd0;
initial tbl[83]  = 3'd6;
initial tbl[84]  = 3'd3;
initial tbl[85]  = 3'd5;
initial tbl[86]  = 3'd0;
initial tbl[87]  = 3'd5;
initial tbl[88]  = 3'd3;
initial tbl[89]  = 3'd6;

endmodule
