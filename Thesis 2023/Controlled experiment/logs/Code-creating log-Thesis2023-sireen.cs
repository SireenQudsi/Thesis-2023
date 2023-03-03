using System;
using System.Runtime.InteropServices;
using Excel = Microsoft.Office.Interop.Excel;




    class Pro
    {

        public static void Main(string[] args)
        {
            Random rnd = new Random();
            int row = 1, caseid = 492;

            int banker, loanamount, ir, date, customer;
            string[] act1 = { "Request Loan", "Check Employee Eligibility", "Cancel Request" };
            string[] act2 = { "Request Loan", "Check Employee Eligibility", "Record Loan Application Information", "Check Amount Legality", "Cancel Request" };
            string[] act3 = { "Request Loan", "Check Employee Eligibility", "Record Loan Application Information", "Check Amount Legality", "Client Assessment", "Cancel Request" };
            string[] act4 = { "Request Loan", "Check Employee Eligibility", "Record Loan Application Information", "Check Amount Legality", "Client Assessment", "Setup Loan Contract", "Check Interest Rate Average", "Cancel Request" };
            string[] act5 = { "Request Loan", "Check Employee Eligibility", "Record Loan Application Information", "Check Amount Legality", "Client Assessment", "Setup Loan Contract", "Check Interest Rate Average", "Sign Loan Contract", "disbursement" };

            int[,] daynn = new int[4, 31];// shorot employee  3amodot is days
            int[] monthsum = new int[4]; // shorot is empolyee 3amodot employee sum amount
            int[,] IR = new int[4, 2]; // shorot 70-74    3amodot  sum of Ir  count IR   to found avg
            int[] cusamount = new int[7]; // number of customers
            string[,] log = new string[120000, 12];
            log[0, 0] = "CaseID";
            log[0, 1] = "CustomerID";
            log[0, 2] = "BankerID";
            log[0, 3] = "Loan Amount";
            log[0, 4] = "Interest Rate";
            log[0, 5] = "Start Time";
            log[0, 6] = "End Time";
            log[0, 7] = "Activity";
            log[0, 8] = "employee loan per day ";//dayn
            log[0, 9] = "Average IR";//ir
            log[0, 10] = "Customer Total Amount";//cusamount
            log[0, 11] = "Employee Total Amount";//monthsum



            for (int i = 0; i < 4; ++i)
                for (int j = 0; j < 31; ++j)
                    daynn[i, j] = 0;

            for (int i = 0; i < 4; i++)
                monthsum[i] = 0;

            for (int i = 0; i < 4; i++)
                for (int j = 0; j < 2; j++)
                    IR[i, j] = 0;

            for (int i = 0; i < 7; i++)
                cusamount[i] = 0;




        for (int i = 3; i < 28; i++)
        {
            date = i;
            int cases = rnd.Next(4, 16);

            for (int j = 0; j < cases; j++)
            {
                customer = rnd.Next(1, 7);
                loanamount = rnd.Next(5000, 20000);
                ir = rnd.Next(1, 9);
                banker = rnd.Next(70, 74);



                if (daynn[banker % 10, date - 1] >= 3)
                {

                    for (int k = 0; k < 3; k++)
                    {
                        log[row, 0] = caseid.ToString();
                        log[row, 1] = customer.ToString();
                        log[row, 2] = banker.ToString();
                        log[row, 3] = "0";
                        log[row, 4] = "0";
                        log[row, 5] = date.ToString();
                        log[row, 6] = date.ToString();
                        log[row, 7] = act1[k];
                        log[row, 8] = daynn[banker % 10, date - 1].ToString();
                        /* if (IR[banker % 10, 1] == 0)
                             log[row, 9] = "0";
                         else
                             log[row, 9] = (IR[banker % 10, 0] / IR[banker % 10, 1]).ToString();*/
                        log[row, 9] = ir.ToString();
                        log[row, 10] = cusamount[customer - 1].ToString();
                        log[row, 11] = monthsum[banker % 10].ToString();

                        row++;

                    }

                    caseid++;

                    /*
                     Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act1[0]);
                     Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act1[1]);
                     Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act1[2]);
                     log[row] = new string[] { customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act1[0] };
                     log[row] = new string[] { customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act1[1] };
                     log[row] = new string[] { customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act1[2] };
                     */

                }

                else if (daynn[banker % 10, date - 1] < 3 && monthsum[banker % 10] + loanamount > 1000000)
                {
                    for (int k = 0; k < 5; k++)
                    {
                        log[row, 0] = caseid.ToString();
                        log[row, 1] = customer.ToString();
                        log[row, 2] = banker.ToString();
                        log[row, 3] = "0";
                        log[row, 4] = "0";
                        log[row, 5] = date.ToString();
                        log[row, 6] = date.ToString();
                        log[row, 7] = act2[k];
                        log[row, 8] = daynn[banker % 10, date - 1].ToString();
                        /*  if (IR[banker % 10, 1] == 0)
                              log[row, 9] = "0";
                          else
                              log[row, 9] = (IR[banker % 10, 0] / IR[banker % 10, 1]).ToString();*/
                        log[row, 9] = ir.ToString();
                        log[row, 10] = cusamount[customer - 1].ToString();
                        log[row, 11] = monthsum[banker % 10].ToString();

                        if (k >= 2)
                            log[row, 3] = loanamount.ToString();

                        row++;

                    }
                    caseid++;

                    /*
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act2[0]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act2[1]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act2[2]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act2[3]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act2[4]);
                    */

                }

                else if (daynn[banker % 10, date - 1] < 3 && monthsum[banker % 10] + loanamount <= 1000000 && cusamount[customer - 1] + loanamount > 200000)
                {

                    for (int k = 0; k < 6; k++)
                    {
                        log[row, 0] = caseid.ToString();
                        log[row, 1] = customer.ToString();
                        log[row, 2] = banker.ToString();
                        log[row, 3] = "0";
                        log[row, 4] = "0";
                        log[row, 5] = date.ToString();
                        log[row, 6] = date.ToString();
                        log[row, 7] = act3[k];
                        log[row, 8] = daynn[banker % 10, date - 1].ToString();
                        /*  if (IR[banker % 10, 1] == 0)
                              log[row, 9] = "0";
                          else
                              log[row, 9] = (IR[banker % 10, 0] / IR[banker % 10, 1]).ToString();*/
                        log[row, 9] = ir.ToString();
                        log[row, 10] = cusamount[customer - 1].ToString();
                        log[row, 11] = monthsum[banker % 10].ToString();

                        if (k > 1)
                            log[row, 3] = loanamount.ToString();

                        row++;

                    }

                    caseid++;

                    /*
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act3[0]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act3[1]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act3[2]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act3[3]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act3[4]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act3[5]);
                    */

                }

                else if (daynn[banker % 10, date - 1] < 3 && monthsum[banker % 10] + loanamount <= 1000000 && cusamount[customer - 1] + loanamount <= 200000 && (IR[banker % 10, 0] + ir) / (IR[banker % 10, 1] + 1) > 6)
                {

                    for (int k = 0; k < 8; k++)
                    {

                        log[row, 0] = caseid.ToString();
                        log[row, 1] = customer.ToString();
                        log[row, 2] = banker.ToString();
                        log[row, 3] = "0";
                        log[row, 4] = "0";
                        log[row, 5] = date.ToString();
                        log[row, 6] = date.ToString();
                        log[row, 7] = act4[k];
                        log[row, 8] = daynn[banker % 10, date - 1].ToString();
                        /*  if (IR[banker % 10, 1] == 0)
                              log[row, 9] = "0";
                          else
                              log[row, 9] = (IR[banker % 10, 0] / IR[banker % 10, 1]).ToString();*/
                        log[row, 9] = ir.ToString();
                        log[row, 10] = cusamount[customer - 1].ToString();
                        log[row, 11] = monthsum[banker % 10].ToString();

                        if (k == 2)
                            log[row, 3] = loanamount.ToString();
                        if (k > 2)
                        {
                            log[row, 3] = loanamount.ToString();
                            log[row, 4] = ir.ToString();
                        }

                        row++;

                    }

                    caseid++;

                    /*
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act4[0]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act4[1]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", banker.ToString(), loanamount.ToString(), "0", date.ToString(), act4[2]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act4[3]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act4[4]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), ir.ToString(), date.ToString(), act4[5]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), ir.ToString(), date.ToString(), act4[6]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), ir.ToString(), date.ToString(), act4[7]);
                    */

                }

                else if (daynn[banker % 10, date - 1] < 3 && monthsum[banker % 10] + loanamount <= 1000000 && cusamount[customer - 1] + loanamount <= 200000 && (IR[banker % 10, 0] + ir) / (IR[banker % 10, 1] + 1) <= 6)
                {


                    for (int k = 0; k < 9; k++)
                    {

                        log[row, 0] = caseid.ToString();
                        log[row, 1] = customer.ToString();
                        log[row, 2] = banker.ToString();
                        log[row, 3] = "0";
                        log[row, 4] = "0";
                        log[row, 5] = date.ToString();
                        log[row, 6] = date.ToString();
                        log[row, 7] = act5[k];
                        log[row, 8] = daynn[banker % 10, date - 1].ToString();// dis
                        /*  if (IR[banker % 10, 1] == 0)
                              log[row, 9] = "0";
                          else
                              log[row, 9] = (IR[banker % 10, 0] / IR[banker % 10, 1]).ToString();*/
                        log[row, 9] = ir.ToString();
                        log[row, 10] = cusamount[customer - 1].ToString();
                        log[row, 11] = monthsum[banker % 10].ToString();

                        if (k >= 2 && k <= 4)
                        {
                            log[row, 3] = loanamount.ToString();


                        }


                        if (k > 4 && k < 8)
                        {
                            log[row, 3] = loanamount.ToString();
                            log[row, 4] = ir.ToString();


                        }

                        if (k == 8)
                        {

                            log[row, 3] = loanamount.ToString();
                            log[row, 4] = ir.ToString();
                            daynn[banker % 10, date - 1]++;
                            log[row, 8] = daynn[banker % 10, date - 1].ToString();
                            IR[banker % 10, 1]++;
                            IR[banker % 10, 0] = IR[banker % 10, 0] + ir;
                            // log[row, 9] = (IR[banker % 10, 0]/IR[banker % 10, 1]).ToString();
                            log[row, 9] = ir.ToString();
                            cusamount[customer - 1] = cusamount[customer - 1] + loanamount;
                            log[row, 10] = cusamount[customer - 1].ToString();
                            monthsum[banker % 10] = monthsum[banker % 10] + loanamount;
                            log[row, 11] = monthsum[banker % 10].ToString();

                        }


                        row++;


                    }







                    caseid++;

                    /*

                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act5[0]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), "0", "0", date.ToString(), act5[1]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act5[2]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act5[3]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), "0", date.ToString(), act5[4]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), ir.ToString(), date.ToString(), act5[5]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), ir.ToString(), date.ToString(), act5[6]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), ir.ToString(), date.ToString(), act5[7]);
                    Console.WriteLine("{0}   {1}   {2}   {3}   {4}   {5}", customer.ToString(), banker.ToString(), loanamount.ToString(), ir.ToString(), date.ToString(), act5[8]);

                   
                   */




                }

            }
        }


            Excel.Application xlApp = new Microsoft.Office.Interop.Excel.Application();

            if (xlApp == null)
            {
                Console.WriteLine("Excel is not properly installed!!");
                return;
            }

            Excel.Workbook xlWorkBook;
            Excel.Worksheet xlWorkSheet;
            object misValue = System.Reflection.Missing.Value;
            xlWorkBook = xlApp.Workbooks.Add(misValue);

            for (int i = 0; i < 3000; i++)
            {
                for (int j = 0; j < 12; j++)
                {
                    xlWorkSheet = (Excel.Worksheet)xlWorkBook.Worksheets.get_Item(1);
                    string v = log[i, j]; 
                    xlWorkSheet.Cells[i + 1, j + 1] = v;
                    Marshal.ReleaseComObject(xlWorkSheet);

                }

            }

            
            


            xlWorkBook.SaveAs("d:\\Sireen2023-month3.csv", Excel.XlFileFormat.xlWorkbookNormal, misValue, misValue, misValue, misValue, Excel.XlSaveAsAccessMode.xlExclusive, misValue, misValue, misValue, misValue, misValue);
            xlWorkBook.Close(true, misValue, misValue);
            xlApp.Quit();

            Marshal.ReleaseComObject(xlWorkBook);
            Marshal.ReleaseComObject(xlApp);




            for (int i = 0; i < 4; i++)
            {
                for (int j = 0; j < 31; j++)
                    Console.Write(daynn[i, j] + "   ");

                Console.WriteLine();
            }

            Console.WriteLine();
            Console.WriteLine();
            for (int i = 0; i < 4; i++)
                Console.Write(monthsum[i] + "   ");

            Console.WriteLine();
            Console.WriteLine();

            for (int i = 0; i < 4; i++)
            {
                for (int j = 0; j < 2; j++)
                    Console.Write(IR[i, j] + "   ");



                Console.WriteLine();
            }

            Console.WriteLine();
            Console.WriteLine();

            for (int i = 0; i < 7; i++)
                Console.WriteLine(cusamount[i]);

            Console.WriteLine();
            Console.WriteLine();
            Console.WriteLine();
            Console.WriteLine();

            /*  for (int i = 0; i < 3000; i++)
               {
                   for (int j = 0; j < 7; j++)
                   {
                       Console.Write(log[i, j] + "  ");



                   }

                   Console.WriteLine();





               }*/

        }







    }



