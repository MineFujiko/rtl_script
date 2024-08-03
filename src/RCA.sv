// -------------------------------------------------------------------------------------------------
// Copyright (c) 2020-2023. All rights reserved.
// Project    :
// Filename   :    RCA.sv
// Author     :    Niechuan
// Email      :    niechuan.wk@gmail.com
// Description:
//
// ***********************************************************************************************
// Modification History:
// Date           By           Revision           Change Description
// -----------------------------------------------------------------------------------------------
// 2023-05-12                  1.0                origin
//
//
// ***********************************************************************************************
// Warning:
// Any bug or new reqirement, please report to the Author.
// ***********************************************************************************************

module RCA #(
    parameter C_WIDTH = 16 
)
(
   input      [C_WIDTH-1:0] din_a,
   input      [C_WIDTH-1:0] din_b,
   output     [C_WIDTH  :0] dout
);

// ------------------------------------------------------------------------------------------
// Function: 
// ------------------------------------------------------------------------------------------
logic [C_WIDTH-1:0] ci;
logic [C_WIDTH-1:0] co;
logic [C_WIDTH-1:0] r;

assign ci[0] = 1'b0;

generate
    for(genvar i=0;i<C_WIDTH;i=i+1)
    begin:u_gen_rca
        FA u_FA (
            .a     (din_a[i]),
            .b     (din_b[i]),
            .ci    (ci[i]),
            .r     (r[i]),
            .co    (co[i])
        );

        if (i<C_WIDTH-1) begin
            assign ci[i+1] = co[i];
        end
    end
endgenerate

assign dout = {co[C_WIDTH-1],r[C_WIDTH-1:0]};

endmodule