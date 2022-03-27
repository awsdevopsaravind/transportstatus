

def output_df_to_pdf(pdf, df):
    # A cell is a rectangular area, possibly framed, which contains some text
    # Set the width and height of cell
    table_cell_width = 25
    table_cell_height = 6
    # Select a font as Arial, bold, 8
    pdf.set_font('Arial', 'B', 8)
    
    # Loop over to print column names
    cols = df.columns
    for col in cols:
        pdf.cell(table_cell_width, table_cell_height, col, align='C', border=1)
    # Line break
    pdf.ln(table_cell_height)
    # Select a font as Arial, regular, 10
    pdf.set_font('Arial', '', 10)
    # Loop over to print each data in the table
    for row in df.itertuples():
        for col in cols:
            value = str(getattr(row, col))
            pdf.cell(table_cell_width, table_cell_height, value, align='C', border=1)
        pdf.ln(table_cell_height)


from fpdf import FPDF

# 1. Set up the PDF doc basics
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)

# 2. Layout the PDF doc contents
## Title
pdf.cell(40, 10, 'Daily S&P 500 prices report')
## Line breaks
pdf.ln(20)
## Image
pdf.image('chart.png')
## Line breaks
pdf.ln(20)
## Show table of historical data
### Transform the DataFrame to include index of Date
sp500_history_pdf = sp500_history.reset_index()
### Transform the Date column as str dtype
sp500_history_pdf['Date'] = sp500_history_pdf['Date'].astype(str)
### Round the numeric columns to 2 decimals
numeric_cols = sp500_history_pdf.select_dtypes(include='number').columns
sp500_history_pdf[numeric_cols] = sp500_history_pdf[numeric_cols].round(2)
### Use the function defined earlier to print the DataFrame as a table on the PDF 
output_df_to_pdf(pdf, sp500_history_pdf.tail(3))
## Line breaks
pdf.ln(20)
## Show table of historical summary data
sp500_history_summary_pdf = sp500_history_summary.reset_index()
numeric_cols = sp500_history_summary_pdf.select_dtypes(include='number').columns
sp500_history_summary_pdf[numeric_cols] = sp500_history_summary_pdf[numeric_cols].round(2)

output_df_to_pdf(pdf, sp500_history_summary_pdf)
# 3. Output the PDF file
pdf.output('fpdf_pdf_report.pdf', 'F')
