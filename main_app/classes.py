from fpdf import FPDF
from datetime import date

class PDF(FPDF):
    def header(self):
        # Create the TOP title of the Page
        self.set_font(family='times', style='BU', size=24)
        self.set_text_color(55, 121, 186)
        self.cell(0, 10, 'Medicat report and treatement advice', ln=True, align='C')

        # Create the title description of the page
        self.set_font(family='times', style='BI', size=20)
        self.set_text_color(50, 50, 50)
        self.cell(0, 10, 'Doctor treatment advice', ln=True, align='C')

        # Write the page generation date
        self.set_font(family='times', style='I', size=12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 10, f'Date: {date.today()}', ln=True, align='C')

        self.ln(7)

    def footer(self):
        self.set_font('times', style='I', size=10)
        # Create the page footer
        self.set_y(-20)
        self.cell(0, 5, 'Welcome to our Hospital', ln=True, align='C')

        # Create page number for the page
        self.set_x(-10)
        self.set_y(-15)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, f'Page: {self.page_no()}')
