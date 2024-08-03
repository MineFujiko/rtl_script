// -------------------------------------------------------------------------------------------------
// Copyright (c) 2020-2023. All rights reserved.
// Project    :
// Filename   :    FA.sv
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

module FA
(
    input     a ,
    input     b ,
    input     ci,
    output    r ,
    output    co
);

    assign r  = a^b^ci;
    assign co = (a^b)&ci | (a&b);

endmodule